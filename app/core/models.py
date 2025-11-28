"""Data models for misinformation detection system."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class DataPoint(BaseModel):
    """Base model for incoming datapoints from various sources."""
    id: str
    source_type: str  # "rss" or "tavily"
    source_name: str
    source_url: str
    title: str
    content: str
    url: str
    published_at: Optional[str] = None  # ISO format datetime string
    author: Optional[str] = None
    categories: List[str] = Field(default_factory=list)
    ingested_at: str  # ISO format datetime string
    
    # Tavily-specific fields
    search_query: Optional[str] = None
    relevance_score: Optional[float] = None


class StoredDataPoint(BaseModel):
    """Model for datapoints stored in MongoDB with embeddings."""
    id: str
    source_type: str
    source_name: str
    source_url: str
    title: str
    content: str
    url: str
    published_at: datetime
    author: Optional[str] = None
    categories: List[str] = Field(default_factory=list)
    ingested_at: datetime
    
    # Tavily-specific fields
    search_query: Optional[str] = None
    relevance_score: Optional[float] = None
    
    # Vectorization fields
    embedding: List[float] = Field(default_factory=list)
    embedding_model: str = "BAAI/bge-base-en-v1.5"  # Together AI default
    vectorized_at: Optional[datetime] = None
    
    # Processing status
    processed: bool = False
    claims_extracted: bool = False
    clustered: bool = False
    cluster_id: Optional[str] = None
    
    # Metadata for clustering
    text_for_embedding: str  # Cleaned/processed text used for embedding
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class Claim(BaseModel):
    """Model for extracted claims from datapoints."""
    id: str
    datapoint_id: str
    claim_text: str
    extracted_at: datetime
    entities: List[str] = Field(default_factory=list)
    embedding: List[float] = Field(default_factory=list)
    cluster_id: Optional[str] = None

