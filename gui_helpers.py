import selenium_actions as sel
import PySimpleGUI as sg

def update_gui_field(window, field_key, value):
    try:
        window.Element(field_key).Update(value)
    except Exception as e:
        sg.popup(f'Error updating field {field_key} with value {value}. Exception: {e}')

def populate_procedures_field(window):
    # TODO: populates fetched proc codes into gui_field
    procedure_codes = '\n'.join(sel.fetch_procedure_codes())
    try:
        update_gui_field(window, 'procedure_codes', procedure_codes)
    except ValueError as e:
        sg.popup(f'Error: {e}.')

def popup(s):
    sg.popup(f'Error: {s}')

def populate_requested_dos_field(window):
    requested_dos = sel.fetch_requested_dos()
    try:
        update_gui_field(window, 'requested_dos', requested_dos)
    except ValueError as e:
        sg.popup(f'Error: {e}.')




def display_mco_field(window, values):
    if values["MCO"]:
        window["mco_text"].update(visible=True)
        window["mco_start_date"].update(visible=True)
    else:
        window["mco_text"].update(visible=False)
        window["mco_start_date"].update(visible=False)
        window["mco_start_date"].update(value="")