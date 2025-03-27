from http.client import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import Note, NoteTags, Tag
from schemas import NoteCreate
from datetime import datetime, UTC
from .migrations import update_null_locked_fields

def initialize_db(db: Session):
    update_null_locked_fields(db)
def create_note(db: Session, note_data: NoteCreate, user_id: int):
    if note_data.locked is None:
        note_data.locked = False
    note = Note(**note_data.model_dump(), user_id=user_id)
    db.add(note)
    db.commit()
    db.refresh(note)
    for tag_name in note_data.tags:
        tag = db.query(Tag).filter(Tag.name == tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
            db.add(tag)
            db.commit()
            db.refresh(tag)
        note_tag = NoteTags(note_id=note.id, tag_id=tag.id)
        db.add(note_tag)
    db.commit()
    return note

def get_notes(db: Session, user_id: int):
    notes = db.query(Note).filter(Note.user_id == user_id).all()
    for note in notes:
        note.tags = db.query(Tag).join(NoteTags).filter(NoteTags.note_id == note.id).all()
    return notes

def get_note_by_id(db: Session, note_id: int, user_id: int):
    note = db.query(Note).filter(Note.id == note_id, Note.user_id == user_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    note.tags = db.query(Tag).join(NoteTags).filter(NoteTags.note_id == note.id).all()
    return note

def update_note(db: Session, note_id: int, user_id: int, note_data: NoteCreate):
    note = db.query(Note).filter(Note.id == note_id, Note.user_id == user_id).first()
    if note is None:
        return None

    note.title = note_data.title
    note.content = note_data.content
    note.locked = note_data.locked
    note.updated_at = datetime.now(UTC)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return None

    return note

def delete_note(db: Session, note_id: int, user_id: int):
    note = db.query(Note).filter(Note.id == note_id, Note.user_id == user_id).first()
    if note:
        db.delete(note)
        db.commit()
        return True
    return False
