from http.client import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import Note
from schemas import NoteCreate
from datetime import datetime, UTC

def create_note(db: Session, note_data: NoteCreate, user_id: int):
    note = Note(**note_data.model_dump(), user_id=user_id)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

def get_notes(db: Session, user_id: int):
    return db.query(Note).filter(Note.user_id == user_id).all()

def get_note_by_id(db: Session, note_id: int, user_id: int):
    note = db.query(Note).filter(Note.id == note_id, Note.user_id == user_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

def update_note(db: Session, note_id: int, user_id: int, note_data: NoteCreate):
    note = db.query(Note).filter(Note.id == note_id, Note.user_id == user_id).first()
    if note is None:
        return None

    note.title = note_data.title
    note.content = note_data.content
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
