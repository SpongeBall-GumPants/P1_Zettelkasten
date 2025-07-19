import os
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine
from backend.app import app
import db_models   # noqa: F401, registers your User table
from backend.db import get_session

# Use the same DATABASE_URL from your .env
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=False)
client = TestClient(app)


@pytest.fixture(autouse=True)
def init_db():
    # Recreate tables
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    # Seed a known user
    from passlib.context import CryptContext
    pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed = pwd_ctx.hash("Secret123!")
    with next(get_session()) as session:
        session.add(db_models.User(
            username="alice",
            email="alice@example.com",
            hashed_password=hashed
        ))
        session.commit()
    yield
    SQLModel.metadata.drop_all(engine)


def test_login_success():
    """Valid credentials should return 200 and a bearer token."""
    res = client.post("/auth/login", json={
        "username": "alice",
        "password": "Secret123!"
    })
    assert res.status_code == 200, res.text
    data = res.json()
    assert "access_token" in data
    assert data.get("token_type") == "bearer"


def test_login_failure():
    """Bad credentials should return 401 Unauthorized."""
    res = client.post("/auth/login", json={
        "username": "alice",
        "password": "WrongPass!"
    })
    assert res.status_code == 401
