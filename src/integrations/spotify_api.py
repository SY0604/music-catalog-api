import aiohttp
import asyncio
import base64
import os
from typing import Optional, Dict


class SpotifyApiClient:
    """
    Client for Spotify Web API integration.

    Handles authentication via Client Credentials flow and provides
    track search functionality with metadata retrieval.
    """

    def __init__(self):
        self.app_id = os.getenv("SPOTIFY_APP_ID")
        self.app_secret = os.getenv("SPOTIFY_APP_SECRET")
        self.auth_endpoint = os.getenv("SPOTIFY_AUTH_ENDPOINT")
        self.search_endpoint = os.getenv("SPOTIFY_SEARCH_ENDPOINT")
        self.bearer_token: Optional[str] = None

    async def _authenticate(self) -> str:
        """Obtain access token using Client Credentials flow."""
        if self.bearer_token:
            return self.bearer_token

        if not self.app_id or not self.app_secret:
            raise Exception("Spotify credentials (APP_ID or APP_SECRET) not configured")

        # Encode credentials for Basic authentication
        credentials = f"{self.app_id}:{self.app_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()

        auth_headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        auth_payload = {"grant_type": "client_credentials"}

        async with aiohttp.ClientSession() as session:
            async with session.post(self.auth_endpoint, data=auth_payload, headers=auth_headers) as response:
                response_text = await response.text()
                if response.status != 200:
                    raise Exception(f"Spotify authentication failed: {response.status}, response={response_text}")

                token_response = await response.json()
                self.bearer_token = token_response["access_token"]
                return self.bearer_token

    async def search_track_metadata(self, track_title: str, artist_name: str) -> Optional[Dict]:
        """
        Search for track metadata on Spotify.
        Returns metadata for the first matching result or None if not found.
        """
        access_token = await self._authenticate()
        search_query = f"track:{track_title} artist:{artist_name}"

        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.search_endpoint,
                params={"q": search_query, "type": "track", "limit": 1},
                headers={"Authorization": f"Bearer {access_token}"},
            ) as response:
                if response.status != 200:
                    return None
                    
                search_data = await response.json()
                track_items = search_data.get("tracks", {}).get("items", [])
                if not track_items:
                    return None

                track_info = track_items[0]
                return {
                    "spotify_id": track_info["id"],
                    "release_date": track_info["album"]["release_date"],
                    "external_url": track_info["external_urls"]["spotify"],
                    "album_artwork": track_info["album"]["images"][0]["url"]
                    if track_info["album"]["images"]
                    else None,
                }
