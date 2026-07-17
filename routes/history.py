import csv
import io
import sqlite3

from flask import Blueprint, Response, render_template

from auth import login_required
from database import get_database_connection


history_bp = Blueprint(
    "history",
    __name__
)


@history_bp.route("/history")
@login_required
def history():
    """
    Display prediction history and analytics.
    """

    connection = None

    try:
        connection = get_database_connection()

        predictions = connection.execute(
            """
            SELECT
                id,
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
                risk_level,
                prediction_date
            FROM predictions
            ORDER BY id DESC
            """
        ).fetchall()

        # ------------------------------------------
        # Dashboard statistics
        # ------------------------------------------

        total_predictions = len(predictions)

        approved_predictions = sum(
         1
        for row in predictions
         if row["prediction"] == "Loan Approved"
        )

        rejected_predictions = (
            total_predictions - approved_predictions
        )

        confidence_values = []

        for row in predictions:
            confidence = row["confidence"]

            if confidence is not None:
                try:
                    confidence_values.append(float(confidence))
                except (TypeError, ValueError):
                    pass

        if confidence_values:
            average_confidence = round(
                sum(confidence_values)
                / len(confidence_values),
                2
            )
        else:
            average_confidence = 0

        # ------------------------------------------
        # Approval chart data
        # ------------------------------------------

        approval_chart_data = {
            "approved": approved_predictions,
            "rejected": rejected_predictions
        }

        # ------------------------------------------
        # Risk chart data
        # ------------------------------------------

        risk_chart_data = {
            "low": 0,
            "medium": 0,
            "high": 0
        }

        # ------------------------------------------
        # Daily chart temporary data
        # ------------------------------------------

        daily_counts = {}

        for row in predictions:

            # --------------------------------------
            # Risk level processing
            # --------------------------------------

            risk_level = row["risk_level"]

            if risk_level:
                normalized_risk = str(
                    risk_level
                ).strip().lower()

                if normalized_risk == "low":
                    risk_chart_data["low"] += 1

                elif normalized_risk == "medium":
                    risk_chart_data["medium"] += 1

                elif normalized_risk == "high":
                    risk_chart_data["high"] += 1

            # --------------------------------------
            # Prediction date processing
            # --------------------------------------

            prediction_date = row["prediction_date"]

            if prediction_date:
                date_only = str(
                    prediction_date
                ).split(" ")[0]

                daily_counts[date_only] = (
                    daily_counts.get(date_only, 0) + 1
                )

        # ------------------------------------------
        # Convert daily data for Chart.js
        # ------------------------------------------

        sorted_dates = sorted(daily_counts.keys())

        daily_chart_data = {
            "labels": sorted_dates,
            "counts": [
                daily_counts[date]
                for date in sorted_dates
            ]
        }

        return render_template(
            "history.html",
            predictions=predictions,
            total_predictions=total_predictions,
            approved_predictions=approved_predictions,
            rejected_predictions=rejected_predictions,
            average_confidence=average_confidence,
            approval_chart_data=approval_chart_data,
            risk_chart_data=risk_chart_data,
            daily_chart_data=daily_chart_data
        )

    except sqlite3.Error as error:
        print(f"History database error: {error}")

        return render_template(
            "history.html",
            predictions=[],
            total_predictions=0,
            approved_predictions=0,
            rejected_predictions=0,
            average_confidence=0,
            approval_chart_data={
                "approved": 0,
                "rejected": 0
            },
            risk_chart_data={
                "low": 0,
                "medium": 0,
                "high": 0
            },
            daily_chart_data={
                "labels": [],
                "counts": []
            },
            error_message=(
                "Prediction history could not be loaded."
            )
        )

    finally:
        if connection is not None:
            connection.close()


@history_bp.route("/export-csv")
@login_required
def export_csv():
    """
    Export prediction history as a CSV file.
    """

    connection = None

    try:
        connection = get_database_connection()

        predictions = connection.execute(
            """
            SELECT
                id,
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
                risk_level,
                prediction_date
            FROM predictions
            ORDER BY id DESC
            """
        ).fetchall()

        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow([
            "ID",
            "Gender",
            "Married",
            "Dependents",
            "Education",
            "Self Employed",
            "Applicant Income",
            "Co-applicant Income",
            "Loan Amount",
            "Loan Term",
            "Credit History",
            "Property Area",
            "Prediction",
            "Confidence",
            "Risk Level",
            "Prediction Date"
        ])

        for prediction in predictions:
            writer.writerow([
                prediction["id"],
                prediction["gender"],
                prediction["married"],
                prediction["dependents"],
                prediction["education"],
                prediction["self_employed"],
                prediction["applicant_income"],
                prediction["coapplicant_income"],
                prediction["loan_amount"],
                prediction["loan_term"],
                prediction["credit_history"],
                prediction["property_area"],
                prediction["prediction"],
                prediction["confidence"],
                prediction["risk_level"],
                prediction["prediction_date"]
            ])

        csv_data = output.getvalue()
        output.close()

        return Response(
            csv_data,
            mimetype="text/csv",
            headers={
                "Content-Disposition": (
                    "attachment; "
                    "filename=loan_prediction_history.csv"
                )
            }
        )

    except sqlite3.Error as error:
        print(f"CSV export error: {error}")

        return Response(
            "Prediction history could not be exported.",
            status=500,
            mimetype="text/plain"
        )

    finally:
        if connection is not None:
            connection.close()