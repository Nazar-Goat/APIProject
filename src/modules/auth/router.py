from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from starlette import status

from src.modules.auth.schemas import (
    UserRegisterSchema,
    UserRegisterOutSchema,
    UserLoginSchema,
    CurrentUserSchema,
)
from src.modules.auth.auth_dependencies import get_user_service as user_service
from src.modules.auth.service import UserService
from src.dependencies import AUS


auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post(
    "/register",
    response_model=UserRegisterOutSchema,
    status_code=status.HTTP_201_CREATED,
)
async def register(
        register_data: UserRegisterSchema,
        service: UserService = Depends(user_service),
):
    user_data = await service.register_user(register_data)
    return user_data

@auth_router.post(
    "/login",
    status_code=status.HTTP_200_OK
)
async def login(
        login_data: UserLoginSchema,
        service: UserService = Depends(user_service),
):
    token = await service.login_user(login_data)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"access": token}
    )

@auth_router.get(
    "/profile",
    status_code=status.HTTP_200_OK,
    response_model=CurrentUserSchema,
)
async def profile(
current_user: AUS
):
    return current_user