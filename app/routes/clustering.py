"""API routes for topic clustering."""

import asyncio
import logging
from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from app.core.clustering import ClusteringService
from app.dependencies import get_storage_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/clustering", tags=["clustering"])


class ClusterResponse(BaseModel):
    """Response model for clustering."""
    status: str
    clusters_found: int
    total_datapoints_clustered: int
    statistics: Dict[str, Any]
    clusters: Dict[str, List[Dict[str, Any]]]


class ClusterStatsResponse(BaseModel):
    """Response model for cluster statistics."""
    total_clusters: int
    total_datapoints: int
    cluster_details: List[Dict[str, Any]]


@router.post("/cluster", response_model=ClusterResponse)
async def cluster_datapoints(
    hours: int = Query(168, description="Look back this many hours (default: 168 = 7 days)"),
    min_cluster_size: Optional[int] = Query(2, description="Minimum cluster size"),
    eps: Optional[float] = Query(None, description="DBSCAN eps parameter (0.0-1.0, default: 0.4)"),
    use_dbscan: bool = Query(True, description="Use DBSCAN (True) or simple similarity (False)"),
    force_recluster: bool = Query(False, description="Recluster even already-clustered datapoints"),
    storage_service = Depends(get_storage_service)
):
    """
    Cluster recent unclustered datapoints into topic groups.
    
    Uses DBSCAN algorithm to automatically discover topic clusters based on
    semantic similarity of embeddings.
    """
    try:
        # Initialize clustering service
        clustering_service = ClusteringService(
            storage_service=storage_service,
            eps=eps if eps is not None else 0.3,
            min_samples=min_cluster_size if min_cluster_size else 2
        )
        
        # Run clustering in thread pool (blocking operation)
        clusters = await asyncio.to_thread(
            clustering_service.cluster_recent_datapoints,
            hours=hours,
            min_cluster_size=min_cluster_size,
            use_dbscan=use_dbscan,
            force_recluster=force_recluster
        )
        
        # Get statistics
        stats = clustering_service.get_cluster_statistics(clusters)
        
        # Convert clusters to serializable format
        clusters_dict = {}
        for cluster_id, datapoints in clusters.items():
            clusters_dict[cluster_id] = [
                {
                    "id": dp.get("_id"),
                    "title": dp.get("title"),
                    "source_name": dp.get("source_name"),
                    "source_type": dp.get("source_type"),
                    "published_at": str(dp.get("published_at")),
                    "categories": dp.get("categories", [])
                }
                for dp in datapoints
            ]
        
        return ClusterResponse(
            status="success",
            clusters_found=len(clusters),
            total_datapoints_clustered=stats["total_datapoints"],
            statistics=stats,
            clusters=clusters_dict
        )
        
    except Exception as e:
        logger.error(f"Failed to cluster datapoints: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats", response_model=ClusterStatsResponse)
async def get_cluster_stats(
    storage_service = Depends(get_storage_service)
):
    """Get statistics about existing clusters."""
    try:
        # Aggregate cluster statistics
        pipeline = [
            {"$match": {"clustered": True, "cluster_id": {"$exists": True}}},
            {"$group": {
                "_id": "$cluster_id",
                "count": {"$sum": 1},
                "sources": {"$addToSet": "$source_name"},
                "categories": {"$addToSet": "$categories"},
                "earliest": {"$min": "$published_at"},
                "latest": {"$max": "$published_at"}
            }},
            {"$sort": {"count": -1}}
        ]
        
        cluster_groups = list(storage_service.datapoints_collection.aggregate(pipeline))
        
        cluster_details = []
        total_datapoints = 0
        
        for group in cluster_groups:
            cluster_id = group["_id"]
            count = group["count"]
            total_datapoints += count
            
            # Flatten categories
            categories = set()
            for cat_list in group.get("categories", []):
                if isinstance(cat_list, list):
                    categories.update(cat_list)
            
            cluster_details.append({
                "cluster_id": cluster_id,
                "size": count,
                "sources": list(group.get("sources", [])),
                "topics": list(categories),
                "earliest": str(group.get("earliest", "")),
                "latest": str(group.get("latest", ""))
            })
        
        return ClusterStatsResponse(
            total_clusters=len(cluster_details),
            total_datapoints=total_datapoints,
            cluster_details=cluster_details
        )
        
    except Exception as e:
        logger.error(f"Failed to get cluster stats: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

