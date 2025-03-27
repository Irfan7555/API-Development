from executing import cache
from fastapi import FastAPI, status, HTTPException
import models
from database import engine, get_db  
from sqlalchemy.orm import Session
from fastapi import Depends
from schemas import PostCreate, Post, UserCreate, UserOut
from typing import List
from utils import hash
from routers import post, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)



