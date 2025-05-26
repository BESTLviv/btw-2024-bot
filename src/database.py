from motor.motor_asyncio import AsyncIOMotorClient
import config


async def init_db():
    client = AsyncIOMotorClient(config.MONGO_URI)
    db = client[config.DB_NAME]

    users_collection = db['users']
    await users_collection.create_index([("user_id", 1)], unique=True)
    return db
