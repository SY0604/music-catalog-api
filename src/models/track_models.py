from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class TrackBase(BaseModel):
    """Base model for track information."""
    title: str = Field(..., description="Track title")
    artist: str = Field(..., description="Artist or performer name")

class TrackCreation(TrackBase):
    """Model for creating new tracks."""
    pass  # Inherits all fields from TrackBase

class TrackWithLyrics(TrackBase):
    """Complete track model including lyrics content."""
    id: str = Field(..., description="Unique track identifier")
    release_date: Optional[date] = Field(None, description="Track release date")
    lyrics: Optional[List[str]] = Field(None, description="Track lyrics as list of lines")
    external_link: Optional[str] = Field(None, description="External source URL")

class TrackSummary(TrackBase):
    """Condensed track information without lyrics."""
    id: str = Field(..., description="Unique track identifier")
    release_date: Optional[date] = Field(None, description="Track release date")
    external_link: Optional[str] = Field(None, description="External source URL")

class TrackSearchQuery(BaseModel):
    """Search parameters for track queries."""
    from_date: Optional[date] = None
    to_date: Optional[date] = None
    search_terms: Optional[List[str]] = None
    external_link: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "search_terms": ["rock", "classic"]
            }
        }

class TrackUpdateRequest(BaseModel):
    """Model for partial track updates."""
    title: Optional[str] = None
    artist: Optional[str] = None
    lyrics: List[Optional[str]] = None

    class Config:
        schema_extra = {
            "example": {
                "title": "Updated Track Title"
            }
        }
