
from fastapi import APIRouter, Depends, HTTPException, status   # Importing the necessary modules
from sqlalchemy.orm import Session
from typing import List
import models
from database import get_db
from schemas import PostCreate, Post
from oauth2 import get_current_user

router = APIRouter(
    prefix="/posts",
    tags=["Posts"] 
)

@router.get("/", response_model= List[Post])
def test_posts(db: Session = Depends(get_db), current_user: int= Depends(get_current_user)):
    posts = db.query(models.Post).all()
    # posts = db.query(models.Post)
    print(posts)
    return posts


@router.get("/{id}", response_model=Post)
def get_one_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()  # Fix filter condition
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
    return post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_post(post: PostCreate, db: Session = Depends(get_db), current_user: int= Depends(get_current_user)):
    # print(current_user.id)
    new_post = models.Post(owner_id = current_user.id,**post.model_dump())
    db.add(new_post)    # For actually adding the data to the database
    db.commit()
    db.refresh(new_post)
    print(current_user)
    return new_post


@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
    print(f"Current User ID: {current_user.id}, Post Owner ID: {post.owner_id}")
    if post.owner_id != current_user.id:  # Ensure current_user has an id attribute
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not Authorized to perform the proposed operation")

    post_query.delete(synchronize_session=False)
    db.commit()

    return {"message": f"Post with id {id} deleted successfully"}

@router.put("/{id}", response_model=Post)
def update_post(id: int, updated_post: PostCreate, db: Session = Depends(get_db), current_user: int= Depends(get_current_user)):
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
