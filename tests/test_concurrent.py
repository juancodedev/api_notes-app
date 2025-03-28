import pytest
import threading
from sqlalchemy import create_engine
from sqlalchemy.orm import Session,sessionmaker
from models import Note
from schemas import NoteCreate
from services.notes import update_note
from database import Base

SQLALCHEMY_TEST_DATABASE_URL = "postgresql://postgres:5HOmZmsJ6Jhe6Ky@localhost:5432/test_db"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def test_concurrent_updates(db: Session):
    def update_note_thread(note_id, user_id, new_title):
        note_data = NoteCreate(title=new_title, content="Updated content", locked=False)
        update_note(db, note_id, user_id, note_data)

    note = Note(title="Original Title", content="Original Content", user_id=1)
    db.add(note)
    db.commit()
    db.refresh(note)

    thread1 = threading.Thread(target=update_note_thread, args=(note.id, 1, "Title from Thread 1"))
    thread2 = threading.Thread(target=update_note_thread, args=(note.id, 1, "Title from Thread 2"))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    updated_note = db.query(Note).filter(Note.id == note.id).first()
    assert updated_note.title in ["Title from Thread 1", "Title from Thread 2"]