"""Dependency injection for services."""

import os
import logging
from functools import lru_cache
from pymongo import MongoClient
from langchain_together import TogetherEmbeddings
from langchain_core.embeddings import Embeddings

from app.core.ingestion import IngestionService
from app.core.vectorization import VectorizationService
from app.core.storage import StorageService
from app.core.clustering import ClusteringService
from app.core.pattern_detection import PatternDetectionService
from app.core.classification import ClassificationService
from app.core.verification import VerificationService
from app.core.public_updates import PublicUpdateService

logger = logging.getLogger(__name__)


@lru_cache()
def get_mongo_client() -> MongoClient:
    """
    Get MongoDB client.
    
    Supports both authenticated and non-authenticated connections.
    If MONGODB_URL is provided, it's used as-is.
    Otherwise, constructs URL from MONGO_ROOT_USERNAME and MONGO_ROOT_PASSWORD if available.
    """
    mongo_url = os.getenv("MONGODB_URL")
    username = os.getenv("MONGO_ROOT_USERNAME", "admin")
    password = os.getenv("MONGO_ROOT_PASSWORD", "changeme")
    db_name = os.getenv("MONGODB_DB_NAME", "misinformation_detection")
    
    # If MONGODB_URL is set but doesn't contain credentials, construct authenticated URL
    if mongo_url and "@" not in mongo_url and username and password:
        # MONGODB_URL provided but no credentials - add them
        # Extract host/port from MONGODB_URL or use defaults
        if "://" in mongo_url:
            # Extract everything after mongodb://
            parts = mongo_url.split("://", 1)[1]
            if "/" in parts:
                host_port = parts.split("/")[0]
            else:
                host_port = parts.split("?")[0] if "?" in parts else parts
        else:
            host_port = "localhost:27017"
        
        mongo_url = f"mongodb://{username}:{password}@{host_port}/{db_name}?authSource=admin"
        logger.info("Using MongoDB with authentication (credentials added to MONGODB_URL)")
    elif not mongo_url:
        # No MONGODB_URL provided - construct from individual credentials
        if username and password:
            # Construct authenticated connection string
            mongo_url = f"mongodb://{username}:{password}@localhost:27017/{db_name}?authSource=admin"
            logger.info("Using MongoDB with authentication")
        else:
            # No authentication
            mongo_url = "mongodb://localhost:27017"
            logger.info("Using MongoDB without authentication")
    # If MONGODB_URL is set and contains credentials, use it as-is
    elif mongo_url and "@" in mongo_url:
        logger.info("Using MongoDB with authentication (from MONGODB_URL)")
    else:
        logger.info("Using MongoDB without authentication (from MONGODB_URL)")
    
    return MongoClient(mongo_url)


@lru_cache()
def get_embeddings_model() -> TogetherEmbeddings:
    """
    Get embeddings model using Together AI via langchain-together.
    
    Uses the official LangChain Together integration as documented at:
    https://docs.langchain.com/oss/python/integrations/text_embedding/together
    
    Available Together AI embedding models:
    - BAAI/bge-base-en-v1.5 (768 dimensions, recommended)
    - BAAI/bge-large-en-v1.5 (1024 dimensions, higher quality)
    - BAAI/bge-small-en-v1.5 (384 dimensions, faster)
    - togethercomputer/m2-bert-80M-8k-retrieval (Together's model)
    """
    together_api_key = os.getenv("TOGETHER_API_KEY")
    together_model = os.getenv("TOGETHER_EMBEDDING_MODEL", "BAAI/bge-base-en-v1.5")
    
    if not together_api_key:
        raise ValueError(
            "TOGETHER_API_KEY environment variable is required. "
            "Get your API key from https://api.together.xyz/"
        )
    
    # Use official LangChain Together integration
    # TogetherEmbeddings will use TOGETHER_API_KEY from env if not provided
    return TogetherEmbeddings(
        model=together_model,
        together_api_key=together_api_key
    )


@lru_cache()
def get_storage_service() -> StorageService:
    """Get storage service."""
    mongo_client = get_mongo_client()
    db_name = os.getenv("MONGODB_DB_NAME", "misinformation_detection")
    return StorageService(mongo_client, db_name)


@lru_cache()
def get_vectorization_service() -> VectorizationService:
    """Get vectorization service."""
    embeddings_model = get_embeddings_model()
    return VectorizationService(embeddings_model)


def get_ingestion_service() -> IngestionService:
    """Get ingestion service."""
    vectorization_service = get_vectorization_service()
    storage_service = get_storage_service()
    return IngestionService(vectorization_service, storage_service)


def get_clustering_service() -> ClusteringService:
    """Get clustering service."""
    storage_service = get_storage_service()
    return ClusteringService(storage_service)


def get_pattern_detection_service() -> PatternDetectionService:
    """Get pattern detection service."""
    storage_service = get_storage_service()
    clustering_service = get_clustering_service()
    return PatternDetectionService(storage_service, clustering_service)


def get_classification_service() -> ClassificationService:
    """Get classification service."""
    return ClassificationService()


def get_verification_service() -> VerificationService:
    """Get verification service."""
    storage_service = get_storage_service()
    return VerificationService(storage_service)


def get_public_update_service() -> PublicUpdateService:
    """Get public update service."""
    storage_service = get_storage_service()
    pattern_service = get_pattern_detection_service()
    classification_service = get_classification_service()
    verification_service = get_verification_service()
    return PublicUpdateService(
        storage_service,
        pattern_service,
        classification_service,
        verification_service
    )

