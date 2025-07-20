import os
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine
from backend.app import app  # Fixed import
from backend import db_models  # Fixed import
from backend.db import get_session  # Fixed import
from passlib.context import CryptContext


DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=False)
client = TestClient(app)


@pytest.fixture(autouse=True)
def init_db_and_token():
    # 1) Recreate the schema
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

    # 2) Seed a test user
    pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed = pwd_ctx.hash("Secret123!")
    with next(get_session()) as session:
        user = db_models.User(username="alice", email="a@a.com", hashed_password=hashed)  # Fixed reference
        session.add(user)
        session.commit()
        session.refresh(user)

    # 3) Login to get a Bearer token
    res = client.post("/auth/login", data={"username": "alice", "password": "Secret123!"})
    token = res.json()["access_token"]
    yield token

    # 4) Teardown
    SQLModel.metadata.drop_all(engine)


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


def test_create_and_list_notes(init_db_and_token):
    token = init_db_and_token

    # Create
    r1 = client.post(
        "/notes",
        headers=auth_headers(token),
        json={"title": "Test Note", "content": "Hello world"}
    )
    assert r1.status_code == 201

    # List
    r2 = client.get("/notes", headers=auth_headers(token))
    assert r2.status_code == 200
    data = r2.json()
    assert isinstance(data, list)
    assert data and data[0]["title"] == "Test Note"


def test_get_update_delete_note(init_db_and_token):
    token = init_db_and_token

    # Seed a note
    client.post("/notes",
        headers=auth_headers(token),
        json={"title": "Seed", "content": "Data"}
    )

    # GET by ID
    r1 = client.get("/notes/1", headers=auth_headers(token))
    assert r1.status_code == 200
    assert r1.json()["content"] == "Data"

    # UPDATE
    r2 = client.put("/notes/1",
        headers=auth_headers(token),
        json={"title": "Updated", "content": "New"}
    )
    assert r2.status_code == 200
    assert r2.json()["title"] == "Updated"

    # DELETE
    r3 = client.delete("/notes/1", headers=auth_headers(token))
    assert r3.status_code == 204

    # GET after delete → 404
    r4 = client.get("/notes/1", headers=auth_headers(token))
    assert r4.status_code == 404