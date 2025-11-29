"""Storage service for MongoDB operations."""

import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from app.core.models import StoredDataPoint

logger = logging.getLogger(__name__)


class StorageService:
    """Service for storing and retrieving datapoints from MongoDB."""
    
    def __init__(self, mongo_client: MongoClient, db_name: str = "misinformation_detection"):
        self.client = mongo_client
        self.db: Database = mongo_client[db_name]
        self.datapoints_collection: Collection = self.db["datapoints"]
        self._ensure_indexes()
    
    def _ensure_indexes(self):
        """Create indexes for efficient queries."""
        try:
            # Index on timestamp for temporal queries
            self.datapoints_collection.create_index("published_at")
            self.datapoints_collection.create_index("ingested_at")
            
            # Index on source for filtering
            self.datapoints_collection.create_index("source_type")
            self.datapoints_collection.create_index("source_name")
            
            # Index on processing status
            self.datapoints_collection.create_index("processed")
            self.datapoints_collection.create_index("clustered")
            
            # Index on cluster_id for clustering queries
            self.datapoints_collection.create_index("cluster_id")
            
            # Index on URL for deduplication
            self.datapoints_collection.create_index("url")
            
            # Text index for search
            self.datapoints_collection.create_index([("title", "text"), ("content", "text")])
            
            logger.info("MongoDB indexes created successfully")
        except Exception as e:
            logger.warning(f"Failed to create indexes (may already exist): {e}")
    
    def store_datapoint(self, datapoint: StoredDataPoint) -> str:
        """
        Store a datapoint in MongoDB.
        
        Args:
            datapoint: StoredDataPoint to store
            
        Returns:
            MongoDB document ID
        """
        try:
            # Convert to dict for MongoDB
            doc = datapoint.model_dump()
            # Convert datetime objects to ensure proper serialization
            doc["published_at"] = datapoint.published_at
            doc["ingested_at"] = datapoint.ingested_at
            if datapoint.vectorized_at:
                doc["vectorized_at"] = datapoint.vectorized_at
            
            # Use datapoint.id as _id to prevent duplicates
            doc["_id"] = datapoint.id
            
            # Upsert to handle duplicates
            result = self.datapoints_collection.update_one(
                {"_id": datapoint.id},
                {"$set": doc},
                upsert=True
            )
            
            logger.debug(f"Stored datapoint: {datapoint.id}")
            return str(result.upserted_id) if result.upserted_id else datapoint.id
            
        except Exception as e:
            logger.error(f"Failed to store datapoint {datapoint.id}: {e}", exc_info=True)
            raise
    
    def get_datapoint(self, datapoint_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a datapoint by ID."""
        return self.datapoints_collection.find_one({"_id": datapoint_id})
    
    def get_recent_datapoints(
        self,
        hours: int = 24,
        source_type: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get datapoints from the last N hours.
        
        Args:
            hours: Number of hours to look back
            source_type: Optional filter by source type
            limit: Optional limit on number of results
            
        Returns:
            List of datapoint documents
        """
        from datetime import timedelta
        
        since = datetime.utcnow() - timedelta(hours=hours)
        
        query = {
            "published_at": {"$gte": since}
        }
        
        if source_type:
            query["source_type"] = source_type
        
        cursor = self.datapoints_collection.find(query).sort("published_at", -1)
        
        if limit:
            cursor = cursor.limit(limit)
        
        return list(cursor)
    
    def get_unprocessed_datapoints(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get datapoints that haven't been processed yet."""
        query = {"processed": False}
        cursor = self.datapoints_collection.find(query).sort("ingested_at", 1)
        
        if limit:
            cursor = cursor.limit(limit)
        
        return list(cursor)
    
    def mark_as_processed(self, datapoint_id: str):
        """Mark a datapoint as processed."""
        self.datapoints_collection.update_one(
            {"_id": datapoint_id},
            {"$set": {"processed": True}}
        )
    
    def update_cluster_id(self, datapoint_id: str, cluster_id: str):
        """Update the cluster ID for a datapoint."""
        self.datapoints_collection.update_one(
            {"_id": datapoint_id},
            {"$set": {"cluster_id": cluster_id, "clustered": True}}
        )
    
    def get_datapoints_by_cluster(self, cluster_id: str) -> List[Dict[str, Any]]:
        """Get all datapoints in a specific cluster."""
        return list(self.datapoints_collection.find({"cluster_id": cluster_id}))
    
    def datapoint_exists(self, datapoint_id: str = None, url: str = None) -> Optional[Dict[str, Any]]:
        """
        Check if a datapoint already exists in the database.
        
        Args:
            datapoint_id: Optional datapoint ID to check
            url: Optional URL to check (for deduplication)
            
        Returns:
            Existing datapoint document if found, None otherwise
        """
        if datapoint_id:
            existing = self.datapoints_collection.find_one({"_id": datapoint_id})
            if existing:
                return existing
        
        if url:
            existing = self.datapoints_collection.find_one({"url": url})
            if existing:
                return existing
        
        return None

