from flask import request, jsonify
from bson.objectid import ObjectId


class ValidationError(Exception):
    """Custom validation exception."""
    pass


class Validator:

    @staticmethod
    def validate_json_request():
        """
        Validates JSON request presence.
        """

        data = request.get_json()

        if not data:
            raise ValidationError("Request must contain valid JSON")

        return data

    @staticmethod
    def validate_note_payload(data):

        title = data.get("title")
        content = data.get("content")

        if not title or not isinstance(title, str) or not title.strip():
            raise ValidationError("Title is required and must be valid")

        if len(title.strip()) > 200:
            raise ValidationError("Title must not exceed 200 characters")

        if not content or not isinstance(content, str) or not content.strip():
            raise ValidationError("Content is required and must be valid")

        if len(content.strip()) > 5000:
            raise ValidationError("Content must not exceed 5000 characters")

        return {
            "title": title.strip(),
            "content": content.strip()
        }

    @staticmethod
    def validate_object_id(object_id):

        if not object_id:
            raise ValidationError("ID is required")

        if not ObjectId.is_valid(object_id):
            raise ValidationError("Invalid ID format")

        return object_id


def handle_validation_error(error):
    """
    Converts validation error to proper API response.
    """

    return jsonify({
        "msg": str(error)
    }), 400
