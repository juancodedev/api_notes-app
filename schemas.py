from pydantic import BaseModel
from typing import Optional, List

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
    locked: Optional[bool] = False
    tags: List[str] = []

class NoteResponse(NoteCreate):
    id: int
    user_id: int
    locked: bool

class UserLogin(BaseModel):
    username: str
    password: str
class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id: int

    class Config:
        orm_mode = True