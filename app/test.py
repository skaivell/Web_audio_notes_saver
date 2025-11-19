from typing import List, Dict, Optional, Annotated
from fastapi import FastAPI, HTTPException, Path, Query, Body
app = FastAPI()

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index = True)
    age = Column(Integer)

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index = True)
    body = Column(String)
    author_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("User")


#@app.get("/items")
#async def items() -> List[Post]:
#    post_objects = []
#    for post in posts:
#        post_objects.append(Post(id=post["id"], title=post["title"], body=post["body"]))
#    return post_objects

@app.get("/items")
async def items() -> List[Post]:
    return [Post(**post) for post in posts]

@app.post("/items/add")
async def additem(post: PostCreate) -> Post:
    author = next((user for user in users if user["id"] == post.author_id), None)
    if not author:
        raise HTTPException(status_code=404, detail= "User not found")
    
    new_post_id = len(posts) + 1

    new_post = {"id": new_post_id, "title": post.title, "body": post.body, "author": author}
    posts.append(new_post)

    return Post(**new_post)

@app.get("/items/{id}")
async def item(id: Annotated[int, Path(...,title="Здесь указывается id поста", ge= 1, lt= 100)]) -> Post:
    for post in posts:
        if post["id"] == id:
            return Post(**post)
        
    raise HTTPException(status_code=404, detail="Post not found")

@app.get("/search")
async def search(post_id: Annotated[
    Optional[int],
    Query(title="ID of post to search for", ge=1, lt=50)
]) -> Dict[str, Optional[Post]]:
    if post_id:
        for post in posts:
            if post["id"] == post_id:
                return {"data": Post(**post)}
        raise HTTPException(status_code=404, detail="Post not found")
    else:
        return {"data": None}

@app.post("/user/add")
async def user_add(user: Annotated[
    UserCreate,
    Body(..., example={
        "name": "UserName",
        "age": 1
    })
]) -> User:
    new_user_id = len(users) + 1

    new_user = {"id": new_user_id, "name": user.name, "age": user.age}
    users.append(new_user)

    return User(**new_user)