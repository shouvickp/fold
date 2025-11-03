from mongoengine import Document, StringField, DateTimeField
from datetime import datetime

class Note(Document):
    title = StringField(required=True)
    content = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    modified_at = DateTimeField(default=datetime.utcnow)

class User(Document):
    username = StringField(required=True)
    password = StringField(required=True)
    # created_at  should be automatically inserted only once at the time of creation
    created_at = DateTimeField(default=datetime.utcnow)
    # modified_at should be updated automatically when updated
    modified_at = DateTimeField(default=datetime.utcnow)