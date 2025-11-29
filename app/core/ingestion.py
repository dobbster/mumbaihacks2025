"""Data ingestion pipeline for processing JSON datapoints."""

import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
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
    
    def process_datapoint(self, datapoint: DataPoint, skip_if_exists: bool = True) -> Optional[StoredDataPoint]:
        """
        Process a single datapoint: vectorize and prepare for storage.
        
        Args:
            datapoint: DataPoint to process
            skip_if_exists: If True, skip processing if duplicate exists
            
        Returns:
            StoredDataPoint ready for MongoDB, or None if duplicate found
        """
        # Check for existing datapoint (deduplication)
        # Priority: URL (most reliable) > ID (may be deterministic)
        if skip_if_exists:
            existing = None
            # First check by URL (most reliable - URLs are unique per article)
            if datapoint.url:
                existing = self.storage_service.datapoint_exists(url=datapoint.url)
                if existing:
                    logger.debug(f"Duplicate datapoint found by URL: {datapoint.url}, skipping")
                    return None
            
            # If no URL, check by ID (fallback)
            if not existing and datapoint.id:
                existing = self.storage_service.datapoint_exists(datapoint_id=datapoint.id)
                if existing:
                    logger.debug(f"Duplicate datapoint found by ID: {datapoint.id}, skipping")
                    return None
        
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
        batch_size: int = 10,
        skip_duplicates: bool = True
    ) -> Dict[str, Any]:
        """
        Ingest multiple datapoints: vectorize and store in MongoDB.
        When duplicates are found, retrieves existing datapoints from MongoDB.
        
        Args:
            datapoints: List of DataPoint objects to ingest
            batch_size: Number of datapoints to process in parallel
            skip_duplicates: If True, skip duplicate datapoints (by ID or URL) and retrieve existing ones
            
        Returns:
            Dictionary with ingestion statistics and retrieved duplicates
        """
        stats = {
            "total": len(datapoints),
            "processed": 0,
            "stored": 0,
            "skipped_duplicates": 0,
            "retrieved_duplicates": 0,  # New: count of retrieved duplicates
            "failed": 0,
            "errors": []
        }
        
        # List to store retrieved duplicate datapoints (converted back to DataPoint format)
        retrieved_duplicates: List[DataPoint] = []
        
        # Process in batches
        for i in range(0, len(datapoints), batch_size):
            batch = datapoints[i:i + batch_size]
            logger.info(f"Processing batch {i//batch_size + 1} ({len(batch)} datapoints)")
            
            for datapoint in batch:
                try:
                    # Process datapoint (includes deduplication check and embedding generation)
                    stored = self.process_datapoint(datapoint, skip_if_exists=skip_duplicates)
                    
                    if stored is None:
                        # Duplicate found - retrieve existing datapoint from MongoDB
                        stats["skipped_duplicates"] += 1
                        
                        # Try to retrieve by URL first (most reliable)
                        existing_doc = None
                        if datapoint.url:
                            existing_doc = self.storage_service.datapoint_exists(url=datapoint.url)
                        
                        # Fallback to ID if URL check didn't find it
                        if not existing_doc and datapoint.id:
                            existing_doc = self.storage_service.datapoint_exists(datapoint_id=datapoint.id)
                        
                        if existing_doc:
                            # Convert MongoDB document back to DataPoint format
                            retrieved_dp = self._mongo_doc_to_datapoint(existing_doc)
                            retrieved_duplicates.append(retrieved_dp)
                            stats["retrieved_duplicates"] += 1
                            logger.debug(f"Retrieved existing datapoint from MongoDB: {datapoint.id or datapoint.url}")
                        else:
                            logger.warning(f"Duplicate detected but could not retrieve from MongoDB: {datapoint.id}")
                        continue
                    
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
            f"{stats['skipped_duplicates']} duplicates skipped ({stats['retrieved_duplicates']} retrieved), "
            f"{stats['failed']} failed"
        )

        # Add retrieved duplicates to stats for downstream use
        stats["retrieved_duplicates_list"] = [dp.model_dump() for dp in retrieved_duplicates]
        
        return stats
    
    def _mongo_doc_to_datapoint(self, doc: Dict[str, Any]) -> DataPoint:
        """
        Convert a MongoDB document back to a DataPoint object.
        
        Args:
            doc: MongoDB document dictionary
            
        Returns:
            DataPoint object
        """
        # Convert datetime objects to ISO format strings
        published_at = doc.get("published_at")
        if published_at and isinstance(published_at, datetime):
            published_at = published_at.isoformat() + "Z"
        elif published_at:
            published_at = str(published_at)
        
        ingested_at = doc.get("ingested_at")
        if ingested_at and isinstance(ingested_at, datetime):
            ingested_at = ingested_at.isoformat() + "Z"
        elif ingested_at:
            ingested_at = str(ingested_at)
        
        return DataPoint(
            id=doc.get("_id") or doc.get("id", ""),
            source_type=doc.get("source_type", ""),
            source_name=doc.get("source_name", ""),
            source_url=doc.get("source_url", ""),
            title=doc.get("title", ""),
            content=doc.get("content", ""),
            url=doc.get("url", ""),
            published_at=published_at,
            author=doc.get("author"),
            categories=doc.get("categories", []),
            ingested_at=ingested_at or datetime.utcnow().isoformat() + "Z",
            search_query=doc.get("search_query"),
            relevance_score=doc.get("relevance_score")
        )
    
    def _prepare_text_for_embedding(self, datapoint: DataPoint) -> str:
        """
        Prepare text for embedding by combining title and content.
        Truncates to ensure it fits within embedding model's token limit (512 tokens).
        
        Args:
            datapoint: DataPoint to prepare text for
            
        Returns:
            Combined text string for embedding (truncated to ~400 tokens for safety)
        """
        # Combine title and content for better semantic understanding
        text_parts = [datapoint.title] if datapoint.title else []
        
        if datapoint.content:
            text_parts.append(datapoint.content)
        
        # Add categories as context if available
        if datapoint.categories:
            text_parts.append(" ".join(datapoint.categories))
        
        combined_text = " ".join(text_parts).strip()
        
        # Truncate to ~400 tokens (roughly 3000 characters) to stay within 512 token limit
        # Using character count as rough estimate: ~7.5 chars per token for English
        max_chars = 3000  # Conservative limit for ~400 tokens
        
        if len(combined_text) > max_chars:
            # Truncate but try to preserve title and first part of content
            if datapoint.title and len(datapoint.title) < max_chars:
                # Keep full title, truncate content
                remaining_chars = max_chars - len(datapoint.title) - 1  # -1 for space
                if datapoint.content:
                    truncated_content = datapoint.content[:remaining_chars]
                    # Try to truncate at word boundary
                    last_space = truncated_content.rfind(' ')
                    if last_space > remaining_chars * 0.8:  # If we can find a word boundary
                        truncated_content = truncated_content[:last_space]
                    combined_text = f"{datapoint.title} {truncated_content}"
                else:
                    combined_text = datapoint.title
            else:
                # Title itself is too long, truncate everything
                combined_text = combined_text[:max_chars]
                # Try to truncate at word boundary
                last_space = combined_text.rfind(' ')
                if last_space > max_chars * 0.8:
                    combined_text = combined_text[:last_space]
        
        return combined_text
    
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

