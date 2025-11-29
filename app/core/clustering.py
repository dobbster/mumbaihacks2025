"""Topic clustering service for grouping similar datapoints using DBSCAN."""

import logging
import numpy as np
from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime, timedelta
from sklearn.cluster import DBSCAN

from app.core.storage import StorageService

logger = logging.getLogger(__name__)


class ClusteringService:
    """
    Service for clustering similar datapoints using DBSCAN algorithm.
    
    DBSCAN advantages:
    - Automatically determines number of clusters
    - Handles noise/outliers (marks as -1)
    - Works well with high-dimensional embeddings
    - Finds clusters of varying densities
    """
    
    def __init__(
        self,
        storage_service: StorageService,
        eps: float = 0.30,  # Optimized based on testing: balances topic diversity and cluster quality
        min_samples: int = 2,
        metric: str = "cosine",
        similarity_threshold: float = 0.75
    ):
        """
        Initialize clustering service.
        
        Args:
            storage_service: Storage service for MongoDB operations
            eps: Maximum distance between samples in the same neighborhood (0.0-1.0 for cosine)
                 Lower = stricter clustering (fewer, tighter clusters)
                 Higher = looser clustering (more, larger clusters)
                 Recommended: 0.2-0.4 for topic clustering
            min_samples: Minimum number of samples in a neighborhood to form a cluster
                        Lower = more small clusters
                        Higher = only large clusters
            metric: Distance metric ('cosine' recommended for embeddings)
            similarity_threshold: Minimum cosine similarity for find_similar_datapoints (0.0-1.0)
        """
        self.storage_service = storage_service
        self.eps = eps
        self.min_samples = min_samples
        self.metric = metric
        self.similarity_threshold = similarity_threshold
    
    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return float(dot_product / (norm1 * norm2))
    
    def find_similar_datapoints(
        self,
        query_embedding: List[float],
        hours: int = 24,
        limit: int = 100
    ) -> List[Tuple[Dict[str, Any], float]]:
        """
        Find datapoints similar to the query embedding.
        
        Args:
            query_embedding: Embedding vector to search for
            hours: Look back this many hours
            limit: Maximum number of results
            
        Returns:
            List of tuples (datapoint, similarity_score)
        """
        # Get recent datapoints
        recent_datapoints = self.storage_service.get_recent_datapoints(hours=hours, limit=limit * 2)
        
        similar = []
        for datapoint in recent_datapoints:
            if "embedding" not in datapoint or not datapoint["embedding"]:
                continue
            
            similarity = self.cosine_similarity(query_embedding, datapoint["embedding"])
            
            if similarity >= self.similarity_threshold:
                similar.append((datapoint, similarity))
        
        # Sort by similarity and limit
        similar.sort(key=lambda x: x[1], reverse=True)
        return similar[:limit]
    
    def cluster_datapoints(
        self,
        datapoints: List[Dict[str, Any]],
        min_cluster_size: Optional[int] = None
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Cluster datapoints using DBSCAN algorithm.
        
        Args:
            datapoints: List of datapoint documents with embeddings
            min_cluster_size: Override min_samples for this clustering run
            
        Returns:
            Dictionary mapping cluster_id to list of datapoints
            Note: cluster_id = -1 means noise/outlier (not in any cluster)
        """
        if not datapoints:
            logger.warning("No datapoints provided for clustering")
            return {}
        
        # Extract embeddings and valid indices
        embeddings = []
        valid_indices = []
        valid_datapoints = []
        
        for i, datapoint in enumerate(datapoints):
            if "embedding" not in datapoint or not datapoint["embedding"]:
                logger.debug(f"Skipping datapoint {i}: no embedding")
                continue
            
            embedding = datapoint["embedding"]
            if not isinstance(embedding, list) or len(embedding) == 0:
                logger.debug(f"Skipping datapoint {i}: invalid embedding")
                continue
            
            embeddings.append(embedding)
            valid_indices.append(i)
            valid_datapoints.append(datapoint)
        
        if len(embeddings) < 2:
            logger.warning(f"Not enough valid embeddings for clustering: {len(embeddings)}")
            return {}
        
        # Convert to numpy array
        embeddings_array = np.array(embeddings)
        
        # Use provided min_samples or default
        min_samples = min_cluster_size if min_cluster_size is not None else self.min_samples
        
        # Apply DBSCAN
        logger.info(
            f"Running DBSCAN on {len(embeddings)} datapoints "
            f"(eps={self.eps}, min_samples={min_samples}, metric={self.metric})"
        )
        
        dbscan = DBSCAN(
            eps=self.eps,
            min_samples=min_samples,
            metric=self.metric,
            n_jobs=-1  # Use all CPU cores
        )
        
        cluster_labels = dbscan.fit_predict(embeddings_array)
        
        # Group datapoints by cluster label
        clusters = {}
        noise_count = 0
        
        for idx, label in enumerate(cluster_labels):
            datapoint = valid_datapoints[idx]
            
            if label == -1:
                # Noise/outlier - don't assign to cluster
                noise_count += 1
                continue
            
            cluster_id = f"cluster_{label}"
            
            if cluster_id not in clusters:
                clusters[cluster_id] = []
            
            clusters[cluster_id].append(datapoint)
            
            # Update cluster_id in MongoDB
            self.storage_service.update_cluster_id(datapoint["_id"], cluster_id)
        
        logger.info(
            f"DBSCAN clustering complete: {len(clusters)} clusters, "
            f"{noise_count} noise points, "
            f"{sum(len(c) for c in clusters.values())} clustered datapoints"
        )
        
        return clusters
    
    def cluster_datapoints_simple(
        self,
        datapoints: List[Dict[str, Any]],
        similarity_threshold: float = 0.75,
        min_cluster_size: int = 2
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Simple similarity-based clustering (fallback method).
        Use DBSCAN for better results, but this is available for comparison.
        
        Args:
            datapoints: List of datapoint documents with embeddings
            similarity_threshold: Minimum cosine similarity for clustering
            min_cluster_size: Minimum number of datapoints in a cluster
            
        Returns:
            Dictionary mapping cluster_id to list of datapoints
        """
        clusters = {}
        used_indices = set()
        cluster_id_counter = 0
        
        for i, datapoint in enumerate(datapoints):
            if i in used_indices:
                continue
            
            if "embedding" not in datapoint or not datapoint["embedding"]:
                continue
            
            # Start a new cluster
            cluster_id = f"cluster_{cluster_id_counter}"
            cluster = [datapoint]
            used_indices.add(i)
            
            # Find similar datapoints
            for j, other_datapoint in enumerate(datapoints[i+1:], start=i+1):
                if j in used_indices:
                    continue
                
                if "embedding" not in other_datapoint or not other_datapoint["embedding"]:
                    continue
                
                similarity = self.cosine_similarity(
                    datapoint["embedding"],
                    other_datapoint["embedding"]
                )
                
                if similarity >= similarity_threshold:
                    cluster.append(other_datapoint)
                    used_indices.add(j)
            
            # Only keep clusters with minimum size
            if len(cluster) >= min_cluster_size:
                clusters[cluster_id] = cluster
                cluster_id_counter += 1
                
                # Update cluster_id in storage
                for dp in cluster:
                    self.storage_service.update_cluster_id(dp["_id"], cluster_id)
        
        logger.info(f"Created {len(clusters)} clusters from {len(datapoints)} datapoints")
        return clusters
    
    def cluster_datapoints_by_ids(
        self,
        datapoint_ids: List[str],
        min_cluster_size: Optional[int] = None,
        use_dbscan: bool = True,
        include_context: bool = True,
        context_hours: int = 168
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Cluster specific datapoints by their IDs, optionally including context from recent datapoints.
        
        Args:
            datapoint_ids: List of datapoint IDs to cluster
            min_cluster_size: Override min_samples for DBSCAN
            use_dbscan: Use DBSCAN (True) or simple similarity (False)
            include_context: If True, include other recent datapoints for better clustering context
            context_hours: Hours to look back for context datapoints
            
        Returns:
            Dictionary mapping cluster_id to list of datapoints
        """
        # Fetch datapoints by IDs
        target_datapoints = []
        for dp_id in datapoint_ids:
            dp = self.storage_service.get_datapoint(dp_id)
            if dp and dp.get("embedding"):
                target_datapoints.append(dp)
        
        if not target_datapoints:
            logger.warning(f"No datapoints found for IDs: {datapoint_ids}")
            return {}
        
        logger.info(f"Clustering {len(target_datapoints)} target datapoints")
        
        # Optionally include context datapoints for better clustering
        if include_context:
            context_datapoints = self.storage_service.get_recent_datapoints(hours=context_hours)
            # Filter to only include datapoints with embeddings
            context_datapoints = [dp for dp in context_datapoints if dp.get("embedding")]
            
            # Combine target and context, avoiding duplicates
            target_ids = {dp.get("_id") or dp.get("id") for dp in target_datapoints}
            context_datapoints = [dp for dp in context_datapoints if (dp.get("_id") or dp.get("id")) not in target_ids]
            
            all_datapoints = target_datapoints + context_datapoints
            logger.info(f"Including {len(context_datapoints)} context datapoints (total: {len(all_datapoints)})")
        else:
            all_datapoints = target_datapoints
        
        if use_dbscan:
            return self.cluster_datapoints(all_datapoints, min_cluster_size)
        else:
            min_size = min_cluster_size if min_cluster_size else 2
            return self.cluster_datapoints_simple(all_datapoints, min_cluster_size=min_size)
    
    def cluster_recent_datapoints(
        self,
        hours: int = 168,  # Default to 7 days to catch more datapoints
        min_cluster_size: Optional[int] = None,
        use_dbscan: bool = True,
        force_recluster: bool = False
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Cluster all recent unclustered datapoints.
        
        Args:
            hours: Look back this many hours (default: 168 = 7 days)
            min_cluster_size: Override min_samples for DBSCAN
            use_dbscan: Use DBSCAN (True) or simple similarity (False)
            force_recluster: If True, recluster even already-clustered datapoints
            
        Returns:
            Dictionary mapping cluster_id to list of datapoints
        """
        # Get recent datapoints
        recent = self.storage_service.get_recent_datapoints(hours=hours)
        
        # Filter unclustered unless force_recluster is True
        if force_recluster:
            unclustered = recent
            logger.info(f"Force reclustering: processing {len(unclustered)} datapoints (including already clustered)")
        else:
            unclustered = [dp for dp in recent if not dp.get("clustered", False)]
            logger.info(f"Found {len(unclustered)} unclustered datapoints out of {len(recent)} recent datapoints")
        
        if not unclustered:
            logger.info("No unclustered datapoints found")
            return {}
        
        if use_dbscan:
            return self.cluster_datapoints(unclustered, min_cluster_size)
        else:
            # Fallback to simple similarity-based clustering
            min_size = min_cluster_size if min_cluster_size else 2
            return self.cluster_datapoints_simple(unclustered, min_cluster_size=min_size)
    
    def get_cluster_statistics(self, clusters: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """
        Get statistics about clusters.
        
        Args:
            clusters: Dictionary of clusters from clustering operation
            
        Returns:
            Statistics dictionary
        """
        if not clusters:
            return {
                "total_clusters": 0,
                "total_datapoints": 0,
                "avg_cluster_size": 0,
                "largest_cluster": 0,
                "smallest_cluster": 0
            }
        
        cluster_sizes = [len(cluster) for cluster in clusters.values()]
        
        return {
            "total_clusters": len(clusters),
            "total_datapoints": sum(cluster_sizes),
            "avg_cluster_size": np.mean(cluster_sizes),
            "largest_cluster": max(cluster_sizes),
            "smallest_cluster": min(cluster_sizes),
            "cluster_size_distribution": {
                "small": len([s for s in cluster_sizes if s < 5]),
                "medium": len([s for s in cluster_sizes if 5 <= s < 20]),
                "large": len([s for s in cluster_sizes if s >= 20])
            }
        }

