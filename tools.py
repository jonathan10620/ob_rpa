from string import Template

def calculate_age(age_string):
    """
    takes a datetime object and return age
    """
    pass








BASE_COMMENT = "Portal ID: $portal. Fax #: $fax. Client is eligible. Provider is eligible. \
Duplicates/history checked.  Submitter certification page submitted & completed. \
'Requested DOS: $start_dos-$end_dos."

base_template = Template(BASE_COMMENT)

def generate_blurb(portal, fax, mco_start_date, start_dos, end_dos):
    if mco_start_date:
        # TODO: handle if mco_start_date exists
        pass


    data = {'portal' : portal,
            'fax': fax,
            'mco_start_date': mco_start_date,
            'start_dos': start_dos,
            'end_dos': end_dos
            }
    
    return base_template.substitute(data)