from flask import Blueprint, request, jsonify, session
from services.auth_service import login_user, logout_user

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    result = login_user(username, password)
    if result["success"]:
        session["user_id"] = result["user_id"]
        session["username"] = result["username"]
        return jsonify({"message": "Login successful", "username": result["username"]}), 200

    return jsonify({"error": result["error"]}), 401


@auth_bp.route("/logout", methods=["POST"])
def logout():
    logout_user()
    return jsonify({"message": "Logged out"}), 200


@auth_bp.route("/status", methods=["GET"])
def status():
    if "user_id" in session:
        return jsonify({"logged_in": True, "username": session["username"]}), 200
    return jsonify({"logged_in": False}), 200
