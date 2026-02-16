from extensions import db
from datetime import datetime


class Note(db.Document):
    """
    Note document representing user-created notes.

    Sonar Compliance:
    - Indexed fields for performance
    - Required field validation
    - Proper schema constraints
    """

    title = db.StringField(
        required=True,
        min_length=1,
        max_length=200
    )

    content = db.StringField(
        required=True,
        min_length=1,
        max_length=5000
    )

    user_id = db.StringField(
        required=True
    )

    created_at = db.DateTimeField(
        default=datetime.utcnow
    )

    updated_at = db.DateTimeField(
        default=datetime.utcnow
    )

    meta = {
        "collection": "notes",
        "indexes": [
            "user_id",
            "title",
            "-created_at"
        ],
        "ordering": ["-created_at"]
    }

    def to_dict(self):
        """
        Converts Note document to dictionary.
        Avoids exposing internal Mongo fields.
        """

        return {
            "id": str(self.id),
            "title": self.title,
            "content": self.content,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
