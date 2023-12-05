import PySimpleGUI as sg

sg.theme('DarkBlue8')
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
    [
        sg.Text("MCO", key="MCO_TEXT"),
        sg.Checkbox("", key="MCO"),
        sg.Text("Start date:", key="mco_text"),
        sg.InputText(key="mco_start_date", visible=False, size=(10)),
    ],
    [
        sg.Text("Requested DOS:"),
        sg.InputText(key="requested_dos", size=(19)),
    ],
    [sg.Text("EDC"), sg.InputText(key="edc", size=(9))],
    [
        sg.Radio("First", "trimester", key="T1", default=True),
        sg.Radio("Second", "trimester", key="T2"),
        sg.Radio("Third", "trimester", key="T3"),
    ],
    [
        sg.Text("Procedure Codes"),
        sg.Multiline(default_text="", key="procedure_codes", size=(10, 4)),
    ],
    [sg.Text("Diagnosis"), sg.Multiline(default_text="", key="dx", size=(10, 4))],
    [
        sg.Radio("Approved", "decision", key="approved", default=True),
        sg.Radio("Pend", "decision", key="pend"),
    ],
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
