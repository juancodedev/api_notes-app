from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    name: str
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    name: str
    model_config = {
        "from_attributes": True
    }


class NoteCreate(BaseModel):
    title: str
    content: str

class NoteResponse(NoteCreate):
    id: int
    user_id: int
    locked: bool

class UserLogin(BaseModel):
    username: str
    password: str
