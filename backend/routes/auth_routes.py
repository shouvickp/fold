from flask import Blueprint, request, jsonify
from services.auth_service import AuthService
from models.user_model import User


auth_routes = Blueprint("auth_routes", __name__, url_prefix="/api/auth")


@auth_routes.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    user, error = AuthService.register_user(username, email, password)

    if error:
        return jsonify({"msg": error}), 400

    return jsonify({"msg": "User registered successfully"}), 201


@auth_routes.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    result, error = AuthService.login_user(username, password)

    if error:
        return jsonify({"msg": error}), 401

    return jsonify(result), 200


@auth_routes.route("/setup-mfa/<user_id>", methods=["POST"])
def setup_mfa(user_id):

    user = User.objects(id=user_id).first()

    if not user:
        return jsonify({"msg": "User not found"}), 404

    qr = AuthService.setup_mfa(user)

    return jsonify({
        "qr_code": qr
    })


@auth_routes.route("/verify-mfa/<user_id>", methods=["POST"])
def verify_mfa(user_id):

    data = request.get_json()

    otp = data.get("otp")

    user = User.objects(id=user_id).first()

    token, error = AuthService.verify_mfa(user, otp)

    if error:
        return jsonify({"msg": error}), 400

    return jsonify({
        "access_token": token
    })
