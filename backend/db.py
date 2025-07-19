from sqlmodel import create_engine, Session
from dotenv import load_dotenv
import os, pathlib

# Load .env
load_dotenv(pathlib.Path(__file__).parent / ".env")

# Engine
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

# Dependency
def get_session():
    with Session(engine) as session:
        yield session
