from flask_smorest import Blueprint, abort
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from ..models import db, Note
from ..schemas import NoteSchema, NoteCreateSchema, NoteUpdateSchema
from marshmallow import ValidationError

blp = Blueprint(
    "Notes", "notes", url_prefix="/notes", description="CRUD operations for notes"
)

def error_response(message, code=400, status="error", errors=None):
    """Consistent error response structure."""
    return {
        "code": code,
        "status": status,
        "message": message,
        "errors": errors or {},
    }, code

@blp.route("/")
class NotesList(MethodView):
    @blp.response(200, NoteSchema(many=True), description="List all notes.")
    def get(self):
        """Retrieve all notes."""
        notes = Note.query.order_by(Note.created_at.desc()).all()
        return notes

    @blp.arguments(NoteCreateSchema)
    @blp.response(201, NoteSchema, description="Create a new note.")
    def post(self, note_data):
        """Create a new note."""
        try:
            note = Note(**note_data)
            db.session.add(note)
            db.session.commit()
            return note
        except SQLAlchemyError:
            db.session.rollback()
            abort(*error_response("Database error: could not create note.", 500, "db_error"))

@blp.route("/<int:note_id>")
class NoteDetail(MethodView):
    @blp.response(200, NoteSchema, description="Get a note by ID.")
    def get(self, note_id):
        """Retrieve a single note by ID."""
        note = Note.query.get(note_id)
        if not note:
            abort(*error_response(f"Note with id={note_id} not found.", 404, "not_found"))
        return note

    @blp.arguments(NoteUpdateSchema)
    @blp.response(200, NoteSchema, description="Update an existing note.")
    def put(self, update_data, note_id):
        """Update an existing note."""
        note = Note.query.get(note_id)
        if not note:
            abort(*error_response(f"Note with id={note_id} not found.", 404, "not_found"))
        try:
            if "title" in update_data:
                note.title = update_data["title"]
            if "content" in update_data:
                note.content = update_data["content"]
            db.session.commit()
            return note
        except SQLAlchemyError:
            db.session.rollback()
            abort(*error_response("Database error: could not update note.", 500, "db_error"))

    @blp.response(204, description="Delete a note by ID.")
    def delete(self, note_id):
        """Delete a note by ID."""
        note = Note.query.get(note_id)
        if not note:
            abort(*error_response(f"Note with id={note_id} not found.", 404, "not_found"))
        try:
            db.session.delete(note)
            db.session.commit()
            return "", 204
        except SQLAlchemyError:
            db.session.rollback()
            abort(*error_response("Database error: could not delete note.", 500, "db_error"))


# Register error handlers for validation
@blp.errorhandler(ValidationError)
def handle_validation_error(error):
    return error_response("Validation failed.", 400, "validation_error", error.messages)
