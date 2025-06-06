from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from connection import posts, conn, cursor
# from .models import models
import models
from database import engine, get_db  
from sqlalchemy.orm import Session
from fastapi import Depends

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Post(BaseModel):
    id: Optional[int] = None 
    title: str
    content: Optional[str] = None
    published: bool = True


@app.get("/posts")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    # posts = db.query(models.Post)
    print(posts)
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)    # For actually adding the data to the database
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}
    
@app.delete("/posts/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
    post.delete(synchronize_session=False)
    db.commit()
    return {"data": f"Post with id {id} deleted successfully"}

@app.put("/posts/{id}")
def update_post(id: int, updated_post: Post, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")

    # Ensure the id is included in the update data
    update_data = updated_post.model_dump()
    update_data["id"] = id  # Explicitly setting the ID

    post_query.update(update_data, synchronize_session=False)
    db.commit()

    return {"data": post_query.first()}

    