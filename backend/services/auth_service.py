from models.user_model import User
from utils.security import hash_password, verify_password
from services.mfa_service import MFAService
from flask_jwt_extended import create_access_token


class AuthService:

    @staticmethod
    def register_user(username, email, password):

        if User.objects(username=username).first():
            return None, "Username already exists"

        if User.objects(email=email).first():
            return None, "Email already exists"

        user = User(
            username=username,
            email=email,
            password_hash=hash_password(password)
        )

        user.save()

        return user, None

    @staticmethod
    def login_user(username, password):

        user = User.objects(username=username).first()

        if not user:
            return None, "Invalid username"

        if not verify_password(password, user.password_hash):
            return None, "Invalid password"

        if user.mfa_enabled:
            return {
                "mfa_required": True,
                "user_id": str(user.id),
                "mfa_enabled": True
            }, None

        token = create_access_token(identity=str(user.id))

        return {
                    "access_token": token,
                    "user_id": str(user.id),
                    "mfa_enabled": False,
                    "mfa_required": False
                }, None

    @staticmethod
    def setup_mfa(user):

        secret = MFAService.generate_secret()

        user.mfa_secret = secret
        user.save()

        qr_code = MFAService.generate_qr_code(user.username, secret)

        return qr_code

    @staticmethod
    def verify_mfa(user, otp):

        if not MFAService.verify_otp(user.mfa_secret, otp):
            return None, "Invalid OTP"

        user.mfa_enabled = True
        user.save()

        token = create_access_token(identity=str(user.id))

        return token, None
