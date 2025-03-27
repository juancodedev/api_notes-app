from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.notes import create_note, get_notes, get_note_by_id, update_note, delete_note
from schemas import NoteCreate, NoteResponse
from database import get_db
from services.auth import get_current_user

router = APIRouter()


@router.post("/")
def add_note(note: NoteCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    user_id = current_user["id"]
    return create_note(db, note, user_id)


@router.get("/", response_model=List[NoteResponse])
def list_notes(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user["id"]
    return get_notes(db, user_id)

@router.get("/{id}")
def get_note(
    id: int, db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user["id"]
    return get_note_by_id(db, id, user_id)


@router.put("/{id}")
def modify_note(id: int, note: NoteCreate, db: Session = Depends(get_db),
                current_user: dict = Depends(get_current_user)
                ):
    user_id = current_user["id"]
    return update_note(db, id, user_id, note)


@router.delete("/{id}")
def remove_note(id: int, db: Session = Depends(get_db),
                current_user: dict = Depends(get_current_user)
                ):
    user_id = current_user["id"]
    return delete_note(db, id, user_id)
