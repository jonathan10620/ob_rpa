import PySimpleGUI as sg
import pyperclip

from pawf import fetch_pawf_data
import gui_helpers as gh
from tools import calculate_age, generate_blurb
from layout import main_layout
from selenium_actions import load_ticket_page

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

        # populate Requested DOS field
        gh.populate_requested_dos_field(window)

        # populate procedure field
        gh.populate_procedures_field(window)

        pan = pawf_data.get('pan')
        load_ticket_page(pan, portal)
        input('does it work?')



    if event == "copy":
        # Get gui values
        portal = values.get("portal_id", "<PORTAL_ID>")
        mco_start_date = values.get("mco_start_date", "<MCO_START_DATE>")
        edc = values.get("edc", "<EDC>")
        dx = values.get("dx", "<DIAGNOSIS>")
        approved = values.get('approved')
        pend = values.get('pend')

        if values.get("T1"):
            trimester = "first"
        elif values.get("T2"):
            trimester = "second"
        else:
            trimester = "third"

        try:
            start_dos, end_dos = values.get("requested_dos").split("-")
        except ValueError as e:
            sg.popup(f"Requested DOS field empty or incorrect. {e}")
            start_dos = "<START_DOS>"
            end_dos = "<END_DOS>"

        # get pawf values
        try:
            fax = pawf_data.get("provider").get("fax")
            age = calculate_age(pawf_data.get("client").get("dob"))
            month = pawf_data.get('rec_date').strftime('%B')
        except AttributeError as e:
            sg.popup(f"Error: {e}")
            fax = "<FAX>"
            age = "<AGE>"
        
        add_on_codes = ['ADDONCODE']
        npn_codes = ['NPNCODE', 'NPNCODE']
        

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
