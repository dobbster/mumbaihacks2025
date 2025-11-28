"""Data ingestion pipeline for processing JSON datapoints."""

import json
import logging
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path

from app.core.models import DataPoint, StoredDataPoint
from app.core.vectorization import VectorizationService
from app.core.storage import StorageService

logger = logging.getLogger(__name__)


class IngestionService:
    """Service for ingesting and processing datapoints from JSON."""
    
    def __init__(
        self,
        vectorization_service: VectorizationService,
        storage_service: StorageService
    ):
        self.vectorization_service = vectorization_service
        self.storage_service = storage_service
    
    def load_datapoints_from_json(self, json_path: str | Path) -> List[DataPoint]:
        """
        Load datapoints from JSON file.
        
        Args:
            json_path: Path to JSON file containing list of datapoints
            
        Returns:
            List of DataPoint objects
        """
        json_path = Path(json_path)
        
        if not json_path.exists():
            raise FileNotFoundError(f"JSON file not found: {json_path}")
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            raise ValueError("JSON file must contain a list of datapoints")
        
        datapoints = []
        for item in data:
            try:
                datapoint = DataPoint(**item)
                datapoints.append(datapoint)
            except Exception as e:
                logger.warning(f"Failed to parse datapoint: {e}", extra={"item": item})
                continue
        
        logger.info(f"Loaded {len(datapoints)} datapoints from {json_path}")
        return datapoints
    
    def load_datapoints_from_dict(self, data: List[Dict[str, Any]]) -> List[DataPoint]:
        """
        Load datapoints from Python dict/list.
        
        Args:
            data: List of dictionaries representing datapoints
            
        Returns:
            List of DataPoint objects
        """
        datapoints = []
        for item in data:
            try:
                datapoint = DataPoint(**item)
                datapoints.append(datapoint)
            except Exception as e:
                logger.warning(f"Failed to parse datapoint: {e}", extra={"item": item})
                continue
        
        logger.info(f"Loaded {len(datapoints)} datapoints from dict")
        return datapoints
    
    def process_datapoint(self, datapoint: DataPoint) -> StoredDataPoint:
        """
        Process a single datapoint: vectorize and prepare for storage.
        
        Args:
            datapoint: DataPoint to process
            
        Returns:
            StoredDataPoint ready for MongoDB
        """
        # Prepare text for embedding (combine title + content)
        text_for_embedding = self._prepare_text_for_embedding(datapoint)
        
        # Generate embedding
        embedding = self.vectorization_service.generate_embedding(text_for_embedding)
        
        # Convert to StoredDataPoint
        stored = StoredDataPoint(
            id=datapoint.id,
            source_type=datapoint.source_type,
            source_name=datapoint.source_name,
            source_url=datapoint.source_url,
            title=datapoint.title,
            content=datapoint.content,
            url=datapoint.url,
            published_at=self._parse_datetime(datapoint.published_at),
            author=datapoint.author,
            categories=datapoint.categories,
            ingested_at=self._parse_datetime(datapoint.ingested_at),
            search_query=datapoint.search_query,
            relevance_score=datapoint.relevance_score,
            embedding=embedding,
            embedding_model=self.vectorization_service.model_name,
            vectorized_at=datetime.utcnow(),
            text_for_embedding=text_for_embedding,
            processed=False,
            claims_extracted=False,
            clustered=False
        )
        
        return stored
    
    def ingest_datapoints(
        self,
        datapoints: List[DataPoint],
        batch_size: int = 10
    ) -> Dict[str, Any]:
        """
        Ingest multiple datapoints: vectorize and store in MongoDB.
        
        Args:
            datapoints: List of DataPoint objects to ingest
            batch_size: Number of datapoints to process in parallel
            
        Returns:
            Dictionary with ingestion statistics
        """
        stats = {
            "total": len(datapoints),
            "processed": 0,
            "stored": 0,
            "failed": 0,
            "errors": []
        }
        
        # Process in batches
        for i in range(0, len(datapoints), batch_size):
            batch = datapoints[i:i + batch_size]
            logger.info(f"Processing batch {i//batch_size + 1} ({len(batch)} datapoints)")
            
            for datapoint in batch:
                try:
                    # Process datapoint (includes embedding generation)
                    stored = self.process_datapoint(datapoint)
                    stats["processed"] += 1
                    
                    # Store in MongoDB
                    self.storage_service.store_datapoint(stored)
                    stats["stored"] += 1
                    
                    logger.debug(f"Successfully ingested datapoint: {datapoint.id}")
                    
                except Exception as e:
                    stats["failed"] += 1
                    # Extract more detailed error information
                    error_msg = str(e)
                    error_type = type(e).__name__
                    
                    # Provide helpful error messages
                    if "Connection" in error_type or "connection" in error_msg.lower():
                        error_msg = (
                            f"Connection error. Please check:\n"
                            f"1. TOGETHER_API_KEY is set in environment variables\n"
                            f"2. Your internet connection is working\n"
                            f"3. Together AI API is accessible\n"
                            f"Run: python scripts/check_together_api.py to verify"
                        )
                    elif "Blocking" in error_type or "blocking" in error_msg.lower():
                        error_msg = (
                            f"Blocking operation detected. "
                            f"Restart LangGraph server with: langgraph dev --allow-blocking"
                        )
                    
                    error_info = {
                        "datapoint_id": datapoint.id,
                        "error": error_msg,
                        "error_type": error_type
                    }
                    stats["errors"].append(error_info)
                    logger.error(f"Failed to ingest datapoint {datapoint.id}: {e}", exc_info=True)
        
        logger.info(
            f"Ingestion complete: {stats['stored']}/{stats['total']} stored, "
            f"{stats['failed']} failed"
        )
        
        return stats
    
    def _prepare_text_for_embedding(self, datapoint: DataPoint) -> str:
        """
        Prepare text for embedding by combining title and content.
        
        Args:
            datapoint: DataPoint to prepare text for
            
        Returns:
            Combined text string for embedding
        """
        # Combine title and content for better semantic understanding
        text_parts = [datapoint.title]
        
        if datapoint.content:
            text_parts.append(datapoint.content)
        
        # Add categories as context if available
        if datapoint.categories:
            text_parts.append(" ".join(datapoint.categories))
        
        return " ".join(text_parts).strip()
    
    def _parse_datetime(self, dt_string: str) -> datetime:
        """Parse ISO format datetime string."""
        try:
            # Handle ISO format with or without timezone
            if dt_string.endswith('Z'):
                dt_string = dt_string[:-1] + '+00:00'
            return datetime.fromisoformat(dt_string.replace('Z', '+00:00'))
        except Exception as e:
            logger.warning(f"Failed to parse datetime '{dt_string}', using current time: {e}")
            return datetime.utcnow()

