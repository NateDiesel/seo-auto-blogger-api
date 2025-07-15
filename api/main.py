
from fastapi import FastAPI, Request
from pydantic import BaseModel
from api.logic import generate_blog_post  # assumes logic.py has a generate_blog_post function

app = FastAPI(title="SEO Auto Blogger API")

class BlogRequest(BaseModel):
    topic: str
    style: str = "informative"
    length: str = "short"

@app.get("/")
def read_root():
    return {"message": "Welcome to the SEO Auto Blogger API"}

@app.post("/generate-blog")
async def generate_blog(data: BlogRequest):
    result = generate_blog_post(topic=data.topic, style=data.style, length=data.length)
    return {"blog_post": result}
