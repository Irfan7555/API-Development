
from fastapi import APIRouter, Depends, HTTPException, status   # Importing the necessary modules
from sqlalchemy.orm import Session
from typing import List
import models
from database import get_db
from schemas import PostCreate, Post
from oauth2 import create_access_token, verify_access_token, get_current_user

router = APIRouter(
    prefix="/posts",
    tags=["Posts"] 
)

@router.get("/", response_model= List[Post])
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    # posts = db.query(models.Post)
    print(posts)
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_post(post: PostCreate, db: Session = Depends(get_db), user_id: int= Depends(get_current_user)):
    print(user_id)
    new_post = models.Post(**post.model_dump())
    db.add(new_post)    # For actually adding the data to the database
    db.commit()
    db.refresh(new_post)
    return new_post
    
@router.delete("/{id}", response_model=Post)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
    post.delete(synchronize_session=False)
    db.commit()
    return {"data": f"Post with id {id} deleted successfully"}

@router.put("/{id}", response_model=Post)
def update_post(id: int, updated_post: PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")

    # Ensure the id is included in the update data
    update_data = updated_post.model_dump()
    update_data["id"] = id  # Explicitly setting the ID

    post_query.update(update_data, synchronize_session=False)
    db.commit()

    return post_query.first()
