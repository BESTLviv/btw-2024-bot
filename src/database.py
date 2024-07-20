from motor.motor_asyncio import AsyncIOMotorClient


async def init_db(mongo_uri):
    client = AsyncIOMotorClient(mongo_uri)
    db = client.get_database()

    users_collection = db['users']
    await users_collection.create_index([("user_id", 1)], unique=True)
    return db
