from loguru import logger
from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

_client: AsyncMongoClient | None = None
_db: AsyncDatabase | None = None


def get_database() -> AsyncDatabase:
    if _db is None:
        logger.warning("Database not initialized")
        raise RuntimeError("Database not initialized")

    return _db


async def connect_to_mongo(
    mongo_uri: str,
    db_name: str,
) -> None:
    global _client, _db

    _client = AsyncMongoClient(
        mongo_uri,
        maxPoolSize=50,
        minPoolSize=10,
    )

    _db = _client[db_name]


async def close_mongo_connection() -> None:
    global _client

    if _client is not None:
        await _client.close()
        _client = None