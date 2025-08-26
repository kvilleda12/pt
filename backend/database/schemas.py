from __future__ import annotations
from datetime import date
from typing import Optional
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
    body_part: Optional[str] = None
    body_part_id: Optional[int] = None

    had_this_problem_before: Optional[bool] = False
    previous_problem_date: Optional[date] = None   
    what_helped_before: Optional[str] = None
    had_physical_therapy_before: Optional[bool] = False
    previous_unrelated_problem: Optional[str] = None

    class Config:
        extra = "ignore"