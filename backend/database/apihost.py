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

#encrypting the user password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


# --- AUTH ROUTES ---

@app.post("/api/auth/check-email")
def check_email(payload: schemas.EmailCheck, db: Session = Depends(dependency.get_db)):
    db_user = db.query(database.User).filter(database.User.email == payload.email).first()
    return {"exists": db_user is not None}


@app.post("/api/auth/signup", status_code=201)
def signup(user: schemas.UserCreate, db: Session = Depends(dependency.get_db)):
    existing_user = db.query(database.User).filter(
        (database.User.email == user.email) | (database.User.username == user.username)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email or Username already registered")

    hashed_password = get_password_hash(user.password) 
    
    new_user = database.User(
        email=user.email, 
        hashed_password=hashed_password, 
        name=user.name,
        username=user.username
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return { 'ok': True, "message": "User created successfully!", "user_id": new_user.id }

@app.post("/api/auth/signin")
def signin(payload: schemas.UserSignIn, db: Session = Depends(dependency.get_db)):
    db_user = db.query(database.User).filter(database.User.email == payload.email).first()
    
    # Check user first to safely access password.
    if not db_user:
        return {
            'ok': False,
            "message": "Unable to sign in. Please verify your email and password.",
            }
    
    if not verify_password(payload.password, db_user.hashed_password):
        return {
            'ok': False,
            "message": "Unable to sign in. Please verify your email and password.",
            }
        
    return {
        'ok': True,
        "message": "Sign in successful", 
        "user": {
            "id": db_user.id,
            "email": db_user.email,
            "name": db_user.name,
            "username": db_user.username
        }
    }

# --- USER DATA ROUTES ---
# @app.post("/api/set-body-part")
# def set_body_part(payload: schemas.BodyPartSelection, db: Session = Depends(dependency.get_db)):
#     print(f"API received body part selection: {payload.body_part}")
#     # In a real application, you might want to save this to the database or perform other actions.
#     return {"status": "success", "body_part_received": payload.body_part}


