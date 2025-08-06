from pydantic import BaseModel
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
    previous_problem_date: str
    what_helped_before: str
    had_physical_therapy_before: bool
    previous_unrelated_problem: str
