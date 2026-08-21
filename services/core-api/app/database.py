import logging
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

logger = logging.getLogger(__name__)

class MongoDB:
    client: AsyncIOMotorClient = None
    db = None

db_instance = MongoDB()

async def connect_to_mongo():
    logger.info(f"Connecting to MongoDB at {settings.MONGODB_URI}...")
    db_instance.client = AsyncIOMotorClient(settings.MONGODB_URI)
    db_instance.db = db_instance.client[settings.DATABASE_NAME]
    logger.info(f"Connected to MongoDB database: {settings.DATABASE_NAME}")

async def close_mongo_connection():
    logger.info("Closing MongoDB connection...")
    if db_instance.client:
        db_instance.client.close()
        logger.info("MongoDB connection closed.")

def get_database():
    return db_instance.db

# Collection accessor helpers
def get_assets_collection():
    return db_instance.db["assets"]

def get_lessees_collection():
    return db_instance.db["lessees"]

def get_leases_collection():
    return db_instance.db["leases"]

def get_invoices_collection():
    return db_instance.db["invoices"]

def get_telemetry_collection():
    return db_instance.db["telemetry_records"]

def get_agent_logs_collection():
    return db_instance.db["agent_action_logs"]
