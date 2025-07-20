# backend/app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from backend.authentication import router as auth_router  # Fixed import
from backend.notes import router as notes_router  # Fixed import
from sqlmodel import SQLModel, create_engine

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# include your auth routes
app.include_router(auth_router)

# include your notes routes
app.include_router(notes_router)

engine = create_engine(DATABASE_URL, echo=True)


@app.get("/ping")
async def ping():
    return {"pong": True}


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
