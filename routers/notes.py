from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.notes import create_note, get_notes, get_note_by_id, update_note, delete_note
from schemas import NoteCreate, NoteResponse
from database import get_db

router = APIRouter()

@router.post("/")
def add_note(note: NoteCreate, db: Session = Depends(get_db)):
    return create_note(db, note)

@router.get("/", response_model=List[NoteResponse])
def list_notes(db: Session = Depends(get_db)):
    return get_notes(db)

@router.get("/{id}")
def get_note(id: int, db: Session = Depends(get_db)):
    return get_note_by_id(db, id)

@router.put("/{id}")
def modify_note(id: int, note: NoteCreate, db: Session = Depends(get_db)):
    return update_note(db, id, note)

@router.delete("/{id}")
def remove_note(id: int, db: Session = Depends(get_db)):
    return delete_note(db, id)
