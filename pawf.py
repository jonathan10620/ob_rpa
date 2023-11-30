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

def make_request(url):
    try:
        session = requests.Session()
        response = session.get(url, auth=HttpNtlmAuth(USER, PASSWORD), timeout=100)
        response.raise_for_status()  # Raise HTTPError for bad responses
        return Soup(response.text)
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error: Request failed. {e}")

def grab_field(soup, id):
    try:
        return soup.find("input", {"id": id}, mode="first").attrs["value"].strip()
    except AttributeError as e:
        raise RuntimeError(f"Error: Unable to find field with id '{id}'.") from e

def parse_date(date_str):
    if date_str:
        return datetime.strptime(date_str, "%m/%d/%Y %X %p")
    return None

def get_pawf_info(pid):
    url_root = f"http://operations.tmhp.net/PA/PawfTicket/WorkResults?dln={pid}&refererSource=SearchResults"
    
    try:
        soup = make_request(url_root)
    except RuntimeError as e:
        print(e)
        return None

    pan = grab_field(soup, "PANumber")
    rec_date_s = grab_field(soup, "ReceivedDate")
    dob = grab_field(soup, "ClientDOB")

    pawf_client_info = {
        "pcn": grab_field(soup, "PCN"),
        "dob": datetime.strptime(dob, "%m/%d/%Y") if dob else None,
        "first_name": grab_field(soup, "ClientFirstName"),
        "last_name": grab_field(soup, "ClientLastName"),
    }
    pyperclip.copy(pawf_client_info['pcn'])

    pawf_provider_info = {
        "tpi": grab_field(soup, "providerInformation_LegacyID"),
        "npi": grab_field(soup, "NPI"),
        "name": grab_field(soup, "providerInformation_LastName"),
        "fax": grab_field(soup, "ProviderFaxNumber"),
    }

    rec_date = parse_date(rec_date_s)

    data = {
        "pan": pan,
        "rec_date": rec_date,
        "method": grab_field(soup, "SourceId"),
        "client": pawf_client_info,
        "provider": pawf_provider_info,
    }
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