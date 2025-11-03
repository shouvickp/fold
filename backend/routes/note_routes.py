from flask import Blueprint, request, jsonify
from models import Note

note_routes = Blueprint('note_routes', __name__, url_prefix='/api/notes')

# --- Helper Functions to Reduce Duplication ---

def get_note_by_id(note_id):
    """
    Validates note_id, fetches the note, and returns the note object or an error tuple.
    
    Returns: (Note object, None) on success.
    Returns: (None, (jsonify response, status_code)) on failure.
    """
    if not note_id:
        return None, (jsonify({"msg": "Note ID is required."}), 400)
    
    # NOTE: Python uses len() instead of .len for string length
    if len(note_id.strip()) != 24:
        # Assuming a 24-character MongoDB ObjectId format
        return None, (jsonify({"msg": "Note ID is invalid (must be 24 characters)."}), 400)

    note = Note.objects(id=note_id).first()
    
    if not note:
        return None, (jsonify({"msg": "Note not found"}), 404)
        
    return note, None # Success: return note object, no error

def validate_note_payload():
    """
    Validates title and content from request data.
    
    Returns: (clean_data dict, None) on success.
    Returns: (None, (jsonify response, status_code)) on failure.
    """
    data = request.get_json()
    if not data:
        return None, (jsonify({"msg": "Payload must be valid JSON."}), 400)
        
    title = data.get('title')
    content = data.get('content')
    
    if not title or not isinstance(title, str) or not title.strip():
        # Strip is important to catch strings with only spaces
        return None, (jsonify({ "msg": "Title is required and cannot be empty."}), 400)
        
    if not content or not isinstance(content, str) or not content.strip():
        return None, (jsonify({"msg":"Content is required and cannot be empty."}), 400)
        
    # Return cleaned data for insertion/update
    clean_data = {
        "title": title.strip(),
        "content": content.strip()
    }
    
    return clean_data, None # Success: return cleaned data, no error

# ---------------------------------------------

@note_routes.route('/', methods=['GET'])
def get_notes():
    """Fetches all notes from MongoDB and returns them."""
    notes = Note.objects().to_json()
    return notes, 200

@note_routes.route('/add', methods=['POST'])
def create_note():
    """Creates a new note and inserts it into MongoDB."""
    
    # 1. Use helper for validation
    validated_data, error_tuple = validate_note_payload()
    if error_tuple:
        return error_tuple # Returns (jsonify, 400)

    title = validated_data['title']

    # 2. Check for duplicate title (unique constraint logic)
    if Note.objects(title=title).first():
        return jsonify({"msg": "Note with the same title already exists."}), 400

    # 3. Create and save
    note = Note(**validated_data)
    note.save()
    return note.to_json(), 201

@note_routes.route('/<string:note_id>', methods=['GET'])
def get_note(note_id):
    """Fetches a single note by ID from MongoDB and returns it."""
    
    # Use helper to validate ID and fetch note
    note, error_tuple = get_note_by_id(note_id)
    if error_tuple:
        return error_tuple # Returns (jsonify, 400 or 404)

    # Note is guaranteed to exist here
    return note.to_json(), 200

@note_routes.route('/<string:note_id>', methods=['PUT'])
def update_note(note_id):
    """Updates a note by ID in MongoDB."""
    
    # 1. Validate ID and fetch existing note
    note, error_tuple = get_note_by_id(note_id)
    if error_tuple:
        return error_tuple # Returns (jsonify, 400 or 404)
        
    # 2. Validate payload data
    validated_data, error_tuple = validate_note_payload()
    if error_tuple:
        return error_tuple # Returns (jsonify, 400)
    
    # 3. Check for duplicate title if title is being changed
    new_title = validated_data['title']
    if new_title != note.title and Note.objects(title=new_title).first():
        return jsonify({"msg": "Note with the same title already exists."}), 400
    
    # 4. Update the note
    note.update(**validated_data) 
    return jsonify({"msg": "Note updated successfully"}), 200

@note_routes.route('/<note_id>', methods=['DELETE'])
def delete_note(note_id):
    """Deletes a note by ID from MongoDB."""
    
    # Use helper to validate ID and fetch existing note
    note, error_tuple = get_note_by_id(note_id)
    if error_tuple:
        return error_tuple # Returns (jsonify, 400 or 404)

    # Note is guaranteed to exist here
    note.delete()
    return jsonify({"msg": "Note deleted successfully"}), 200