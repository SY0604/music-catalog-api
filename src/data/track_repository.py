from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Optional
from bson import ObjectId
from datetime import datetime
from fastapi import HTTPException
from pymongo import ASCENDING

class TrackRepository:
    """Data access layer for track operations."""
    
    def __init__(self, connection_string: str, database_name: str):
        self.mongodb_client = AsyncIOMotorClient(connection_string)
        self.database = self.mongodb_client[database_name]
        self.tracks_collection = self.database["tracks"]

    async def find_existing_track(self, track_data: dict) -> Optional[dict]:
        """Check if a track already exists in the database."""
        track_title = track_data.get("title", "")
        track_artist = track_data.get("artist", "")
        existing_track = await self.tracks_collection.find_one({
            "title": track_title, 
            "artist": track_artist
        })
        if existing_track:
            return dict(existing_track)
        return None

    async def create_track(self, track_data: dict) -> str:
        """Insert a new track and return its ID."""
        insert_result = await self.tracks_collection.insert_one(track_data)
        return str(insert_result.inserted_id)

    async def retrieve_track(self, track_id: str) -> Optional[dict]:
        """Retrieve a track by its unique identifier."""
        try:
            object_id = ObjectId(track_id)
        except Exception:
            return None

        track_document = await self.tracks_collection.find_one({"_id": object_id})
        if track_document:
            track_document = dict(track_document)
            track_document["id"] = str(track_document["_id"])
        return track_document

    async def modify_track(self, track_id: str, updates: dict):
        """Update an existing track with new data."""
        try:
            object_id = ObjectId(track_id)
        except Exception:
            return False

        # Perform atomic update operation
        updated_track = await self.tracks_collection.find_one_and_update(
            {"_id": object_id},
            {"$set": updates},
            return_document=True
        )

        return bool(updated_track)

    async def remove_track(self, track_id: str):
        """Delete a track from the database."""
        try:
            object_id = ObjectId(track_id)
        except Exception:
            return False

        deleted_track = await self.tracks_collection.find_one_and_delete({"_id": object_id})
        return bool(deleted_track)

    async def query_tracks(self, search_criteria: dict) -> List[dict]:
        """Search for tracks based on various criteria."""
        query_filter = {}

        # Handle date range filtering
        if search_criteria.get("from_date") or search_criteria.get("to_date"):
            query_filter["release_date"] = {}
            if search_criteria.get("from_date"):
                query_filter["release_date"]["$gte"] = search_criteria["from_date"].isoformat()
            if search_criteria.get("to_date"):
                query_filter["release_date"]["$lte"] = search_criteria["to_date"].isoformat()

        # Handle external link filtering
        if search_criteria.get("external_link", False):
            query_filter["external_link"] = search_criteria["external_link"]

        # Handle full-text search
        if search_criteria.get("search_terms", False):
            query_filter["$text"] = {"$search": " ".join(search_criteria["search_terms"])}

        # Execute query
        query_cursor = self.tracks_collection.find(query_filter)

        # Sort by relevance if using text search
        if "$text" in query_filter:
            query_cursor = query_cursor.sort([("score", {"$meta": "textScore"})])

        # Limit results and convert to list
        track_results = await query_cursor.to_list(length=100)
        for track in track_results:
            track["id"] = str(track["_id"])
        return track_results
