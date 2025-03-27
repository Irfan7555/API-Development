from pydantic import BaseModel
from typing import Optional

class Post(BaseModel):
    id: Optional[int] = None
    title: str
    content: Optional[str] = None
    published: bool = True