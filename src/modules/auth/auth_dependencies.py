from fastapi import Depends

from src.modules.auth.repository import UserRepository
from src.modules.auth.service import UserService


def get_user_repository() -> UserRepository:
    return UserRepository()

def get_user_service(repo: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(repo)
