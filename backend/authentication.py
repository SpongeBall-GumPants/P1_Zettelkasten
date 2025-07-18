from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from passlib.context import CryptContext

from db import get_session
from models import User
from schemas import UserCreate

router = APIRouter(prefix="/auth", tags=["auth"])
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register", response_model=User, status_code=201)
def register(user_in: UserCreate, session: Session = Depends(get_session)):
    # Check for existing username/email
    stmt = select(User).where(
        (User.username == user_in.username) | (User.email == user_in.email)
    )
    if session.exec(stmt).first():
        raise HTTPException(status_code=400, detail="Username or email already registered")

    hashed = pwd_ctx.hash(user_in.password)
    user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
