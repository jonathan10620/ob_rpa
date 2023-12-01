from string import Template
from datetime import date

def calculate_age(born):
    """
    takes a datetime object and return age
    """
    today = date.today()
    return today.year - born.year - ((today.month, today.day)< (born.month, born.day))








BASE_COMMENT = "Portal ID: $portal. Fax #: $fax. Client is eligible.$mco_start_date Provider is eligible. \
Duplicates/history checked.  Submitter certification page submitted & completed. \
'Requested DOS: $start_dos-$end_dos. Client Age: $age. Estimate Date of Confinement: $edc. \
Client is in $trimester trimester with diagnosis: $dx. Request is medically necessary for \
$trimester trimester per policy: Screening for fetal anomolies. $add_on_code$npn_blurb "

base_template = Template(BASE_COMMENT)


def generate_blurb(portal, fax, mco_start_date, start_dos, end_dos, age, edc, trimester, dx,add_on, npn_codes, approved, month):
    if mco_start_date:
        # TODO: handle if mco_start_date exists
        mco_blurb = f" Please note, the client will be enrolled in a Managed Care Organization effective: {mco_start_date}"
    else:
        mco_blurb = ''

    if add_on:
        add_on_blurb = f'Procedure code, {str(add_on)}, is an add-on code and will not be reimbursed separately from the primary procedure code.'
    else:
        add_on_blurb = ''
    
    if npn_codes:
        npn_blurb = f' No prior authorization is required for the requested items/services, {str(npn_codes)}, when properly billed.'
    else:
        npn_blurb = ''

    data = {'portal' : portal,
            'fax': fax,
            'mco_start_date': mco_blurb,
            'start_dos': start_dos,
            'end_dos': end_dos,
            'age': age,
            'edc': edc,
            'trimester': trimester,
            'add_on_code': add_on_blurb,
            'npn_blurb': npn_blurb

            }
    template = base_template.substitute(data)

    if approved:
        template += f'Request approved based on Texas Medicaid Medical Policy Manual— {month}, 2023 Obstetrics Services. SOP 119 J. Delapaz RN.'
    else:
        template += f'Based on Texas Medicaid Medical Policy Manual— {month}, 2023 Obstetrics Services, TMHP is pending your submission for the following reasons: ______ SOP 119 J. Delapaz RN.'

    return template