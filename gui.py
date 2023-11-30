import PySimpleGUI as sg
from pawf import fetch_pawf_data

top_frame = [
    [
        sg.Text("PID: "),
        sg.InputText(size=(10, 20), key="portal_id"),
        sg.Button("go", key="go"),
    ],
    [sg.Text("PCN: "), sg.InputText(size=(12, 20), key="pcn")],
]
 #TODO Trimester radio field. 
mid_frame = [
    [sg.Text("MCO", key="MCO_TEXT"), sg.Push(), sg.Checkbox("", key="MCO")],
    [
        sg.Text("Start date:", key="mco_text"),
        sg.Push(),
        sg.InputText(key="mco_start_date", visible=False, size=(10)),
    ],
    [
        sg.Text("Intake Date:"),
        sg.Push(),
        sg.InputText(key="intake_date", size=(10)),
    ],
    [sg.Text("Age"), sg.Push(), sg.InputText(key="age", size=(3))],
    [
        sg.Radio("Child", "demographic", key="demographic", default=True),
        sg.Radio("Pregnant Woman", "demographic"),
    ],
    [sg.Text("Condition")],
    [sg.Multiline(default_text="", key="condition", size=(30, 4))],
]

bottom_frame = [
    [
        sg.Button("Copy"),
    ]
]

main_layout = [
    [sg.Frame("Automation", top_frame)],
    [sg.Frame("Request Information", mid_frame, expand_x=True)],
    [sg.Frame("Action", bottom_frame, expand_x=True)],
]

window = sg.Window("OB", main_layout, keep_on_top=True, finalize=True)

pawf_data = {}

while True:
    event, values = window.read(timeout=150)

    portal = values["portal_id"]

    if event == "go":
        try:
            pawf_data = fetch_pawf_data(portal)
        except Exception as e:
            sg.popup(str(e))
            continue

    # window.Element("pcn").Update(pawf_data.get("client").get("pcn"))

    if values["MCO"]:
        window["mco_text"].update(visible=True)
        window["mco_start_date"].update(visible=True)

    else:
        window["mco_text"].update(visible=False)
        window["mco_start_date"].update(visible=False)
        window["mco_start_date"].update(value="")
