from datetime import datetime
import requests
from requests_ntlm import HttpNtlmAuth
from gazpacho import Soup
from pprint import pprint
import pyperclip



class PortalError(Exception):
    pass

class PidLengthError(PortalError):
    pass

class PidNotNumericError(PortalError):
    pass



USER = "TMHP\\jonathan.delapaz"
PASSWORD = "XC4life123;"


def get_pawf_info(pid):
    """
    Accepts a portal id and returns a dict
    with pan, client info, and provider info
    """
    
    



    def grab_field(soup, id):
        try:
            return soup.find("input", {"id": id}, mode="first").attrs["value"].strip()
        except AttributeError as e:
            print(f"Error: Unable to find field with id '{id}'.")
            return None

    url_root = f"http://operations.tmhp.net/PA/PawfTicket/WorkResults?dln={pid}&refererSource=SearchResults"

    try:
        req = requests.get(url_root, auth=HttpNtlmAuth(USER, PASSWORD), timeout=100)
    except requests.exceptions.RequestException as e:
        print(f"Error: Request failed. {e}")
        return None

    try:
        s = Soup(req.text)
    except Exception as e:
        print(f"Error: Unable to parse response as HTML. {e}")
        return None

    pan = grab_field(s, "PANumber")
    rec_date_s = grab_field(s, "ReceivedDate")
    dob = grab_field(s, "ClientDOB")

    pawf_client_info = {
        "pcn": grab_field(s, "PCN"),
        "dob": datetime.strptime(dob.strip(), "%m/%d/%Y") if dob else None,
        "first_name": grab_field(s, "ClientFirstName"),
        "last_name": grab_field(s, "ClientLastName"),
    }
    pyperclip.copy(pawf_client_info['pcn'])

    pawf_provider_info = {
        # this is the legacy ID formerly known as tpi, keeping tpi for convenience
        "tpi": grab_field(s, "providerInformation_LegacyID"),

        "npi": grab_field(s, "NPI"),

        "name": grab_field(s, "providerInformation_LastName"),
        "fax": grab_field(s, "ProviderFaxNumber"),
    }

    if rec_date_s:
        rec_date = datetime.strptime(rec_date_s, "%m/%d/%Y %X %p")
    else:
        rec_date = None

    data = {
        "pan": pan,
        "rec_date": rec_date,
        "method": grab_field(s, "SourceId"),
        "client": pawf_client_info,
        "provider": pawf_provider_info,
    }
    # copy pcn so that it facilitaes client lookup/duplicate lookup
    pyperclip.copy(data['client']['pcn'])
    pprint(data)

    return data



def fetch_pawf_data(portal):
    try:
        if len(portal) != 9:
            raise PidLengthError("Ensure PID is length 9.")
        
        int(portal)  # Check if portal is numeric
    except PidLengthError as e:
        raise PortalError(str(e))
    except ValueError:
        raise PortalError("Ensure PID is a numeric digit.")
    
    try:
        return get_pawf_info(portal)
    except Exception as e:
        raise PortalError("Error getting pawf information, ensure credentials are updated.")