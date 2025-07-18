# in backend/app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from sqlmodel import SQLModel, create_engine
import models   # noqa: F401
from authentication import router as auth_router


load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI()
app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:3000"],
  allow_methods=["*"],
  allow_headers=["*"],
)


@app.get("/ping")
async def ping():
    return {"pong": True}

engine = create_engine(DATABASE_URL, echo=True)


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


app.include_router(auth_router)
