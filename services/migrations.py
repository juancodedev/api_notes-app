from sqlalchemy.orm import Session
from models import Note

def update_null_locked_fields(db: Session):
    notes = db.query(Note).filter(Note.locked.is_(None)).all()
    for note in notes:
        note.locked = False
    db.commit()

