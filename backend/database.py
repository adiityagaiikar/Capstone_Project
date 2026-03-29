import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/roadsafetydb")

motor_client: AsyncIOMotorClient = None


async def init_db(document_models: list):
    """
    Initialize the async MongoDB connection and register Beanie documents.
    Compatible with Beanie 1.x and 2.x.
    """
    import beanie
    global motor_client
    motor_client = AsyncIOMotorClient(MONGO_URI)

    # Parse the database name from the URI (handles Atlas URIs with query params too)
    db_name = MONGO_URI.split("/")[-1].split("?")[0] or "roadsafetydb"
    database = motor_client[db_name]

    await beanie.init_beanie(
        database=database,
        document_models=document_models,
    )
    print(f"[DB] Connected -> MongoDB database: '{db_name}'")


async def close_db():
    global motor_client
    if motor_client:
        motor_client.close()
        print("[DB] MongoDB connection closed.")
