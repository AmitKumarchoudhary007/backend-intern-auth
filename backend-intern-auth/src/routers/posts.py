from fastapi import APIRouter, Depends
from ..auth import get_current_user




router = APIRouter(prefix="/api", tags=["posts"])



sample_posts = [
         {"post_id": 1, "title": "Welcome to LawVriksh", "contentSnippet": "Intro to the platform."},
     {"post_id": 2, "title": "How to file a case", "contentSnippet": "Step-by-step guidelines..."}
]





@router.get("/posts")

def get_posts(user = Depends(get_current_user)):
    return sample_posts
