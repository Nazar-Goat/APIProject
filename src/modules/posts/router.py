from fastapi import APIRouter


posts_router = APIRouter(prefix="/posts", tags=["posts"])