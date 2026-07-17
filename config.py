import os


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "loan_model.pkl"
)

DATABASE_PATH = os.path.join(
    BASE_DIR,
    "predictions.db"
)

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "loanwise-ai-admin-secret-key"
)

DEFAULT_ADMIN_USERNAME = os.environ.get(
    "DEFAULT_ADMIN_USERNAME",
    "admin"
)

DEFAULT_ADMIN_PASSWORD = os.environ.get(
    "DEFAULT_ADMIN_PASSWORD",
    "loanwise123"
)

DEBUG = os.environ.get(
    "FLASK_DEBUG",
    "False"
).lower() == "true"