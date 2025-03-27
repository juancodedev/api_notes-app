from http.client import HTTPException
from sqlalchemy.orm import Session
from models import Tag
from schemas import TagCreate

def create_tag(db: Session, tag_data: TagCreate):
    tag = Tag(**tag_data.dict())
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag

def get_tags(db: Session):
    return db.query(Tag).all()

def get_tag_by_id(db: Session, tag_id: int):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag

def update_tag(db: Session, tag_id: int, tag_data: TagCreate):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    tag.name = tag_data.name
    db.commit()
    return tag

def delete_tag(db: Session, tag_id: int):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if tag:
        db.delete(tag)
        db.commit()
        return True
    return False
