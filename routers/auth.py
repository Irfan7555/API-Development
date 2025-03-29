from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from database import get_db
from schemas import UserLogin
from utils import verify
import models
from oauth2 import create_access_token

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login")
def login(user_credentials: UserLogin, db: Session= Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
    if not verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")

    access_token = create_access_token(data= {"user_id":user.id})


    return {"access_token": access_token, "token_type": "bearer"}

