from flask import Flask

from auth import auth_bp

from routes.home import home_bp

from routes.prediction import prediction_bp

from routes.history import history_bp

from database import initialize_database

app = Flask(__name__)

app.secret_key = "loanwise-ai-admin-secret-key"

app.register_blueprint(home_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(prediction_bp)
app.register_blueprint(history_bp)

# --------------------------------------------------
# Start Flask application
# --------------------------------------------------

if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)