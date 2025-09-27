from ..data.track_repository import TrackRepository
from ..business.track_service import TrackManagementService
from ..integrations.genius_api import GeniusApiClient
from ..integrations.lrclib_api import LyricsLibraryClient
from ..integrations.spotify_api import SpotifyApiClient
from .database_config import DatabaseConfiguration

def initialize_service_dependencies(config: DatabaseConfiguration = None):
    """
    Initialize and wire up all service dependencies.
    
    Creates instances of repositories, external clients, and services
    with proper dependency injection.
    """
    if config is None:
        from src.config.database_config import DatabaseConfiguration
        config = DatabaseConfiguration()

    # Initialize data layer
    track_repository = TrackRepository(
        connection_string=config.mongodb_connection, 
        database_name=config.database_name
    )
    
    # Initialize external API clients
    genius_client = GeniusApiClient()
    lyrics_client = LyricsLibraryClient()
    spotify_client = SpotifyApiClient()

    # Initialize business service with all dependencies
    track_management_service = TrackManagementService(
        data_repository=track_repository, 
        metadata_provider=genius_client, 
        lyrics_provider=lyrics_client, 
        streaming_provider=spotify_client
    )

    return {"track_service": track_management_service}
