from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Load trained model
model = pickle.load(open("loan_model.pkl", "rb"))

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    gender = float(request.form["Gender"])
    married = float(request.form["Married"])
    dependents = float(request.form["Dependents"])
    education = float(request.form["Education"])
    self_employed = float(request.form["Self_Employed"])
    applicant_income = float(request.form["ApplicantIncome"])
    coapplicant_income = float(request.form["CoapplicantIncome"])
    loan_amount = float(request.form["LoanAmount"])
    loan_amount_term = float(request.form["Loan_Amount_Term"])
    credit_history = float(request.form["Credit_History"])
    property_area = float(request.form["Property_Area"])

    features = np.array([[gender,
                          married,
                          dependents,
                          education,
                          self_employed,
                          applicant_income,
                          coapplicant_income,
                          loan_amount,
                          loan_amount_term,
                          credit_history,
                          property_area]])

    prediction = model.predict(features)

    if prediction[0] == 1:
        result = "Loan Approved ✅"
    else:
        result = "Loan Rejected ❌"

    return render_template("index.html", prediction=result)


if __name__ == "__main__":
    app.run(debug=True)