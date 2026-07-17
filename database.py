import sqlite3

from werkzeug.security import generate_password_hash

from config import (
    DATABASE_PATH,
    DEFAULT_ADMIN_USERNAME,
    DEFAULT_ADMIN_PASSWORD
)


def get_database_connection():
    """
    Create and return a SQLite database connection.
    """

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    """
    Create required tables and default admin account.
    """

    connection = get_database_connection()

    try:
        cursor = connection.cursor()

        # ------------------------------------------
        # Predictions table
        # ------------------------------------------

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictions (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                prediction_date
                    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

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

        # ------------------------------------------
        # Admins table
        # ------------------------------------------

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admins (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                username TEXT UNIQUE NOT NULL,

                password_hash TEXT NOT NULL
            )
        """)

        # ------------------------------------------
        # Check default admin
        # ------------------------------------------

        cursor.execute(
            """
            SELECT id
            FROM admins
            WHERE username = ?
            """,
            (
                DEFAULT_ADMIN_USERNAME,
            )
        )

        existing_admin = cursor.fetchone()

        # ------------------------------------------
        # Create default admin once
        # ------------------------------------------

        if existing_admin is None:

            hashed_password = generate_password_hash(
                DEFAULT_ADMIN_PASSWORD
            )

            cursor.execute(
                """
                INSERT INTO admins (
                    username,
                    password_hash
                )
                VALUES (?, ?)
                """,
                (
                    DEFAULT_ADMIN_USERNAME,
                    hashed_password
                )
            )

        connection.commit()

    finally:
        connection.close()


def save_prediction(
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
):
    """
    Save one prediction record.
    """

    connection = get_database_connection()

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
        )

        connection.commit()

    finally:
        connection.close()


def get_all_predictions():
    """
    Return all predictions, newest first.
    """

    connection = get_database_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM predictions
            ORDER BY prediction_date DESC
            """
        )

        records = cursor.fetchall()

        return records

    finally:
        connection.close()


def get_admin_by_username(username):
    """
    Return one admin record by username.
    """

    connection = get_database_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM admins
            WHERE username = ?
            """,
            (
                username,
            )
        )

        admin = cursor.fetchone()

        return admin

    finally:
        connection.close()