from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.database import Base, User
from backend.database.dependency import get_db
from fastapi.middleware.cors import CORSMiddleware
from backend.database.schemas import UserCreate
from passlib.context import CryptContext

from . import schemas, dependency, database
app = FastAPI()



origins = [
    "http://localhost",
    "http://localhost:3000", # The address of your React frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods (GET, POST, etc.)
    allow_headers=["*"], # Allows all headers
)




