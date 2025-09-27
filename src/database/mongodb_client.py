from motor.motor_asyncio import AsyncIOMotorClient
import os
import asyncio
import logging

logger = logging.getLogger(__name__)

def create_mongodb_client():
    """Create and return MongoDB async client with connection settings."""
    connection_string = os.getenv("MONGODB_CONNECTION", "mongodb://localhost:27017")
    return AsyncIOMotorClient(
        connection_string,
        serverSelectionTimeoutMS=5000,  # 5 second timeout
        connectTimeoutMS=5000,
        socketTimeoutMS=5000,
        maxPoolSize=10,
        retryWrites=True
    )

def get_database():
    """Get the configured database instance."""
    client = create_mongodb_client()
    database_name = os.getenv("DATABASE_NAME", "musicdb")
    return client[database_name]

async def wait_for_mongodb(max_retries=10, delay=2):
    """Wait for MongoDB to be available with retry logic."""
    for attempt in range(max_retries):
        try:
            client = create_mongodb_client()
            # Test the connection
            await client.admin.command('ping')
            logger.info("Successfully connected to MongoDB")
            return True
        except Exception as e:
            logger.warning(f"MongoDB connection attempt {attempt + 1}/{max_retries} failed: {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(delay)
            else:
                logger.error("Failed to connect to MongoDB after all retries")
                raise
    return False
