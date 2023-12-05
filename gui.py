import PySimpleGUI as sg
import pyperclip

from pawf import fetch_pawf_data
import gui_helpers as gh
from tools import calculate_age, generate_blurb

from layout import main_layout
from selenium_actions import load_ticket_page, click_header_tab

sg.theme('DarkBlue8')
window = sg.Window("OB", main_layout, keep_on_top=True, finalize=True)

pawf_data = {}


#! ------------BEGIN MAIN LOOP-------------
while True:
    event, values = window.read(timeout=150)
    gh.display_mco_field(window, values)

    if event == "go":
        portal = values["portal_id"]
        try:
            pawf_data = fetch_pawf_data(portal)
        except Exception as e:
            sg.popup(str(e))
            continue

        # Update PCN field with pawf data retrieved
        pcn = pawf_data.get("client").get("pcn")
        gh.update_gui_field(window, "pcn", pcn)

        pan = pawf_data.get("pan")
        load_ticket_page(pan, portal)
        click_header_tab()
        gh.populate_requested_dos_field(window)

        # populate procedure field
        gh.populate_procedures_field(window)



    if event == "copy":
        # Get gui values
        portal = values.get("portal_id", "<PORTAL_ID>")
        mco_start_date = values.get("mco_start_date", "<MCO_START_DATE>")
        edc = values.get("edc", "<EDC>")
        dx = values.get("dx", "<DIAGNOSIS>")
        approved = values.get("approved", None)
        pend = values.get("pend", None)

        if values.get("T1"):
            trimester = "first"
        elif values.get("T2"):
            trimester = "second"
        else:
            trimester = "third"

        try:
            dos_range = values.get("requested_dos", "<START_DOS>-<END_DOS>").split("-")
            start_dos, end_dos = dos_range[0], dos_range[1]
        except (AttributeError, ValueError, IndexError) as e:
            sg.popup(f"Error parsing Requested DOS field: {e}")
            start_dos = values.get("start_dos", "<START_DOS>")
            end_dos = values.get("end_dos", "<END_DOS>")

        # get pawf values
        try:
            fax = pawf_data.get("provider", {}).get("fax", "<FAX>")
            dob = pawf_data.get("client", {}).get("dob")
            age = calculate_age(dob) if dob else "<AGE>"
            rec_date = pawf_data.get("rec_date")
            month = rec_date.strftime("%B") if rec_date else "<MONTH>"
        except (AttributeError, KeyError) as e:
            sg.popup(f"Error: {e}")
            fax = "<FAX>"
            age = "<AGE>"
            month = "<MONTH>"

        add_on_codes = ["ADDONCODE"]
        npn_codes = ["NPNCODE", "NPNCODE"]

        comment = generate_blurb(
            portal,
            fax,
            mco_start_date,
            start_dos,
            end_dos,
            age,
            edc,
            dx,
            trimester,
            add_on_codes,
            npn_codes,
            approved,
            month,
        )

        pyperclip.copy(comment)
