from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# class Post(BaseModel):
#     id: Optional[int] = None
#     title: str
#     content: Optional[str] = None
#     published: bool = True
#
# class CreatePost(BaseModel):
#     title: str
#     content: str
#     published: bool = True
#
# class UpdatedPost(BaseModel):
#     title: str
#     content: str
#     published: bool = True

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime


class Post(PostBase):
    id: int
    owner_id: int
    created_at: datetime
    owner: UserOut

    class Config:
        # orm_mode = True
        from_attributes = True
        # This is used to convert the SQLAlchemy object to a Pydantic model.

class UserCreate(BaseModel):
    email: EmailStr
    password: str




class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None