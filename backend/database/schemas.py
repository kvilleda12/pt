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
    
class BodyPartSelection(BaseModel):
    body_part: str
    email: str
