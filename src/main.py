from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from beanie import init_beanie

from src.config import settings
from src.router import api_router
from src.database import connect_to_mongo, close_mongo_connection, get_database
from src.modules.auth.models import User
from src.modules.articles.models import Article


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo(settings.MONGO_URI, settings.MONGO_DB_NAME)
    await init_beanie(
        database=get_database(),
        document_models=[User, Article],
    )
    yield
    await close_mongo_connection()


if settings.ENVIRONMENT == "DEV":
    app = FastAPI(
        title=settings.APP_NAME,
        lifespan=lifespan
    )

    @app.get("/")
    async def root():
        return {"Hello": "World"}

    app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.APP_PORT, log_config=None)
