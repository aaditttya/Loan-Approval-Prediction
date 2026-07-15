from flask import Flask, render_template, request
import pickle
import numpy as np
import os

app = Flask(__name__)

# Get the directory where app.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Create complete path of the trained model
MODEL_PATH = os.path.join(BASE_DIR, "loan_model.pkl")

# Load trained machine-learning model
with open(MODEL_PATH, "rb") as model_file:
    model = pickle.load(model_file)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get text values from HTML form
        gender_value = request.form.get("Gender")
        married_value = request.form.get("Married")
        dependents_value = request.form.get("Dependents")
        education_value = request.form.get("Education")
        self_employed_value = request.form.get("Self_Employed")
        property_area_value = request.form.get("Property_Area")

        # Check whether all required fields were received
        required_fields = {
            "Gender": gender_value,
            "Married": married_value,
            "Dependents": dependents_value,
            "Education": education_value,
            "Self Employed": self_employed_value,
            "Property Area": property_area_value,
            "Applicant Income": request.form.get("ApplicantIncome"),
            "Co-applicant Income": request.form.get("CoapplicantIncome"),
            "Loan Amount": request.form.get("LoanAmount"),
            "Loan Term": request.form.get("Loan_Amount_Term"),
            "Credit History": request.form.get("Credit_History")
        }

        missing_fields = [
            field_name
            for field_name, field_value in required_fields.items()
            if field_value is None or field_value == ""
        ]

        if missing_fields:
            raise ValueError(
                "Please fill all required fields: "
                + ", ".join(missing_fields)
            )

        # Convert categorical text values into numbers
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

        gender = gender_mapping[gender_value]
        married = married_mapping[married_value]
        dependents = dependents_mapping[dependents_value]
        education = education_mapping[education_value]
        self_employed = self_employed_mapping[self_employed_value]
        property_area = property_area_mapping[property_area_value]

        # Convert numerical form values
        applicant_income = float(
            request.form.get("ApplicantIncome")
        )

        coapplicant_income = float(
            request.form.get("CoapplicantIncome")
        )

        loan_amount = float(
            request.form.get("LoanAmount")
        )

        loan_amount_term = float(
            request.form.get("Loan_Amount_Term")
        )

        credit_history = float(
            request.form.get("Credit_History")
        )

        # Create input array in the same feature order used during training
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

        # Make prediction
        prediction = model.predict(features)

        if int(prediction[0]) == 1:
            result = "Loan Approved ✅"
        else:
            result = "Loan Rejected ❌"

        return render_template(
            "index.html",
            prediction_text=result
        )

    except ValueError as error:
        return render_template(
            "index.html",
            prediction_text=f"Input Error: {error}"
        )

    except KeyError as error:
        return render_template(
            "index.html",
            prediction_text=f"Invalid selected value: {error}"
        )

    except Exception as error:
        print(f"Prediction error: {error}")

        return render_template(
            "index.html",
            prediction_text="Prediction failed. Please check the entered values."
        )


if __name__ == "__main__":
    app.run(debug=True)