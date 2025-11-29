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
        Automatically truncates text to ~400 tokens (3000 chars) to stay within model limits.
        
        Args:
            text: Text to embed
            
        Returns:
            List of floats representing the embedding vector
        """
        try:
            # Truncate to ~400 tokens (3000 chars) to stay within 512 token limit
            # Using character count as rough estimate: ~7.5 chars per token for English
            max_chars = 3000  # Conservative limit for ~400 tokens
            
            original_length = len(text)
            if original_length > max_chars:
                truncated_text = text[:max_chars]
                # Try to truncate at word boundary
                last_space = truncated_text.rfind(' ')
                if last_space > max_chars * 0.8:  # If we can find a word boundary
                    truncated_text = truncated_text[:last_space]
                text = truncated_text
                logger.debug(f"Truncated text from {original_length} to {len(text)} chars for embedding")
            
            embedding = self.embeddings_model.embed_query(text)
            logger.debug(f"Generated embedding of dimension {len(embedding)}")
            return embedding
        except Exception as e:
            logger.error(f"Failed to generate embedding: {e}", exc_info=True)
            raise
    
    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts (more efficient).
        Automatically truncates each text to ~400 tokens (3000 chars) to stay within model limits.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
        """
        try:
            # Truncate each text to ~400 tokens (3000 chars)
            max_chars = 3000
            truncated_texts = []
            
            for text in texts:
                if len(text) > max_chars:
                    truncated = text[:max_chars]
                    # Try to truncate at word boundary
                    last_space = truncated.rfind(' ')
                    if last_space > max_chars * 0.8:
                        truncated = truncated[:last_space]
                    truncated_texts.append(truncated)
                else:
                    truncated_texts.append(text)
            
            embeddings = self.embeddings_model.embed_documents(truncated_texts)
            logger.debug(f"Generated {len(embeddings)} embeddings")
            return embeddings
        except Exception as e:
            logger.error(f"Failed to generate batch embeddings: {e}", exc_info=True)
            raise

