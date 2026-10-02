from fastapi import APIRouter

from src.modules.auth.router import auth_router
from src.modules.posts.router import posts_router


api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth_router)
api_router.include_router(posts_router)

