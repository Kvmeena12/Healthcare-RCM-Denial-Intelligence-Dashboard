from faker import Faker
import pandas as pd
import random

fake = Faker()

claims_835 = []
claims_837 = []

carc_codes = ["16", "18", "29", "50"]

payers = [
    "Aetna",
    "Blue Cross",
    "Medicare",
    "United Healthcare"
]

procedures = [
    "99213",
    "72148",
    "27447"
]

diagnosis_codes = [
    "J06.9",
    "M54.5",
    "M17.11"
]

for i in range(30):

    claim_id = f"CLM-{1000+i}"

    denial = random.choice([True, False])

    if denial:
        paid_amount = 0
        carc = str(
        random.choice(carc_codes))
        status = "4"
    else:
        paid_amount = random.randint(500, 8000)
        carc = "PAID"
        status = "1"

    claim_amount = random.randint(1000, 15000)

    payer = random.choice(payers)

    procedure = random.choice(procedures)

    diagnosis = random.choice(diagnosis_codes)

    # ---------------- 835 DATA ----------------

    claims_835.append({

        "pc_ClaimID": claim_id,

        "pc_ClaimStatus": status,

        "pc_ClaimAmount": claim_amount,

        "pc_ClaimPaid": paid_amount,

        "pc_InsuranceType": "Commercial",

        "pc_ReceivedDate": "2026-03-20",

        "pcla_AdjustmentReason": carc,

        "pcl_ProcedureCode": procedure,

        "pcl_ProcedureModifier1": "",

        "pcl_RemarkCodes": "N20"
    })

    # ---------------- 837 DATA ----------------

    claims_837.append({

        "ec_ClaimNo": claim_id,

        "ec_PayerName": payer,

        "ec_InsuranceType": "Commercial",

        "ec_ServiceDateFrom": "2025-06-15",

        "ec_PrincipalDiagnosis": diagnosis,

        "ec_PriorAuthorization": "",

        "ec_ClaimFrequency": "1"
    })

# ---------------- SAVE CSV ----------------

df835 = pd.DataFrame(claims_835)

df837 = pd.DataFrame(claims_837)

df835.to_csv(
    "data/835_claims.csv",
    index=False
)

df837.to_csv(
    "data/837_claims.csv",
    index=False
)

print("Synthetic datasets created successfully")