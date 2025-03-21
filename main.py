from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from connection import posts as my_posts, conn, cursor
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


# my_posts = [{"id": 1, "title": "Post 1", "content": "This is a post", "published": True},
#             {"id": 2,"title": "Post 2", "content": "This is another post", "published": False}]

def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post
    return None

def find_post_index(id):
    for i, post in enumerate(my_posts):
        if post["id"] == id:
            print(f"i = {i}, post  = {post}" )
            return i
    return None

@app.get("/")
def read_root():
    return {"data": my_posts}


@app.get("/posts")
def get_posts():
    return {"posts": my_posts}

# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_post(new_post: Post):
#     post_dict = new_post.model_dump()
#     post_dict["id"] = len(my_posts) + 1
#     print(len(my_posts))
#     my_posts.append(post_dict)
#     return {"data": post_dict}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES ({post.title}, {post.content}, {post.published})""")

        # cursor.execute/itle,post.content, post.published)) # %s is a variable value that will be replaced by the values in the tuple 
    # new_post  = cursor.fetchone()
    # conn.commit() # commit the transaction and save the changes
    print(post.model_dump()) # Another way to get the data from the post object
    new_post = models.Post(**post.model_dump())
    db.add(new_post)    # For actually adding the data to the database
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}
    # return {"data": new_post} 
    
    

    
@app.get("/posts/latest")
def get_latest_post():
    post = len(my_posts)
    return {"data": len(my_posts[-1])}


# @app.get("/posts/{id}")
# def get_post(id: int, response: Response):
#     print(type(id))
#     post = find_post(id)
#     if not post:
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return {"data": f"Post with id {id} not found"}
#         raise HTTPException(status_code=404, detail=f"Post with id {id} not found")

#     return {"data": post }    


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    # cursor.execute("SELECT * FROM posts WHERE id = %s", [id]) 
    # cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))

    post = cursor.fetchone()

    return {"data": post}



@app.delete("/posts/{id}")
def delete_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
    my_posts.remove(post)
    return {"data": f"Post with id {id} deleted successfully"}

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    post_index = find_post_index(id)
    if post_index is None:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
    post_dict =  post.model_dump()
    post_dict["id"] = id
    my_posts[post_index] =post_dict
    return {"data": post_dict}


@app.get("/sql/posts/")
def sql_get_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"data": posts}

# Testing sqlachemy
@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    # posts = db.query(models.Post)
    print(posts)
    return {"data": posts}
