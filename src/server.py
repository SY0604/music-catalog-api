from fastapi import FastAPI, HTTPException
from src.config.app_config import load_application_settings
from src.handlers.track_handler import track_router
from src.database.mongodb_client import get_database, wait_for_mongodb
from src.config.exception_handlers import handle_http_exceptions
from pymongo import ASCENDING
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app_settings = load_application_settings()

application = FastAPI(**app_settings.get_fastapi_config())

@application.on_event("startup")
async def initialize_application():
    """Initialize database indexes and application startup tasks."""
    logger.info("Starting Music Catalog API...")
    
    # Wait for MongoDB to be ready
    logger.info("Waiting for MongoDB connection...")
    await wait_for_mongodb()
    
    # Initialize database indexes
    logger.info("Creating database indexes...")
    tracks_collection = get_database()["tracks"]
    
    # Create text search index for full-text search capabilities
    await tracks_collection.create_index([("title", "text"), ("lyrics", "text")])
    logger.info("Created text search index")
    
    # Create unique compound index to prevent duplicate tracks
    await tracks_collection.create_index(
        [("title", ASCENDING), ("artist", ASCENDING)],
        unique=True,
        name="unique_track_identifier",
    )
    logger.info("Created unique constraint index")
    logger.info("🎵 Music Catalog API is ready!")

# Register exception handlers
application.add_exception_handler(HTTPException, handle_http_exceptions)

# Include API routes
application.include_router(track_router)
