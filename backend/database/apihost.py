from fastapi import FastAPI, HTTPException, Depends
from pydantic import basemodel
from typing import List, Annotated


app = FastAPI()

