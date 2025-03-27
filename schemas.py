from pydantic import BaseModel, EmailStr
from datetime import datetime


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

class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        # orm_mode = True
        from_attributes = True
        # This is used to convert the SQLAlchemy object to a Pydantic model.

class UserCreate(BaseModel):
    email: EmailStr
    password: str



class UserOut(BaseModel):
    id: int
    email: EmailStr

