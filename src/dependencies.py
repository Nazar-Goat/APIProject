from typing import Annotated

from fastapi import Depends, Cookie, HTTPException
from loguru import logger
from starlette import status

from src.config import settings
from src.modules.auth.schemas import  CurrentUserSchema
from src.session_storage import SessionStorage
from src.jwt_service import JWTService


def get_session_storage() -> SessionStorage:
    return SessionStorage()

def get_jwt_service(session_storage: SessionStorage = Depends(get_session_storage)) -> JWTService:
    return JWTService(session_storage=session_storage)

jwt_service: JWTService = get_jwt_service()


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
)

async def get_current_user(
    jw_token: str | None = Cookie(default=None, alias=settings.ACCESS_COOKIE_NAME),
) -> CurrentUserSchema:
    # logger.info("Try to get current user info") -> this log is too noisy,  this dependency is used in almost every endpoint
    if jw_token is None:
        raise credentials_exception

    user_data = await jwt_service.get_session_data(
        jw_token,
        expected_type="access",
    )
    if user_data is None:
        logger.warning(
            "User not found by token / invalid token. Raise Credentials Exception"
        )
        raise credentials_exception

    return CurrentUserSchema(**user_data)


AUS = Annotated[CurrentUserSchema, Depends(get_current_user)]
