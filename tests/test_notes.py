import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from services.notes import create_note, get_notes, get_note_by_id, update_note, delete_note
from models import Note
from schemas import NoteCreate
from database import Base

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"
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

def test_create_note(db):
    note_data = NoteCreate(title="Test Note", content="This is a test note.")
    user_id = 1
    note = create_note(db, note_data, user_id)
    assert note.id is not None
    assert note.title == "Test Note"
    assert note.content == "This is a test note."
    assert note.user_id == user_id

def test_get_notes(db):
    user_id = 1
    note_data_1 = NoteCreate(title="Note 1", content="Content 1")
    note_data_2 = NoteCreate(title="Note 2", content="Content 2")
    create_note(db, note_data_1, user_id)
    create_note(db, note_data_2, user_id)
    notes = get_notes(db, user_id)
    assert len(notes) == 2
    assert notes[0].title == "Note 1"
    assert notes[1].title == "Note 2"

def test_get_note_by_id(db):
    user_id = 1
    note_data = NoteCreate(title="Test Note", content="This is a test note.")
    note = create_note(db, note_data, user_id)
    fetched_note = get_note_by_id(db, note.id, user_id)
    assert fetched_note.id == note.id
    assert fetched_note.title == note.title

def test_update_note(db):
    user_id = 1
    note_data = NoteCreate(title="Old Title", content="Old Content")
    note = create_note(db, note_data, user_id)
    updated_data = NoteCreate(title="New Title", content="New Content")
    updated_note = update_note(db, note.id, user_id, updated_data)
    assert updated_note.title == "New Title"
    assert updated_note.content == "New Content"

def test_delete_note(db):
    user_id = 1
    note_data = NoteCreate(title="Test Note", content="This is a test note.")
    note = create_note(db, note_data, user_id)
    result = delete_note(db, note.id, user_id)
    assert result is True
    notes = get_notes(db, user_id)
    assert len(notes) == 0