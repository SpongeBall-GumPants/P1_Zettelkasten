from pydantic import BaseModel, EmailStr, constr
from datetime import datetime


class UserCreate(BaseModel):
    username: constr(min_length=3, max_length=50)
    email: EmailStr
    password: constr(min_length=8)


class NoteCreate(BaseModel):
    title: str
    content: str


class NoteRead(NoteCreate):
    id: int
    created_at: datetime
    updated_at: datetime
    user_id: int
