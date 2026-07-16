from flask import Flask, render_template, request
import os
import pickle
import sqlite3

import pandas as pd


app = Flask(__name__)


# --------------------------------------------------
# Load trained machine-learning model
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "loan_model.pkl")

with open(MODEL_PATH, "rb") as model_file:
    model = pickle.load(model_file)


# Model input columns in exact training order
MODEL_FEATURES = [
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
# --------------------------------------------------
# SQLite Database Initialization
# --------------------------------------------------

def initialize_database():

    database_path = os.path.join(BASE_DIR, "predictions.db")
    connection = sqlite3.connect(database_path)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            gender TEXT,

            married TEXT,

            dependents TEXT,

            education TEXT,

            self_employed TEXT,

            applicant_income REAL,

            coapplicant_income REAL,

            loan_amount REAL,

            loan_term REAL,

            credit_history REAL,

            property_area TEXT,

            prediction TEXT,

            confidence REAL,

            risk_level TEXT
        )
    """)

    connection.commit()

    connection.close()


# --------------------------------------------------
# Numeric validation helper
# --------------------------------------------------

def parse_positive_number(value, field_name, allow_zero=False):
    """
    Convert a form value into float and validate it.

    allow_zero=False:
        Number must be greater than zero.

    allow_zero=True:
        Number may be zero but cannot be negative.
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


# --------------------------------------------------
# Home route
# --------------------------------------------------

@app.route("/")
def home():
    return render_template("index.html")


# --------------------------------------------------
# Prediction route
# --------------------------------------------------

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # ------------------------------------------
        # Read form values
        # ------------------------------------------

        gender_value = request.form.get("Gender")
        married_value = request.form.get("Married")
        dependents_value = request.form.get("Dependents")
        education_value = request.form.get("Education")
        self_employed_value = request.form.get("Self_Employed")

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

        required_fields = {
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
        }

        missing_fields = [
            field_name
            for field_name, field_value in required_fields.items()
            if field_value is None
            or str(field_value).strip() == ""
        ]

        if missing_fields:
            raise ValueError(
                "Please fill all required fields: "
                + ", ".join(missing_fields)
            )

        if consent_value != "on":
            raise ValueError(
                "Please confirm that the provided information "
                "is accurate."
            )

        # ------------------------------------------
        # Categorical mappings
        # Must match training-time encoding
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
        dependents = dependents_mapping[dependents_value]
        education = education_mapping[education_value]

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
        # Example: ₹150,000 becomes 150 for model input.
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
        # Create model input
        # ------------------------------------------

        input_data = pd.DataFrame(
            [[
                gender,
                married,
                dependents,
                education,
                self_employed,
                applicant_income,
                coapplicant_income,
                loan_amount_for_model,
                loan_amount_term,
                credit_history,
                property_area
            ]],
            columns=MODEL_FEATURES
        )

        # ------------------------------------------
        # Make prediction
        # ------------------------------------------

        prediction = model.predict(input_data)
        prediction_value = int(prediction[0])

        # ------------------------------------------
        # Calculate model confidence
        # ------------------------------------------

        confidence_score = None

        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(
                input_data
            )[0]

            model_classes = list(model.classes_)

            predicted_class_index = (
                model_classes.index(prediction_value)
            )

            confidence_score = round(
                float(
                    probabilities[
                        predicted_class_index
                    ]
                ) * 100,
                2
            )

        # ------------------------------------------
        # Prepare dynamic explanation
        # ------------------------------------------

        total_income = (
            applicant_income + coapplicant_income
        )

        ai_reasons = []

        if prediction_value == 1:
            prediction_text = (
                "Loan Application Likely to Be Approved"
            )

            prediction_status = "approved"

            if (
                confidence_score is not None
                and confidence_score >= 80
            ):
                risk_level = "Low"
            else:
                risk_level = "Medium"

            if credit_history == 1:
                ai_reasons.append(
                    "Excellent credit history improves "
                    "approval chances."
                )

            if total_income >= 50000:
                ai_reasons.append(
                    "Strong combined income supports "
                    "repayment capacity."
                )

            elif total_income >= 25000:
                ai_reasons.append(
                    "Income profile is adequate for "
                    "the requested loan."
                )

            else:
                ai_reasons.append(
                    "Income is lower, but the complete "
                    "profile still matches approval patterns."
                )

            if loan_amount_rupees <= 300000:
                ai_reasons.append(
                    "Requested loan amount is within "
                    "a comfortable range."
                )

            elif loan_amount_rupees <= 500000:
                ai_reasons.append(
                    "Loan amount is moderate relative "
                    "to the applicant profile."
                )

            else:
                ai_reasons.append(
                    "Loan amount is comparatively high "
                    "and may require stronger repayment capacity."
                )

            if education == 0:
                ai_reasons.append(
                    "Graduate education strengthens "
                    "the applicant profile."
                )

            if self_employed == 0:
                ai_reasons.append(
                    "Salaried or non-self-employed status "
                    "may improve financial stability."
                )

            else:
                ai_reasons.append(
                    "Self-employment is accepted, but income "
                    "consistency remains important."
                )

            if len(ai_reasons) < 4:
                ai_reasons.append(
                    "Overall applicant profile matches "
                    "the model's approval pattern."
                )

        else:
            prediction_text = (
                "Loan Application May Not Be Approved"
            )

            prediction_status = "rejected"

            if (
                confidence_score is not None
                and confidence_score >= 80
            ):
                risk_level = "High"
            else:
                risk_level = "Medium"

            if credit_history == 0:
                ai_reasons.append(
                    "Poor or unavailable credit history "
                    "reduces approval probability."
                )

            else:
                ai_reasons.append(
                    "Credit history is positive, but other "
                    "financial factors may be limiting approval."
                )

            if total_income < 25000:
                ai_reasons.append(
                    "Combined applicant income is "
                    "comparatively low."
                )

            elif total_income < 50000:
                ai_reasons.append(
                    "Income may be insufficient for the "
                    "requested loan amount."
                )

            else:
                ai_reasons.append(
                    "Income is relatively strong, but the "
                    "overall profile still has risk factors."
                )

            if loan_amount_rupees > 500000:
                ai_reasons.append(
                    "Requested loan amount is comparatively high."
                )

            elif loan_amount_rupees > 300000:
                ai_reasons.append(
                    "Loan amount may be high relative "
                    "to the applicant profile."
                )

            else:
                ai_reasons.append(
                    "Loan amount is moderate, but other "
                    "profile factors affect approval."
                )

            if education == 1:
                ai_reasons.append(
                    "Education profile may slightly affect "
                    "the model's decision."
                )

            if self_employed == 1:
                ai_reasons.append(
                    "Self-employment income may require "
                    "additional verification."
                )

            if len(ai_reasons) < 4:
                ai_reasons.append(
                    "Overall profile requires improvement "
                    "for better approval chances."
                )

        # Limit dashboard reasons to maximum 5
        ai_reasons = ai_reasons[:5]

        # ------------------------------------------
        # Save prediction into SQLite database
        # ------------------------------------------

        database_path = os.path.join(
            BASE_DIR,
            "predictions.db"
        )

        connection = sqlite3.connect(database_path)

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO predictions (
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
                    property_area,
                    prediction,
                    confidence,
                    risk_level
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    gender_value,
                    married_value,
                    dependents_value,
                    education_value,
                    self_employed_value,
                    applicant_income,
                    coapplicant_income,
                    loan_amount_rupees,
                    loan_amount_term,
                    credit_history,
                    property_area_value,
                    prediction_text,
                    confidence_score,
                    risk_level
                )
            )

            connection.commit()

        finally:
            connection.close()

        # ------------------------------------------
        # Render prediction dashboard
        # ------------------------------------------

        return render_template(
            "index.html",
            prediction_text=prediction_text,
            prediction_status=prediction_status,
            confidence_score=confidence_score,
            risk_level=risk_level,
            applicant_income=applicant_income,
            coapplicant_income=coapplicant_income,
            total_income=total_income,
            loan_amount=loan_amount_rupees,
            loan_term=loan_amount_term,
            credit_history=credit_history_value,
            property_area=property_area_value,
            ai_reasons=ai_reasons
        )

    except ValueError as error:
        return render_template(
            "index.html",
            error_message=str(error)
        )

    except KeyError as error:
        print(f"Invalid mapping value: {error}")

        return render_template(
            "index.html",
            error_message=(
                "One of the selected values is invalid. "
                "Please refresh the page and try again."
            )
        )

    except sqlite3.Error as error:
        print(f"Database error: {error}")

        return render_template(
            "index.html",
            error_message=(
                "Prediction was created, but it could not be "
                "saved in the database."
            )
        )

    except Exception as error:
        print(f"Prediction error: {error}")

        return render_template(
            "index.html",
            error_message=(
                "Prediction failed. Please check the entered "
                "values and try again."
            )
        )
# --------------------------------------------------
# Prediction History Route
# --------------------------------------------------

@app.route("/history")
def history():
    database_path = os.path.join(
        BASE_DIR,
        "predictions.db"
    )

    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row

    try:
        predictions = connection.execute(
            """
            SELECT *
            FROM predictions
            ORDER BY prediction_date DESC
            """
        ).fetchall()

        total_predictions = connection.execute(
            """
            SELECT COUNT(*)
            FROM predictions
            """
        ).fetchone()[0]

        approved_predictions = connection.execute(
            """
            SELECT COUNT(*)
            FROM predictions
            WHERE prediction LIKE '%Approved%'
            """
        ).fetchone()[0]

        rejected_predictions = connection.execute(
            """
            SELECT COUNT(*)
            FROM predictions
            WHERE prediction LIKE '%Not Be Approved%'
            """
        ).fetchone()[0]

        average_confidence = connection.execute(
            """
            SELECT AVG(confidence)
            FROM predictions
            WHERE confidence IS NOT NULL
            """
        ).fetchone()[0]

    finally:
        connection.close()

    if average_confidence is None:
        average_confidence = 0

    average_confidence = round(
        float(average_confidence),
        2
    )

    return render_template(
        "history.html",
        predictions=predictions,
        total_predictions=total_predictions,
        approved_predictions=approved_predictions,
        rejected_predictions=rejected_predictions,
        average_confidence=average_confidence
    )

    # --------------------------------------------------
# Start Flask application
# --------------------------------------------------

if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)