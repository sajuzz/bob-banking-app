from flask import Flask
from database import init_db
from routes.auth_routes import auth_bp
from routes.account_routes import account_bp

app = Flask(__name__)
app.secret_key = "banking_secret_key_2024"

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(account_bp)

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
