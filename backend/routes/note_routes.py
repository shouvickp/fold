from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.note_model import Note
from utils.validators import (
    Validator,
    ValidationError,
    handle_validation_error
)

from datetime import datetime


note_routes = Blueprint(
    "note_routes",
    __name__,
    url_prefix="/api/notes"
)


# -----------------------------------------
# CREATE NOTE
# -----------------------------------------

@note_routes.route("/", methods=["POST"])
@jwt_required()
def create_note():

    try:

        user_id = get_jwt_identity()

        data = Validator.validate_json_request()

        validated_data = Validator.validate_note_payload(data)

        note = Note(
            title=validated_data["title"],
            content=validated_data["content"],
            user_id=user_id
        )

        note.save()

        return jsonify({
            "msg": "Note created successfully",
            "note": note.to_dict()
        }), 201

    except ValidationError as error:
        return handle_validation_error(error)

    except Exception:
        return jsonify({"msg": "Internal server error"}), 500


# -----------------------------------------
# GET ALL NOTES FOR USER
# -----------------------------------------

@note_routes.route("/", methods=["GET"])
@jwt_required()
def get_notes():

    try:

        user_id = get_jwt_identity()

        notes = Note.objects(user_id=user_id)

        return jsonify([
            note.to_dict()
            for note in notes
        ]), 200

    except Exception:
        return jsonify({"msg": "Internal server error"}), 500


# -----------------------------------------
# GET SINGLE NOTE
# -----------------------------------------

@note_routes.route("/<note_id>", methods=["GET"])
@jwt_required()
def get_note(note_id):

    try:

        Validator.validate_object_id(note_id)

        user_id = get_jwt_identity()

        note = Note.objects(
            id=note_id,
            user_id=user_id
        ).first()

        if not note:
            return jsonify({
                "msg": "Note not found"
            }), 404

        return jsonify(note.to_dict()), 200

    except ValidationError as error:
        return handle_validation_error(error)

    except Exception:
        return jsonify({"msg": "Internal server error"}), 500


# -----------------------------------------
# UPDATE NOTE
# -----------------------------------------

@note_routes.route("/<note_id>", methods=["PUT"])
@jwt_required()
def update_note(note_id):

    try:

        Validator.validate_object_id(note_id)

        user_id = get_jwt_identity()

        note = Note.objects(
            id=note_id,
            user_id=user_id
        ).first()

        if not note:
            return jsonify({
                "msg": "Note not found"
            }), 404

        data = Validator.validate_json_request()

        validated_data = Validator.validate_note_payload(data)

        note.title = validated_data["title"]
        note.content = validated_data["content"]
        note.updated_at = datetime.utcnow()

        note.save()

        return jsonify({
            "msg": "Note updated successfully",
            "note": note.to_dict()
        }), 200

    except ValidationError as error:
        return handle_validation_error(error)

    except Exception:
        return jsonify({"msg": "Internal server error"}), 500


# -----------------------------------------
# DELETE NOTE
# -----------------------------------------

@note_routes.route("/<note_id>", methods=["DELETE"])
@jwt_required()
def delete_note(note_id):

    try:

        Validator.validate_object_id(note_id)

        user_id = get_jwt_identity()

        note = Note.objects(
            id=note_id,
            user_id=user_id
        ).first()

        if not note:
            return jsonify({
                "msg": "Note not found"
            }), 404

        note.delete()

        return jsonify({
            "msg": "Note deleted successfully"
        }), 200

    except ValidationError as error:
        return handle_validation_error(error)

    except Exception:
        return jsonify({"msg": "Internal server error"}), 500
