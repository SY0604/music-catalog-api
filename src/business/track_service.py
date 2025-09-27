from src.data.track_repository import TrackRepository
from src.integrations.genius_api import GeniusApiClient
from src.integrations.lrclib_api import LyricsLibraryClient
from src.integrations.spotify_api import SpotifyApiClient
from src.models.track_models import TrackCreation, TrackSummary
from typing import List, Optional
from fastapi import HTTPException, status
from bson import ObjectId

class TrackManagementService:
    """
    Core business logic for track management operations.

    Orchestrates interactions between API layer, data persistence,
    and external service integrations for comprehensive track management.
    """

    def __init__(self, data_repository: TrackRepository, metadata_provider: GeniusApiClient, 
                 lyrics_provider: LyricsLibraryClient, streaming_provider: SpotifyApiClient, cache_backend=None):
        """
        Initialize the service with required dependencies.

        Args:
            data_repository (TrackRepository): Database operations handler.
            metadata_provider (GeniusApiClient): Primary metadata source.
            lyrics_provider (LyricsLibraryClient): Lyrics content provider.
            streaming_provider (SpotifyApiClient): Additional metadata source.
            cache_backend (Optional): Caching layer for performance optimization.
        """
        self.data_repository = data_repository
        self.metadata_provider = metadata_provider
        self.lyrics_provider = lyrics_provider
        self.streaming_provider = streaming_provider
        self.cache_backend = cache_backend

    async def create_new_track(self, track_request: dict) -> Optional[dict]:
        """
        Create a new track with metadata enrichment.

        Process Flow:
        - Validate track doesn't already exist in database
        - Fetch metadata from Genius API
        - Enhance with LRCLib lyrics if available
        - Supplement with Spotify metadata
        - Persist enriched track data
        - Return complete track information

        Args:
            track_request (dict): Contains 'title' and 'artist' fields.

        Returns:
            dict: Complete track data with generated ID and metadata.

        Raises:
            HTTPException(409): Track already exists in the catalog.
            HTTPException(404): Track not found in external sources.
            HTTPException(500): Database persistence failure.
        """
        # 1. Verify track uniqueness
        duplicate_check = await self.data_repository.find_existing_track(track_request)
        if duplicate_check:
            raise HTTPException(
                status_code=409,
                detail=f"Track already exists in the catalog."
            )

        # 2. Retrieve base metadata from Genius
        genius_metadata = await self.metadata_provider.find_track_metadata(
            track_request["title"], track_request["artist"]
        )
        if not genius_metadata:
            raise HTTPException(
                status_code=404,
                detail=f"Track '{track_request['title']}' by '{track_request['artist']}' not found in external sources"
            )

        # 3. Construct base track document
        track_document = {
            "title": track_request["title"],
            "artist": track_request["artist"],
            "release_date": genius_metadata.get("release_date"),
            "external_link": genius_metadata.get("external_link"),
            "lyrics": genius_metadata.get("lyrics")  # Initial lyrics from Genius
        }

        # 4. Enhance with LRCLib lyrics (priority override)
        lrclib_response = await self.lyrics_provider.get_track_lyrics(
            track_request["title"], track_request["artist"]
        )
        if lrclib_response:
            # Prefer synchronized lyrics, fallback to plain text
            synchronized_lyrics = lrclib_response.get("syncedLyrics")
            plain_lyrics = lrclib_response.get("plainLyrics")

            if synchronized_lyrics:
                track_document["lyrics"] = synchronized_lyrics.split('\n')
            elif plain_lyrics:
                track_document["lyrics"] = plain_lyrics.split('\n')

        # 5. Supplement with Spotify metadata
        spotify_metadata = await self.streaming_provider.search_track_metadata(
            track_request["title"], track_request["artist"]
        )
        if spotify_metadata:
            # Fill missing metadata fields
            if not track_document.get("release_date") and spotify_metadata.get("release_date"):
                track_document["release_date"] = spotify_metadata["release_date"]
            if not track_document.get("external_link") and spotify_metadata.get("external_url"):
                track_document["external_link"] = spotify_metadata["external_url"]

            track_document["spotify_id"] = spotify_metadata.get("spotify_id")
            track_document["album_artwork"] = spotify_metadata.get("album_artwork")

        # 6. Persist to database
        track_id = await self.data_repository.create_track(track_document)
        if not track_id:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to save track to database."
            )
        
        track_document["id"] = track_id
        return track_document

    async def retrieve_track_details(self, track_id: str, page_number: int, page_size: int) -> Optional[dict]:
        """
        Retrieve detailed track information with paginated lyrics.

        Args:
            track_id (str): Unique track identifier.
            page_number (int): Lyrics page number (1-based).
            page_size (int): Number of lyrics lines per page.

        Returns:
            dict: Track data with paginated lyrics content.

        Raises:
            HTTPException(404): Track not found.
        """
        track_data = await self.data_repository.retrieve_track(track_id)
        if not track_data:
            raise HTTPException(
                status_code=404,
                detail=f"Track with ID {track_id} not found"
            )
        
        # Implement lyrics pagination
        lyrics_content = track_data.get("lyrics", [])
        total_lines = len(lyrics_content)

        # Calculate pagination boundaries
        start_index = (page_number - 1) * page_size
        end_index = start_index + page_size
        paginated_lyrics = lyrics_content[start_index:min(end_index, total_lines)]
        
        track_data["lyrics"] = paginated_lyrics
        return track_data

    async def remove_track(self, track_id: str) -> Optional[str]:
        """
        Delete a track from the catalog.

        Args:
            track_id (str): Unique track identifier.

        Returns:
            str: Success confirmation message.

        Raises:
            HTTPException(404): Track not found.
        """
        deletion_success = await self.data_repository.remove_track(track_id)
        if not deletion_success:
            raise HTTPException(
                status_code=404,
                detail=f"Track with ID {track_id} not found"
            )
        return f"Track with ID {track_id} successfully removed from catalog"

    async def update_track_information(self, track_id: str, update_data: dict) -> Optional[str]:
        """
        Apply partial updates to track information.

        Args:
            track_id (str): Unique track identifier.
            update_data (dict): Fields to update (title, artist, etc.).

        Returns:
            str: Update confirmation message.

        Raises:
            HTTPException(404): Track not found.
        """
        update_success = await self.data_repository.modify_track(track_id, update_data)
        if not update_success:
            raise HTTPException(
                status_code=404,
                detail=f"Track with ID {track_id} not found"
            )
        return f"Track with ID {track_id} successfully updated"

    async def search_catalog(self, search_parameters: dict) -> List[TrackSummary]:
        """
        Search tracks using flexible filtering criteria.

        Supports filtering by artist, release date ranges, keywords, and external links.

        Args:
            search_parameters (dict): Search criteria (subset of TrackSearchQuery).

        Returns:
            List[TrackSummary]: Matching tracks (may be empty).
        """
        matching_tracks = await self.data_repository.query_tracks(search_parameters)
        return [TrackSummary(**track) for track in matching_tracks]
