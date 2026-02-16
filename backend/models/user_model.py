from extensions import db
from datetime import datetime


class User(db.Document):
    username = db.StringField(required=True, unique=True)
    email = db.EmailField(required=True, unique=True)
    password_hash = db.StringField(required=True)

    mfa_enabled = db.BooleanField(default=False)
    mfa_secret = db.StringField()

    created_at = db.DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "users",
        "indexes": ["username", "email"]
    }