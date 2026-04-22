from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import get_settings


settings = get_settings()
client = AsyncIOMotorClient(settings.mongodb_uri)


def get_database() -> AsyncIOMotorDatabase:
    return client[settings.mongodb_db]


async def close_database() -> None:
    client.close()
