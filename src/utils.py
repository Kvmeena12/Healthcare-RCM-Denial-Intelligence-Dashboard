import json

PAYER_LIMITS = {

    "Commercial": 180,

    "Medicare": 365,

    "Medicaid": 180
}

def get_filing_limit(insurance_type):

    return PAYER_LIMITS.get(
        insurance_type,
        180
    )

def pretty_print_json(data):

    return json.dumps(
        data,
        indent=4
    )