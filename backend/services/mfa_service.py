import pyotp
import base64
import qrcode
import io


class MFAService:

    @staticmethod
    def generate_secret():
        return pyotp.random_base32()

    @staticmethod
    def generate_qr_code(username, secret):

        totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
            name=username + "@FoldApp",
            issuer_name="FoldApp"
        )

        qr = qrcode.make(totp_uri)

        buffer = io.BytesIO()
        qr.save(buffer, format="PNG")

        return base64.b64encode(buffer.getvalue()).decode()

    @staticmethod
    def verify_otp(secret, otp):

        totp = pyotp.TOTP(secret)

        return totp.verify(otp, valid_window=1)
