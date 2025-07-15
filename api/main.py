from fastapi import FastAPI
from pydantic import BaseModel
from api.logic import generate_blog_post

app = FastAPI()

class BlogRequest(BaseModel):
    topic: str
    style: str = "informative"
    length: str = "short"

@app.get("/")
def read_root():
    return {"message": "Welcome to the SEO Auto Blogger API"}

@app.post("/generate-blog")
def generate_blog(data: BlogRequest):
    result = generate_blog_post(data.topic, data.style, data.length)
    return {"blog_post": result}
