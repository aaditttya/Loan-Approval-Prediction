def parse_positive_number(
    value,
    field_name,
    allow_zero=False
):
    """
    Convert form value into float and validate it.
    """

    try:
        number = float(value)

    except (TypeError, ValueError):
        raise ValueError(
            f"{field_name} must be a valid number."
        )

    if allow_zero:
        if number < 0:
            raise ValueError(
                f"{field_name} cannot be negative."
            )

    else:
        if number <= 0:
            raise ValueError(
                f"{field_name} must be greater than zero."
            )

    return number


def validate_required_fields(required_fields):
    """
    Check whether all required fields contain values.
    """

    missing_fields = [
        field_name
        for field_name, field_value
        in required_fields.items()
        if field_value is None
        or str(field_value).strip() == ""
    ]

    if missing_fields:
        raise ValueError(
            "Please fill all required fields: "
            + ", ".join(missing_fields)
        )


def calculate_confidence(model, input_dataframe):
    """
    Calculate prediction confidence percentage.
    """

    if not hasattr(model, "predict_proba"):
        return 100.0

    probabilities = model.predict_proba(
        input_dataframe
    )[0]

    confidence = max(probabilities) * 100

    return round(float(confidence), 2)


def calculate_risk_level(
    prediction_value,
    confidence
):
    """
    Determine risk level using prediction and confidence.
    """

    if prediction_value == 1:

        if confidence >= 80:
            return "Low"

        if confidence >= 60:
            return "Medium"

        return "High"

    if confidence >= 80:
        return "High"

    if confidence >= 60:
        return "Medium"

    return "High"


def build_prediction_reasons(
    prediction_value,
    applicant_income,
    coapplicant_income,
    loan_amount,
    credit_history
):
    """
    Generate simple explainable prediction reasons.
    """

    reasons = []

    total_income = (
        applicant_income
        + coapplicant_income
    )

    if credit_history == 1:
        reasons.append(
            "Positive credit history supports approval."
        )
    else:
        reasons.append(
            "Poor or missing credit history increases risk."
        )

    if total_income >= loan_amount:
        reasons.append(
            "Combined income is strong compared with the loan amount."
        )
    else:
        reasons.append(
            "Requested loan amount is high compared with income."
        )

    if applicant_income >= 5000:
        reasons.append(
            "Applicant income indicates good repayment capacity."
        )
    else:
        reasons.append(
            "Applicant income may limit repayment capacity."
        )

    if prediction_value == 1:
        reasons.append(
            "The overall applicant profile matches approved cases."
        )
    else:
        reasons.append(
            "The overall applicant profile shows higher lending risk."
        )

    return reasons