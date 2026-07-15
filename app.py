from flask import Flask, render_template, request
import pickle
import numpy as np
import os


app = Flask(__name__)


# Get the folder where app.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Create full model path
MODEL_PATH = os.path.join(BASE_DIR, "loan_model.pkl")


# Load trained machine-learning model
with open(MODEL_PATH, "rb") as model_file:
    model = pickle.load(model_file)


def parse_positive_number(value, field_name, allow_zero=False):
    """
    Convert a form value into a number and validate it.

    allow_zero=False:
        Number must be greater than zero.

    allow_zero=True:
        Number may be zero, but cannot be negative.
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


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        # ---------------------------------
        # Get categorical values from form
        # ---------------------------------

        gender_value = request.form.get("Gender")
        married_value = request.form.get("Married")
        dependents_value = request.form.get("Dependents")
        education_value = request.form.get("Education")
        self_employed_value = request.form.get("Self_Employed")
        property_area_value = request.form.get("Property_Area")
        loan_term_value = request.form.get("Loan_Amount_Term")
        credit_history_value = request.form.get("Credit_History")
        consent_value = request.form.get("consent")

        # ---------------------------------
        # Required-field backend validation
        # ---------------------------------

        required_fields = {
            "Gender": gender_value,
            "Marital status": married_value,
            "Dependents": dependents_value,
            "Education": education_value,
            "Employment type": self_employed_value,
            "Property area": property_area_value,
            "Applicant income": request.form.get("ApplicantIncome"),
            "Co-applicant income": request.form.get("CoapplicantIncome"),
            "Loan amount": request.form.get("LoanAmount"),
            "Loan term": loan_term_value,
            "Credit history": credit_history_value
        }

        missing_fields = [
            field_name
            for field_name, field_value in required_fields.items()
            if field_value is None or str(field_value).strip() == ""
        ]

        if missing_fields:
            raise ValueError(
                "Please fill all required fields: "
                + ", ".join(missing_fields)
            )

        if consent_value != "on":
            raise ValueError(
                "Please confirm that the provided information is accurate."
            )

        # ---------------------------------
        # Categorical mappings
        # ---------------------------------

        gender_mapping = {
            "Female": 0,
            "Male": 1
        }

        married_mapping = {
            "No": 0,
            "Yes": 1
        }

        education_mapping = {
            "Not Graduate": 0,
            "Graduate": 1
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

        dependents_mapping = {
            "0": 0,
            "1": 1,
            "2": 2,
            "3+": 3
        }

        # ---------------------------------
        # Convert categorical values
        # ---------------------------------

        gender = gender_mapping[gender_value]
        married = married_mapping[married_value]
        dependents = dependents_mapping[dependents_value]
        education = education_mapping[education_value]
        self_employed = self_employed_mapping[self_employed_value]
        property_area = property_area_mapping[property_area_value]

        # ---------------------------------
        # Secure numeric validation
        # ---------------------------------

        applicant_income = parse_positive_number(
            request.form.get("ApplicantIncome"),
            "Applicant income"
        )

        coapplicant_income = parse_positive_number(
            request.form.get("CoapplicantIncome"),
            "Co-applicant income",
            allow_zero=True
        )

        loan_amount = parse_positive_number(
            request.form.get("LoanAmount"),
            "Loan amount"
        )

        if loan_amount < 1000:
            raise ValueError(
                "Loan amount must be at least ₹1,000."
            )

        loan_amount_term = parse_positive_number(
            loan_term_value,
            "Loan term"
        )

        credit_history = float(credit_history_value)

        if credit_history not in (0.0, 1.0):
            raise ValueError(
                "Credit history must be either 0 or 1."
            )

        # ---------------------------------
        # Create model input array
        # ---------------------------------

        features = np.array([[
            gender,
            married,
            dependents,
            education,
            self_employed,
            applicant_income,
            coapplicant_income,
            loan_amount,
            loan_amount_term,
            credit_history,
            property_area
        ]], dtype=float)

        # ---------------------------------
        # Make prediction
        # ---------------------------------

        prediction = model.predict(features)
        prediction_value = int(prediction[0])

        if prediction_value == 1:
            prediction_text = (
                "Loan Application Likely to Be Approved"
            )
            prediction_status = "approved"

        else:
            prediction_text = (
                "Loan Application May Not Be Approved"
            )
            prediction_status = "rejected"

        return render_template(
            "index.html",
            prediction_text=prediction_text,
            prediction_status=prediction_status
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

    except Exception as error:
        print(f"Prediction error: {error}")

        return render_template(
            "index.html",
            error_message=(
                "Prediction failed. Please check the entered values "
                "and try again."
            )
        )


if __name__ == "__main__":
    app.run(debug=True)