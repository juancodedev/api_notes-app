from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.tags import create_tag, get_tags, get_tag_by_id, update_tag, delete_tag
from schemas import TagCreate, Tag
from database import get_db

router = APIRouter()

@router.post("/", response_model=Tag)
def add_tag(tag: TagCreate, db: Session = Depends(get_db)):
    return create_tag(db, tag)

@router.get("/", response_model=List[Tag])
def list_tags(db: Session = Depends(get_db)):
    return get_tags(db)

@router.get("/{id}", response_model=Tag)
def get_tag(id: int, db: Session = Depends(get_db)):
    return get_tag_by_id(db, id)

@router.put("/{id}", response_model=Tag)
def modify_tag(id: int, tag: TagCreate, db: Session = Depends(get_db)):
    return update_tag(db, id, tag)

@router.delete("/{id}")
def remove_tag(id: int, db: Session = Depends(get_db)):
    if delete_tag(db, id):
        return {"detail": "Tag deleted successfully"}
    raise HTTPException(status_code=404, detail="Tag not found")
