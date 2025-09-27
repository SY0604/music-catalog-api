import aiohttp
import os


GENIUS_BASE_URL = os.getenv("GENIUS_BASE_URL")
GENIUS_ACCESS_TOKEN = os.getenv("GENIUS_ACCESS_TOKEN")


class GeniusApiClient:
    """Client for interacting with the Genius API to fetch song metadata."""
    
    API_BASE_URL = GENIUS_BASE_URL

    def __init__(self):
        if not GENIUS_ACCESS_TOKEN:
            raise ValueError("GENIUS_ACCESS_TOKEN environment variable is required.")
        self.access_token = GENIUS_ACCESS_TOKEN
        self.request_headers = {"Authorization": f"Bearer {self.access_token}"}

    async def find_track_metadata(self, track_title: str, artist_name: str):
        """
        Search Genius API for track metadata with exact matching.
        Performs case-insensitive comparison and handles punctuation variations.
        """
        search_query = f"{track_title} {artist_name}"
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.API_BASE_URL}/search",
                headers=self.request_headers,
                params={"q": search_query},
            ) as response:
                response_data = await response.json()
                search_results = response_data.get("response", {}).get("hits", [])

                if not search_results:
                    return None

                # Normalize text for accurate comparison
                def normalize_text(text: str) -> str:
                    return "".join(char.lower() for char in text if char.isalnum())

                normalized_title = normalize_text(track_title)
                normalized_artist = normalize_text(artist_name)

                for result in search_results:
                    track_data = result["result"]
                    result_title = normalize_text(track_data["title"])
                    result_artist = normalize_text(track_data["primary_artist"]["name"])

                    if result_title == normalized_title and result_artist == normalized_artist:
                        return {
                            "title": track_data["title"],
                            "artist": track_data["primary_artist"]["name"],
                            "release_date": track_data.get("release_date"),
                            "external_link": track_data.get("url"),
                            "lyrics": [],  # Lyrics would be fetched separately if needed
                        }

                # No exact match found
                return None
