"""Health check endpoint."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Simple health check endpoint.
    
    Returns:
        dict: Status indicating the server is healthy
    """
    return {"status": "healthy"}

