from uuid import uuid4

from fastapi import HTTPException, status
from loguru import logger

from src.modules.auth.repository import UserRepository
from src.modules.auth.schemas import (
    UserRegisterSchema,
    UserRegisterOutSchema,
    UserLoginSchema, CurrentUserSchema,
)

from src.security import get_password_hash, verify_password
from src.dependencies import jwt_service, credentials_exception, get_current_user



class UserService:
    def __init__(self, repo: UserRepository):
        self._repo = repo

    async def register_user(self, register_user_data: UserRegisterSchema) -> UserRegisterOutSchema:
        user_exists = await self._repo.get_user_by_email(register_user_data.email)

        if user_exists is not None:
            logger.warning(
                "User creation failed.Client already exists. ",
                user_exists_id=user_exists.id
            )

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this identity already exists.",
            )

        hashed_password = get_password_hash(register_user_data.password)

        new_user = await self._repo.create_user(
            username=register_user_data.username,
            email=register_user_data.email,
            password_hash=hashed_password,
        )

        return UserRegisterOutSchema.model_validate(new_user, from_attributes=True)

    async def login_user(self, login_data: UserLoginSchema) -> str:
        user_exists = await self._repo.get_user_by_email(login_data.email)

        if user_exists is None:
            logger.warning("User login failed")
            raise credentials_exception

        equal_passwords = verify_password(login_data.password, user_exists.password_hash)

        if not equal_passwords:
            logger.warning("User login failed")
            raise credentials_exception

        session_id = uuid4().hex
        token = await jwt_service.create_session_token(
            subject=session_id,
            data={
                'id': user_exists.id,
                'email': user_exists.email,
                'username': user_exists.username,
            },
            token_type='access',
        )

        return token

