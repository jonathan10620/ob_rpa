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

main_layout = [[sg.Frame('Automation', top_frame)]]

window = sg.Window("OB", main_layout, keep_on_top=True, finalize=True)

pawf_data = {}

while True:
    event,values = window.read()

    portal = values["portal_id"]

    if event == 'go':
        try:
            pawf_data = fetch_pawf_data(portal)
        except Exception as e:
            sg.popup(str(e))
            continue
    window.Element('pcn').Update(pawf_data.get('client').get('pcn'))

750071766