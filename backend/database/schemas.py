from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    email: str
    password: str
    name: str
    username: str

class EmailCheck(BaseModel): 
    email: str

class UserSignIn(BaseModel):
    email: str
    password: str
    
class SetUp(BaseModel):
    email: str
    body_part: str
    had_this_problem_before: bool
    previous_problem_date: Optional[str] = None
    what_helped_before: Optional[str] = None

    had_physical_therapy_before: bool
    previous_unrelated_problem: Optional[str] = None
    
    opinion_cause: str
    pain_worse: str
    pain_better: str
    goal_for_pt: str
