import os
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine
from backend.app import app
import backend.db_models   # noqa: F401, registers your User table
from backend.db import get_session


DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=False)
client = TestClient(app)


@pytest.fixture(autouse=True)
def init_db():
    # Recreate schema each test
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

    # Seed a known user
    from passlib.context import CryptContext
    pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed = pwd_ctx.hash("Secret123!")
    with next(get_session()) as session:
        session.add(backend.db_models.User(
            username="alice",
            email="alice@example.com",
            hashed_password=hashed
        ))
        session.commit()
    yield

    # Tear down
    SQLModel.metadata.drop_all(engine)


def test_login_success():
    """Correct credentials should yield 200 + bearer token."""
    res = client.post("/auth/login", data={
        "username": "alice",
        "password": "Secret123!"
    })
    assert res.status_code == 200, res.text
    body = res.json()
    assert "access_token" in body
    assert body.get("token_type") == "bearer"


def test_login_failure():
    """Wrong password must return 401 Unauthorized."""
    res = client.post("/auth/login", data={
        "username": "alice",
        "password": "WrongPassword"
    })
    assert res.status_code == 401
