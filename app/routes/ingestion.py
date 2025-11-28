"""API routes for data ingestion."""

import asyncio
import logging
from fastapi import APIRouter, HTTPException, Depends, Request, Body
from pydantic import BaseModel
from typing import List, Dict, Any, Union

from app.core.ingestion import IngestionService
from app.core.vectorization import VectorizationService
from app.core.storage import StorageService
from app.dependencies import get_ingestion_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ingestion", tags=["ingestion"])


class IngestRequest(BaseModel):
    """Request model for ingesting datapoints."""
    datapoints: List[Dict[str, Any]]


class IngestResponse(BaseModel):
    """Response model for ingestion."""
    status: str
    total: int
    processed: int
    stored: int
    failed: int
    errors: List[Dict[str, Any]]


@router.post("/datapoints", response_model=IngestResponse)
async def ingest_datapoints(
    request: Request,
    ingestion_service: IngestionService = Depends(get_ingestion_service)
):
    """
    Ingest datapoints from JSON list.
    
    Accepts either:
    1. A JSON object with 'datapoints' field: {"datapoints": [...]}
    2. A raw JSON array: [...]
    
    The datapoints are vectorized and stored in MongoDB for topic clustering.
    """
    try:
        # Get raw body to handle both formats
        body = await request.json()
        
        # Handle both formats: {"datapoints": [...]} or [...]
        if isinstance(body, list):
            # Raw array format
            datapoints_list = body
        elif isinstance(body, dict) and "datapoints" in body:
            # Wrapped format
            datapoints_list = body["datapoints"]
        else:
            raise HTTPException(
                status_code=400,
                detail="Request body must be either a JSON array or an object with 'datapoints' field"
            )
        
        # Load and validate datapoints (this is fast, no need to thread)
        datapoints = ingestion_service.load_datapoints_from_dict(datapoints_list)
        
        if not datapoints:
            raise HTTPException(
                status_code=400,
                detail="No valid datapoints found in request"
            )
        
        # Process and store in a thread pool to avoid blocking the event loop
        # This wraps the blocking MongoDB and embedding operations
        stats = await asyncio.to_thread(ingestion_service.ingest_datapoints, datapoints)
        
        return IngestResponse(
            status="success",
            total=stats["total"],
            processed=stats["processed"],
            stored=stats["stored"],
            failed=stats["failed"],
            errors=stats["errors"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to ingest datapoints: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

