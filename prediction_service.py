import pickle

import pandas as pd

from config import MODEL_PATH
from utils import (
    calculate_confidence,
    calculate_risk_level,
    build_prediction_reasons
)


with open(MODEL_PATH, "rb") as model_file:
    model = pickle.load(model_file)


FEATURE_COLUMNS = [
    "Gender",
    "Married",
    "Dependents",
    "Education",
    "Self_Employed",
    "ApplicantIncome",
    "CoapplicantIncome",
    "LoanAmount",
    "Loan_Amount_Term",
    "Credit_History",
    "Property_Area"
]


def predict_loan_application(
    gender,
    married,
    dependents,
    education,
    self_employed,
    applicant_income,
    coapplicant_income,
    loan_amount,
    loan_term,
    credit_history,
    property_area
):
    """
    Run the trained model and return prediction details.
    """

    input_dataframe = pd.DataFrame(
        [[
            gender,
            married,
            dependents,
            education,
            self_employed,
            applicant_income,
            coapplicant_income,
            loan_amount,
            loan_term,
            credit_history,
            property_area
        ]],
        columns=FEATURE_COLUMNS
    )

    prediction_value = int(
        model.predict(input_dataframe)[0]
    )

    confidence = calculate_confidence(
        model,
        input_dataframe
    )

    if prediction_value == 1:
        prediction_text = "Loan Approved"
        prediction_status = "approved"
    else:
        prediction_text = "Loan Rejected"
        prediction_status = "rejected"

    risk_level = calculate_risk_level(
        prediction_value,
        confidence
    )

    reasons = build_prediction_reasons(
        prediction_value,
        applicant_income,
        coapplicant_income,
        loan_amount,
        credit_history
    )

    return {
        "prediction_value": prediction_value,
        "prediction_text": prediction_text,
        "prediction_status": prediction_status,
        "confidence": confidence,
        "risk_level": risk_level,
        "reasons": reasons
    }