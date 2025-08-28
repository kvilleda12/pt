from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.database import Base, User
from backend.database.dependency import get_db
from fastapi.middleware.cors import CORSMiddleware
from backend.database.schemas import UserCreate
from passlib.context import CryptContext
from backend.llm import llm_api
from datetime import datetime, time
from typing import Optional

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
VALID_CODES = {
    'n','c','ls','rs','lt','rt','lb','rb','a','b',
    'lh','rh','lq','rq','lc','rc','la','ra','e'
}

# Map 3D hitbox slugs to enum codes
BODY_SLUG_TO_CODE = {
    "neck": "n",
    "chest": "c",
    "right_shoulder": "rs",
    "left_shoulder": "ls",
    "right_tricep": "rt",
    "left_tricep": "lt",
    "right_bicep": "rb",
    "left_bicep": "lb",
    "abdomen": "a",
    "back": "b",
    "left_hamstring": "lh",
    "right_hamstring": "rh",
    "left_quad": "lq",
    "right_quad": "rq",
    "left_calf": "lc",
    "right_calf": "rc",
    "left_ankle": "la",
    "right_ankle": "ra",
}

def normalize_body_part(part: Optional[str]) -> str:

    if not part:
        return "e"
    key = part.strip().lower().replace(" ", "_")
    if key in BODY_SLUG_TO_CODE:
        return BODY_SLUG_TO_CODE[key]
    if key in VALID_CODES:
        return key
    return "e"

def to_datetime_or_none(d: Optional[datetime | str]) -> Optional[datetime]:
    """
    Accepts a date (pydantic-parsed) or ISO date string 'YYYY-MM-DD' and returns a datetime at 00:00.
    """
    if d is None:
        return None
    if isinstance(d, datetime):
        return d
    try:
        if hasattr(d, "year"):  # it's a date
            return datetime.combine(d, time.min)
        # it's a string
        return datetime.combine(datetime.fromisoformat(d).date(), time.min)
    except Exception:
        return None



# --- USER DATA ROUTES ---
@app.post("/api/set-up-user")
def set_up_user(payload: schemas.SetUp, db: Session = Depends(dependency.get_db)):
    # 1) find user
    db_user = db.query(database.User).filter(database.User.email == payload.email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Try to find the user's most recent report to update it
    existing_report = db.query(database.ProblemReport)\
        .filter(database.ProblemReport.user_id == db_user.id)\
        .order_by(database.ProblemReport.id.desc())\
        .first()
    
    # OPTION 1: Saving the actual Body Part Object on the PR. Find the parent Body object using the string from the payload
    # body_part_object = db.query(database.Body)\
    #     .filter(database.Body.id == payload.body_part)\
    #     .first()

    # if not body_part_object:
    #     print(f"Error in API Endpoint: parent Body object not found in database.")
    #     raise HTTPException(status_code=404, detail=f"Body part '{payload.body_part}' not found.")
    
    # Safely parse the date string into a datetime object if it exists
    parsed_date = None
    if payload.previous_problem_date:
        try:
            # Assuming the date format is YYYY-MM-DD
            parsed_date = datetime.strptime(payload.previous_problem_date, '%Y-%m-%d')
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Please use YYYY-MM-DD.")

    if existing_report:
        # --- UPDATE THE EXISTING REPORT ---
        existing_report.body_part_id = payload.body_part
        existing_report.had_this_problem_before = payload.had_this_problem_before
        existing_report.previous_problem_date = parsed_date
        existing_report.what_helped_before = payload.what_helped_before
        existing_report.had_physical_therapy_before = payload.had_physical_therapy_before
        existing_report.previous_unrelated_problem = payload.previous_unrelated_problem

        db.add(existing_report)
        db.commit()
        db.refresh(existing_report)

        return {
            "ok": True,
            "action": "updated",
            "report_id": existing_report.id,
            "body_part_code": body_code,
        }
    else:
        # --- CREATE A NEW REPORT ---
        print('creating new problem report')
        new_report = database.ProblemReport(
            user_id=db_user.id,
            body_part_id=payload.body_part,
            had_this_problem_before=payload.had_this_problem_before,
            previous_problem_date=parsed_date,
            what_helped_before=payload.what_helped_before,
            had_physical_therapy_before=payload.had_physical_therapy_before,
            previous_unrelated_problem=payload.previous_unrelated_problem,
            opinion_cause=payload.opinion_cause,
            pain_worse=payload.pain_worse,
            pain_better=payload.pain_better,
            goal_for_pt=payload.goal_for_pt,
        )
        
        db.add(new_report)
        db.commit()
        db.refresh(new_report)
        
        return {
            "ok": True,
            "report_id": new_report.id,
            "action": "created"
        }

# Llama Router for LLM API
app.include_router(llm_api.router, prefix = "/api/llm")
