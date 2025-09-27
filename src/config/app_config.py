import os
import json
from functools import lru_cache
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ApplicationSettings:
    """Central configuration management for the Music Catalog API."""
    
    def __init__(self):
        # Application core settings
        self.development_mode: bool = os.getenv("DEVELOPMENT_MODE", "false").lower() == "true"
        self.api_docs_path: str = os.getenv("API_DOCS_PATH", "/docs")
        self.redoc_docs_path: str = os.getenv("REDOC_DOCS_PATH", "/redoc")
        self.application_name: str = os.getenv("APPLICATION_NAME", "Music API")
        self.application_description: str = os.getenv("APPLICATION_DESCRIPTION", "Music management API")

        # API configuration
        self.api_version_prefix: str = "/api/v1"
        self.cors_origins = self._parse_cors_origins(os.getenv("CORS_ORIGINS", "*"))

    @staticmethod
    def _parse_cors_origins(origins_value: str):
        """Parse CORS origins from environment variable."""
        # Attempt JSON parsing first
        try:
            return json.loads(origins_value)
        except Exception:
            # Fallback to comma-separated parsing
            return [origin.strip() for origin in origins_value.split(",") if origin.strip()]

    def get_fastapi_config(self):
        """Return FastAPI initialization parameters."""
        return {
            "debug": self.development_mode,
            "docs_url": self.api_docs_path,
            "redoc_url": self.redoc_docs_path,
            "title": self.application_name,
            "description": self.application_description,
        }


@lru_cache
def load_application_settings() -> ApplicationSettings:
    """Load and cache application settings."""
    return ApplicationSettings()
