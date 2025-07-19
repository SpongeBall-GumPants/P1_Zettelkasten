from fastapi.testclient import TestClient
import pytest
from sqlmodel import SQLModel, create_engine
from backend.app import app
import backend.db_models   # noqa: F401
import sys
print("python executable:", sys.executable)
# use the same DATABASE_URL or a test DB
client = TestClient(app)
engine = create_engine("postgresql://synapse_user:…@localhost/synapse_db")


@pytest.fixture(autouse=True)
def init_db():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)


def test_register_user():
    res = client.post("/auth/register", json={
        "username": "alice",
        "email": "alice@example.com",
        "password": "Secret123!"
    })
    assert res.status_code == 201
    data = res.json()
    assert data["username"] == "alice"
    assert "id" in data
