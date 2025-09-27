from fastapi import APIRouter, Depends, HTTPException, Query, Body
from ..business.track_service import TrackManagementService
from ..models.track_models import TrackCreation, TrackWithLyrics, TrackSummary, TrackUpdateRequest, TrackSearchQuery
from typing import List, Optional

track_router = APIRouter()

def get_track_service() -> TrackManagementService:
    """
    Dependency injection for track management service.
    Uses configuration module to build service layer dependencies.
    """
    from src.config.dependencies import initialize_service_dependencies
    return initialize_service_dependencies()["track_service"]

@track_router.post("/", response_model=TrackSummary, tags=["Tracks"], 
                   summary="Add new track with automatic metadata enrichment", 
                   responses={
                       404: {"description": "Track not found in external sources"},
                       409: {"description": "Track already exists in catalog"},
                       500: {"description": "Database operation failed"},
                   })
async def create_track(
    track: TrackCreation = Body(..., example={"title": "Bohemian Rhapsody", "artist": "Queen"}), 
    service: TrackManagementService = Depends(get_track_service)
):
    """
    Add a new track to the catalog with automatic metadata enrichment.

    ### Request Body
    - **title**: Track title *(string, required)*
    - **artist**: Artist name *(string, required)*

    The system will automatically enrich the track with:
    - `release_date` from multiple sources
    - `lyrics` content from specialized providers
    - `external_link` to source material

    ### Response Codes
    - **200**: `TrackSummary` (successfully created track)
    - **409**: Track already exists in the catalog
    - **404**: Track not found in external metadata sources
    - **500**: Database persistence error
    """
    return await service.create_new_track(dict(track))

@track_router.get("/{track_id}", response_model=TrackWithLyrics, tags=["Tracks"], 
                  summary="Retrieve track details with paginated lyrics", 
                  responses={404: {"description": "Track not found"}})
async def get_track_details(
    track_id: str,
    page: int = Query(1, ge=1, description="Lyrics page number"),
    size: int = Query(10, ge=1, le=100, description="Lines per page"),
    service: TrackManagementService = Depends(get_track_service)
):
    """
    Retrieve comprehensive track information by unique identifier.

    ### Path Parameters
    - **track_id**: MongoDB ObjectId of the track *(string, required)*

    ### Query Parameters
    - **page**: Page number for lyrics pagination *(integer, default: 1)*
    - **size**: Number of lyrics lines per page *(integer, default: 10, max: 100)*

    ### Response Codes
    - **200**: `TrackWithLyrics` (complete track data)
    - **404**: Track not found in catalog
    """
    track_data = await service.retrieve_track_details(track_id, page, size)
    if track_data is None:
        raise HTTPException(status_code=404, detail="Track not found")
    return track_data

@track_router.delete("/{track_id}", tags=["Tracks"], 
                     summary="Remove track from catalog", 
                     responses={404: {"description": "Track not found"}})
async def delete_track(
    track_id: str, 
    service: TrackManagementService = Depends(get_track_service)
):
    """
    Permanently remove a track from the catalog.

    ### Path Parameters
    - **track_id**: MongoDB ObjectId of the track *(string, required)*

    ### Response Codes
    - **200**: Track successfully deleted
    - **404**: Track not found in catalog
    """
    result = await service.remove_track(track_id)
    return {"message": result}

@track_router.patch("/{track_id}", tags=["Tracks"], 
                    summary="Update track information partially", 
                    responses={404: {"description": "Track not found"}})
async def update_track(
    track_id: str, 
    updates: TrackUpdateRequest = Body(...), 
    service: TrackManagementService = Depends(get_track_service)
):
    """
    Apply partial updates to track information.

    ### Path Parameters
    - **track_id**: MongoDB ObjectId *(string, required)*

    ### Request Body
    Any combination of:
    - **title** *(string, optional)*
    - **artist** *(string, optional)*
    - **lyrics** *(array of strings, optional)*

    ### Response Codes
    - **200**: Track successfully updated
    - **404**: Track not found in catalog
    """
    result = await service.update_track_information(track_id, updates.dict(exclude_unset=True))
    return {"message": result}

@track_router.post("/search", response_model=List[TrackSummary], tags=["Tracks"], 
                   summary="Search tracks with flexible filtering options")
async def search_tracks(
    search_query: TrackSearchQuery = Body(...),
    service: TrackManagementService = Depends(get_track_service)
):
    """
    Search the track catalog using flexible filtering criteria.

    ### Request Body
    - **search_terms** *(array of strings, optional)*: Keywords to match in title, artist, or lyrics
    - **from_date** *(date, optional)*: Earliest release date filter
    - **to_date** *(date, optional)*: Latest release date filter
    - **external_link** *(string, optional)*: Filter by external source URL

    ### Response Codes
    - **200**: List of `TrackSummary` matching search criteria (may be empty)
    """
    results = await service.search_catalog(search_query.dict(exclude_unset=True))
    return results
