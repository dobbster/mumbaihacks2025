"""Vectorization service for generating embeddings."""

import logging
from typing import List, Optional
from langchain_core.embeddings import Embeddings

logger = logging.getLogger(__name__)


class VectorizationService:
    """Service for generating embeddings from text."""
    
    def __init__(
        self,
        embeddings_model: Embeddings,
        model_name: Optional[str] = None
    ):
        """
        Initialize vectorization service.
        
        Args:
            embeddings_model: LangChain embeddings model (any Embeddings implementation)
            model_name: Optional model name for logging (auto-detected if not provided)
        """
        self.embeddings_model = embeddings_model
        # Try to get model name from the embeddings model
        if model_name:
            self.model_name = model_name
        else:
            # Extract model name from embeddings model if available
            self.model_name = getattr(embeddings_model, 'model', 'unknown')
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text to embed
            
        Returns:
            List of floats representing the embedding vector
        """
        try:
            embedding = self.embeddings_model.embed_query(text)
            logger.debug(f"Generated embedding of dimension {len(embedding)}")
            return embedding
        except Exception as e:
            logger.error(f"Failed to generate embedding: {e}", exc_info=True)
            raise
    
    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts (more efficient).
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
        """
        try:
            embeddings = self.embeddings_model.embed_documents(texts)
            logger.debug(f"Generated {len(embeddings)} embeddings")
            return embeddings
        except Exception as e:
            logger.error(f"Failed to generate batch embeddings: {e}", exc_info=True)
            raise

