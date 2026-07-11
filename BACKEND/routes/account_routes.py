from flask import Blueprint, request, jsonify, session
from services.account_service import get_balance, deposit, withdraw

account_bp = Blueprint("account", __name__, url_prefix="/api/account")


def require_login():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized. Please log in."}), 401
    return None


@account_bp.route("/balance", methods=["GET"])
def balance():
    auth_error = require_login()
    if auth_error:
        return auth_error
    result = get_balance(session["user_id"])
    return jsonify(result), 200


@account_bp.route("/deposit", methods=["POST"])
def deposit_funds():
    auth_error = require_login()
    if auth_error:
        return auth_error

    data = request.get_json()
    amount = data.get("amount")
    result = deposit(session["user_id"], amount)
    if result["success"]:
        return jsonify(result), 200
    return jsonify(result), 400


@account_bp.route("/withdraw", methods=["POST"])
def withdraw_funds():
    auth_error = require_login()
    if auth_error:
        return auth_error

    data = request.get_json()
    amount = data.get("amount")
    result = withdraw(session["user_id"], amount)
    if result["success"]:
        return jsonify(result), 200
    return jsonify(result), 400
