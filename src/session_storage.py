from redis.asyncio import Redis
from redis.exceptions import ConnectionError

from src.config import settings


class SessionStorage:
    __KEY_TTL = int(settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    __FAILED_LOGIN_ATTEMPTS_TIMEOUT = int(settings.FAILED_LOGIN_ATTEMPTS_TIMEOUT * 60)
    __WSS_KEY_TTL = settings.WSS_TOKEN_TTL

    def __init__(self):
        self.__redis_auth_db = Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASS,
            db=settings.REDIS_AUTH_DB,
        )

    async def insert_token(self, user_token: str, user_info: str) -> None:
        await self.__redis_auth_db.setex(
            f"user:{user_token}", self.__KEY_TTL, user_info
        )

    async def get_user_by_token(self, user_token: str) -> str:
        result = await self.__redis_auth_db.get(f"user:{user_token}")
        return result