import aiohttp
import os

class LyricsLibraryClient:
    """Client for LRCLib API to fetch synchronized and plain lyrics."""
    
    API_ENDPOINT = os.getenv("LRCLIB_API_ENDPOINT")

    async def get_track_lyrics(self, track_title: str, artist_name: str) -> dict | None:
        """
        Fetch lyrics from LRCLib API.
        Returns synchronized or plain lyrics if available.
        """
        request_params = {"track_name": track_title, "artist_name": artist_name}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.API_ENDPOINT, params=request_params) as response:
                    if response.status != 200:
                        return None
                    return await response.json()
        except Exception as error:
            print(f"LRCLib API request failed: {error}")
            return None
