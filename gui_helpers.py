import selenium_actions as sel


def display_mco_field(window, values):
    if values["MCO"]:
        window["mco_text"].update(visible=True)
        window["mco_start_date"].update(visible=True)
    else:
        window["mco_text"].update(visible=False)
        window["mco_start_date"].update(visible=False)
        window["mco_start_date"].update(value="")




def populate_procedures_field(window):
    # TODO: populates fetched proc codes into gui_field
    procedure_codes = sel.get_procedure_codes()

    pass

def populate_requested_dos_field():
    requested_dos = sel.grab_requested_dos





def update_gui_field(window, field_key, value):
    try:
        window.Element(field_key).Update(value)
    except Exception as e:
        raise ValueError(f'Error updating field {field_key} with value {value}')
    
