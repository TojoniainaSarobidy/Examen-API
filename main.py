from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse, HTMLResponse
from starlette.exceptions import HTTPException as HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime

app = FastAPI()
posts_db = []
class Post(BaseModel):
    author: str
    title: str
    content: str
    creation_datetime: datetime

# Q1
@app.get("/ping", response_class=PlainTextResponse)
async def ping():
    return PlainTextResponse(content="pong", status_code=200)

# Q2
@app.get("/home", response_class=HTMLResponse)
async def home():
    html_content = "<html><body><h1>Welcome home!</h1></body></html>"
    return HTMLResponse(content=html_content, status_code=200)


# Q3
@app.exception_handler(HTTPException)
async def custom_404_handler(request: Request, exception: HTTPException):
    if exception.status_code == 404:
        html_404 = "<html><body><h1>404 NOT FOUND</h1></body></html>"
        return HTMLResponse(content=html_404, status_code=404)
    return PlainTextResponse(str(exception.detail), status_code=exception.status_code)

# Q4
@app.post("/posts", status_code=201)
async def create_posts(new_posts: List[Post]):
    for post in new_posts:
        posts_db.append(post)
    return posts_db

# Q5
@app.get("/posts")
async def get_posts():
    return posts_db

# Q6
@app.put("/posts")
async def update_or_add_posts(updated_posts: List[Post]):
    titles_in_db = {post.title: post for post in posts_db}
    for new_post in updated_posts:
        if new_post.title in titles_in_db:
            index = posts_db.index(titles_in_db[new_post.title])
            posts_db[index] = new_post
        else:
            posts_db.append(new_post)
    return posts_db

# bonus
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse
import base64

app = FastAPI()

@app.get("/ping", response_class=PlainTextResponse)
def ping():
    return "pong"

@app.get("/ping/auth", response_class=PlainTextResponse)
def ping_auth(request: Request):
    auth_header = request.headers.get("Authorization")
    if auth_header is None or not auth_header.startswith("Basic "):
        raise HTTPException(status_code=401, detail="Authentification requise")
    encoded_credentials = auth_header.split(" ")[1]
    try:
        decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8")
    except Exception:
        raise HTTPException(status_code=401, detail="Identifiants mal formés")
    if decoded_credentials == "admin:123456":
        return "pong"
    else:
        raise HTTPException(status_code=401, detail="Identifiants invalides")