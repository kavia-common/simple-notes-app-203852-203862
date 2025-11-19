from marshmallow import Schema, fields, validate

# PUBLIC_INTERFACE
class NoteSchema(Schema):
    """Schema for Note serialization."""
    id = fields.Int(dump_only=True, description="Unique identifier for the note.")
    title = fields.Str(required=True, description="The title of the note.", validate=validate.Length(min=1, max=120))
    content = fields.Str(required=True, description="The content of the note.")
    created_at = fields.DateTime(dump_only=True, description="Timestamp when the note was created.")
    updated_at = fields.DateTime(dump_only=True, description="Timestamp when the note was last updated.")


# PUBLIC_INTERFACE
class NoteCreateSchema(Schema):
    """Schema for creating a new note."""
    title = fields.Str(required=True, validate=validate.Length(min=1, max=120), description="The title of the note.")
    content = fields.Str(required=True, description="The content of the note.")


# PUBLIC_INTERFACE
class NoteUpdateSchema(Schema):
    """Schema for updating an existing note."""
    title = fields.Str(validate=validate.Length(min=1, max=120), description="The new title of the note.")
    content = fields.Str(description="The new content of the note.")
