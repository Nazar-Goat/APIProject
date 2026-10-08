from fastapi import Depends

from src.modules.auth.repository import UserRepository
from src.modules.auth.service import UserService
from src.dependencies import get_jwt_service
from src.jwt_service import JWTService


def get_user_repository() -> UserRepository:
    return UserRepository()

def get_user_service(repo: UserRepository = Depends(get_user_repository), jwt_service: JWTService = Depends(get_jwt_service) ) -> UserService:
    return UserService(repo, jwt_service)
