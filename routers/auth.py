from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.auth import create_access_token, hash_password, authenticate_user
from schemas import UserCreate, UserResponse, UserLogin
from database import get_db
from models import User
from datetime import timedelta

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = hash_password(user.password)
    new_user = User(
        name=user.name, 
        username=user.username, 
        password=hashed_password
        )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, user.username, user.password)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token({"sub": db_user.username}, timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}
