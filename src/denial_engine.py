from datetime import datetime

from src.utils import get_filing_limit


CARC_MAPPING = {
    "16": "Missing Information",
    "18": "Duplicate Claim",
    "29": "Timely Filing",
    "50": "Medical Necessity",
    "97": "Bundled Service",
    "197": "Missing Prior Authorization",
    "252": "Missing Documentation"
}


def analyze_claim(row):

    carc = str(
    row["pcla_AdjustmentReason"]
).strip()

    claim_status = str(row["pc_ClaimStatus"])

    result = {

        "claim_id": row["pc_ClaimID"],

        "carc_reason": CARC_MAPPING.get(
            carc,
            "Unknown"
        ),

        "root_cause": "",

        "recoverability": "",

        "confidence": 0.0,

        "evidence": []
    }

    # ------------------------------------------------
    # PAID CLAIM
    # ------------------------------------------------

    if claim_status == "1":

        result["root_cause"] = (
            "Claim processed successfully"
        )

        result["recoverability"] = (
            "Not Applicable"
        )

        result["confidence"] = 1.0

        result["evidence"] = [

            f"Paid Amount: {row['pc_ClaimPaid']}"
        ]

        return result

    # ------------------------------------------------
    # TIMELY FILING
    # ------------------------------------------------

    if "29" in carc:

        service_date = datetime.strptime(

            row["ec_ServiceDateFrom"],

            "%Y-%m-%d"
        )

        received_date = datetime.strptime(

            row["pc_ReceivedDate"],

            "%Y-%m-%d"
        )

        days_difference = (
            received_date - service_date
        ).days

        filing_limit = get_filing_limit(

            row["ec_InsuranceType"]
        )

        if days_difference > filing_limit:

            result["root_cause"] = (
                "Claim submitted after filing deadline"
            )

            result["recoverability"] = (
                "Not Recoverable"
            )

            result["confidence"] = 0.95

        else:

            result["root_cause"] = (
                "Possible incorrect timely filing denial"
            )

            result["recoverability"] = (
                "Recoverable"
            )

            result["confidence"] = 0.70

        result["evidence"] = [

            f"Service Date: {row['ec_ServiceDateFrom']}",

            f"Received Date: {row['pc_ReceivedDate']}",

            f"Days Difference: {days_difference}",

            f"Insurance Type: {row['ec_InsuranceType']}"
        ]

    # ------------------------------------------------
    # MISSING INFORMATION
    # ------------------------------------------------

    elif "16" in carc:

        modifier = str(

            row.get(
                "pcl_ProcedureModifier1",
                ""
            )
        )

        if modifier == "" or modifier == "nan":

            result["root_cause"] = (
                "Required procedure modifier missing"
            )

            result["recoverability"] = (
                "Recoverable"
            )

            result["confidence"] = 0.90

        result["evidence"] = [

            f"Procedure Code: {row['pcl_ProcedureCode']}",

            f"Remark Code: {row.get('pcl_RemarkCodes')}"
        ]

    # ------------------------------------------------
    # MEDICAL NECESSITY
    # ------------------------------------------------

    elif "50" in carc:

        prior_auth = str(

            row.get(
                "ec_PriorAuthorization",
                ""
            )
        )

        if prior_auth == "" or prior_auth == "nan":

            result["root_cause"] = (
                "Missing prior authorization"
            )

            result["recoverability"] = (
                "Needs Review"
            )

            result["confidence"] = 0.80

        else:

            result["root_cause"] = (
                "Medical necessity denial"
            )

            result["recoverability"] = (
                "Needs Review"
            )

            result["confidence"] = 0.70

        result["evidence"] = [

            f"Procedure Code: {row['pcl_ProcedureCode']}",

            f"Diagnosis: {row['ec_PrincipalDiagnosis']}"
        ]

    # ------------------------------------------------
    # DUPLICATE CLAIM
    # ------------------------------------------------

    elif "18" in carc:

        result["root_cause"] = (
            "Duplicate claim submission"
        )

        result["recoverability"] = (
            "Not Recoverable"
        )

        result["confidence"] = 0.98

        result["evidence"] = [

            "Duplicate CARC denial detected"
        ]

    # ------------------------------------------------
    # UNKNOWN
    # ------------------------------------------------

    else:

        result["root_cause"] = (
            "Unknown denial reason"
        )

        result["recoverability"] = (
            "Needs Review"
        )

        result["confidence"] = 0.50

        result["evidence"] = [

            "Manual review required"
        ]

    return result