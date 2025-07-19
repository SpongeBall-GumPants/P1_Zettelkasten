from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from passlib.context import CryptContext
import os
from backend.db import get_session
from backend.db_models import User
from backend.schemas import UserCreate
from datetime import datetime, timedelta
from jose import jwt  # noqa: F401


router = APIRouter(prefix="/auth", tags=["auth"])
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15


@router.post("/register", response_model=User, status_code=201)
def register(user_in: UserCreate, session: Session = Depends(get_session)):
    # Check for username/email
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


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    stmt = select(User).where(User.username == form_data.username)
    user = session.exec(stmt).first()
    if not user or not pwd_ctx.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
