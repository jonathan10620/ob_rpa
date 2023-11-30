import PySimpleGUI as sg
import pyperclip


from pawf import fetch_pawf_data
import gui_helpers as gh
from tools import calculate_age, generate_blurb


top_frame = [
    [
        sg.Text("PID: "),
        sg.InputText(size=(10, 20), key="portal_id"),
        sg.Button("go", key="go"),
    ],
    [sg.Text("PCN: "), sg.InputText(size=(12, 20), key="pcn")],
]

# TODO Trimester radio field.
mid_frame = [
    [sg.Text("MCO", key="MCO_TEXT"), sg.Checkbox("", key="MCO")],
    [
        sg.Text("Start date:", key="mco_text"),
        sg.InputText(key="mco_start_date", visible=False, size=(10)),
    ],
    [
        sg.Text("Requested DOS:"),
        sg.InputText(key="requested_dos", size=(30)),
    ],
    [sg.Text("Age"), sg.InputText(key="age", size=(3))],
    [
        sg.Radio("Child", "demographic", key="demographic", default=True),
        sg.Radio("Pregnant Woman", "demographic"),
    ],
    [sg.Text("Condition")],
    [sg.Multiline(default_text="", key="condition", size=(30, 4))],
]

bottom_frame = [
    [
        sg.Button("copy"),
    ]
]

main_layout = [
    [sg.Frame("Automation", top_frame)],
    [sg.Frame("Request Information", mid_frame)],
    [sg.Frame("Action", bottom_frame)],
]

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
        pcn = pawf_data.get('client').get('pcn')
        gh.update_gui_field(window, 'pcn', pcn)

        # populate Requested DOS field
        gh.populate_requested_dos_field()
        
        # populate procedure field
        gh.populate_procedures_field(window)

    if event == "copy":
        # Get gui values
        portal = values.get('portal_id')
        mco_start_date = values.get('mco_start_date', None)
        try:
            start_dos, end_dos = values.get('requested_dos').split('-')
        except ValueError as e:
            sg.popup(f'Requested DOS field empty or incorrect. {e}')
            start_dos = '<START_DOS>'
            end_dos = '<END_DOS>'

        # get pawf values
        try:
            fax = pawf_data.get('provider').get('fax')
            age = calculate_age(pawf_data.get('client').get('dob'))
        except AttributeError as e:
            sg.popup(f'Error: {e}')
            fax = '<FAX>'
            age = '<AGE>'

        comment = generate_blurb(portal, fax, mco_start_date, start_dos, end_dos)

        pyperclip.copy(comment)
