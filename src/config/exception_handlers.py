from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

async def handle_http_exceptions(request: Request, exception: HTTPException):
    """
    Global HTTP exception handler for consistent error responses.
    
    Args:
        request: The incoming HTTP request
        exception: The HTTPException that was raised
        
    Returns:
        JSONResponse with standardized error format
    """
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "error": True,
            "message": exception.detail,
            "status_code": exception.status_code,
            "path": str(request.url)
        }
    )
