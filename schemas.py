from pydantic import BaseModel
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

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

    class Config:
        orm_mode = True





