from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError # noqa: F401
from sqlmodel import Session, select
from typing import List
from datetime import datetime
import os

from backend.db import get_session  # Fixed import
from backend.db_models import Note, User  # Fixed import
from backend.schemas import NoteCreate, NoteRead  # Fixed import

# JWT & Auth dependencies
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

router = APIRouter(prefix="/notes", tags=["notes"])

def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)) -> User:
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exc
    except JWTError:
        raise credentials_exc
    user = session.exec(select(User).where(User.username == username)).first()
    if not user:
        raise credentials_exc
    return user

@router.post("", response_model=NoteRead, status_code=201)
def create_note(
    note_in: NoteCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    note = Note(
        title=note_in.title,
        content=note_in.content,
        user_id=current_user.id
    )
    session.add(note)
    session.commit()
    session.refresh(note)
    return note

@router.get("", response_model=List[NoteRead])
def list_notes(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    notes = session.exec(select(Note).where(Note.user_id == current_user.id)).all()
    return notes

@router.get("/{note_id}", response_model=NoteRead)
def read_note(
    note_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    note = session.get(Note, note_id)
    if not note or note.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.put("/{note_id}", response_model=NoteRead)
def update_note(
    note_id: int,
    note_in: NoteCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    note = session.get(Note, note_id)
    if not note or note.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Note not found")
    note.title = note_in.title
    note.content = note_in.content
    note.updated_at = datetime.utcnow()
    session.add(note)
    session.commit()
    session.refresh(note)
    return note

@router.delete("/{note_id}", status_code=204)
def delete_note(
    note_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    note = session.get(Note, note_id)
    if not note or note.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Note not found")
    session.delete(note)
    session.commit()