import sqlite3

from flask import Blueprint, render_template, request

from database import save_prediction
from prediction_service import predict_loan_application
from utils import (
    parse_positive_number,
    validate_required_fields
)


prediction_bp = Blueprint(
    "prediction",
    __name__
)


@prediction_bp.route(
    "/predict",
    methods=["POST"]
)
def predict():
    """
    Validate form data, generate a loan prediction,
    save it to the database, and display the result.
    """

    try:
        # ------------------------------------------
        # Read form values
        # ------------------------------------------

        gender_value = request.form.get("Gender")
        married_value = request.form.get("Married")
        dependents_value = request.form.get("Dependents")
        education_value = request.form.get("Education")
        self_employed_value = request.form.get(
            "Self_Employed"
        )

        applicant_income_value = request.form.get(
            "ApplicantIncome"
        )

        coapplicant_income_value = request.form.get(
            "CoapplicantIncome"
        )

        loan_amount_value = request.form.get(
            "LoanAmount"
        )

        loan_term_value = request.form.get(
            "Loan_Amount_Term"
        )

        credit_history_value = request.form.get(
            "Credit_History"
        )

        property_area_value = request.form.get(
            "Property_Area"
        )

        consent_value = request.form.get("consent")

        # ------------------------------------------
        # Required-field validation
        # ------------------------------------------

        validate_required_fields({
            "Gender": gender_value,
            "Marital status": married_value,
            "Dependents": dependents_value,
            "Education": education_value,
            "Employment type": self_employed_value,
            "Applicant income": applicant_income_value,
            "Co-applicant income": coapplicant_income_value,
            "Loan amount": loan_amount_value,
            "Loan term": loan_term_value,
            "Credit history": credit_history_value,
            "Property area": property_area_value
        })

        if consent_value != "on":
            raise ValueError(
                "Please confirm that the provided "
                "information is accurate."
            )

        # ------------------------------------------
        # Training-time categorical mappings
        # ------------------------------------------

        gender_mapping = {
            "Female": 0,
            "Male": 1
        }

        married_mapping = {
            "No": 0,
            "Yes": 1
        }

        dependents_mapping = {
            "0": 0,
            "1": 1,
            "2": 2,
            "3+": 3
        }

        education_mapping = {
            "Graduate": 0,
            "Not Graduate": 1
        }

        self_employed_mapping = {
            "No": 0,
            "Yes": 1
        }

        property_area_mapping = {
            "Rural": 0,
            "Semiurban": 1,
            "Urban": 2
        }

        # ------------------------------------------
        # Convert categorical values
        # ------------------------------------------

        gender = gender_mapping[gender_value]
        married = married_mapping[married_value]

        dependents = dependents_mapping[
            dependents_value
        ]

        education = education_mapping[
            education_value
        ]

        self_employed = self_employed_mapping[
            self_employed_value
        ]

        property_area = property_area_mapping[
            property_area_value
        ]

        # ------------------------------------------
        # Validate numerical values
        # ------------------------------------------

        applicant_income = parse_positive_number(
            applicant_income_value,
            "Applicant income"
        )

        coapplicant_income = parse_positive_number(
            coapplicant_income_value,
            "Co-applicant income",
            allow_zero=True
        )

        loan_amount_rupees = parse_positive_number(
            loan_amount_value,
            "Loan amount"
        )

        if loan_amount_rupees < 1000:
            raise ValueError(
                "Loan amount must be at least ₹1,000."
            )

        # Dataset stores LoanAmount in ₹1,000 units.
        loan_amount_for_model = (
            loan_amount_rupees / 1000
        )

        loan_amount_term = parse_positive_number(
            loan_term_value,
            "Loan term"
        )

        try:
            credit_history = float(
                credit_history_value
            )

        except (TypeError, ValueError):
            raise ValueError(
                "Credit history must be a valid selection."
            )

        if credit_history not in (0.0, 1.0):
            raise ValueError(
                "Credit history must be either 0 or 1."
            )

        # ------------------------------------------
        # ML prediction service
        # ------------------------------------------

        result = predict_loan_application(
    gender=gender,
    married=married,
    dependents=dependents,
    education=education,
    self_employed=self_employed,
    applicant_income=applicant_income,
    coapplicant_income=coapplicant_income,
    loan_amount=loan_amount_for_model,
    loan_term=loan_amount_term,
    credit_history=credit_history,
    property_area=property_area
)

        # ------------------------------------------
        # Save prediction to SQLite
        # ------------------------------------------

        save_prediction(
            gender=gender_value,
            married=married_value,
            dependents=dependents_value,
            education=education_value,
            self_employed=self_employed_value,
            applicant_income=applicant_income,
            coapplicant_income=coapplicant_income,
            loan_amount=loan_amount_rupees,
            loan_term=loan_amount_term,
            credit_history=credit_history,
            property_area=property_area_value,
            prediction=result["prediction_text"],
            confidence=result["confidence"],
            risk_level=result["risk_level"]
        )

        total_income = (
            applicant_income + coapplicant_income
        )

        # ------------------------------------------
        # Display prediction result
        # ------------------------------------------

        return render_template(
            "index.html",
            prediction_text=result[
                "prediction_text"
            ],
            prediction_status=result[
                "prediction_status"
            ],
            confidence_score=result[
                "confidence"
            ],
            risk_level=result[
                "risk_level"
            ],
            applicant_income=applicant_income,
            coapplicant_income=coapplicant_income,
            total_income=total_income,
            loan_amount=loan_amount_rupees,
            loan_term=loan_amount_term,
            credit_history=credit_history_value,
            property_area=property_area_value,
            ai_reasons=result["reasons"]
        )

    except ValueError as error:
        return render_template(
            "index.html",
            error_message=str(error)
        )

    except KeyError as error:
        print(
            f"Invalid mapping value: {error}"
        )

        return render_template(
            "index.html",
            error_message=(
                "One of the selected values is invalid. "
                "Please refresh the page and try again."
            )
        )

    except sqlite3.Error as error:
        print(
            f"Database error: {error}"
        )

        return render_template(
            "index.html",
            error_message=(
                "Prediction was created, but it could "
                "not be saved in the database."
            )
        )

    except Exception as error:
        print(
            f"Prediction error: {error}"
        )

        return render_template(
            "index.html",
            error_message=(
                "Prediction failed. Please check the "
                "entered values and try again."
            )
        )