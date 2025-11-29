"""API routes for misinformation classification."""

import logging
import asyncio
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Dict, Any, Optional

from app.core.classification import ClassificationService
from app.core.pattern_detection import PatternDetectionService
from app.core.storage import StorageService
from app.dependencies import (
    get_classification_service,
    get_pattern_detection_service,
    get_storage_service
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/classification", tags=["classification"])


@router.post("/cluster/{cluster_id}")
async def classify_cluster(
    cluster_id: str,
    classification_service: ClassificationService = Depends(get_classification_service),
    pattern_service: PatternDetectionService = Depends(get_pattern_detection_service),
    storage_service: StorageService = Depends(get_storage_service)
) -> Dict[str, Any]:
    """
    Classify a cluster as misinformation or legitimate news using LLM analysis.
    
    This endpoint:
    1. Runs pattern detection on the cluster
    2. Uses LLM to analyze the patterns
    3. Returns classification with confidence score and evidence chain
    """
    try:
        # Get cluster datapoints
        cluster_datapoints = storage_service.get_datapoints_by_cluster(cluster_id)
        
        if not cluster_datapoints:
            raise HTTPException(
                status_code=404,
                detail=f"Cluster {cluster_id} not found or empty"
            )
        
        # Run pattern detection
        pattern_analysis = await asyncio.to_thread(
            pattern_service.analyze_cluster,
            cluster_id
        )
        
        # Classify using LLM
        classification_result = await asyncio.to_thread(
            classification_service.classify_cluster,
            cluster_id,
            pattern_analysis,
            cluster_datapoints
        )
        
        return {
            "status": "success",
            "cluster_id": cluster_id,
            "classification": classification_result.model_dump(),
            "pattern_analysis": pattern_analysis
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error classifying cluster {cluster_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-all")
async def classify_all_clusters(
    hours: int = Query(168, description="Look back this many hours for clusters"),
    min_cluster_size: int = Query(2, description="Minimum cluster size to analyze"),
    classification_service: ClassificationService = Depends(get_classification_service),
    pattern_service: PatternDetectionService = Depends(get_pattern_detection_service),
    storage_service: StorageService = Depends(get_storage_service)
) -> Dict[str, Any]:
    """
    Classify all clusters found in recent datapoints.
    
    Returns classification results for all clusters with pattern analysis.
    """
    try:
        # Analyze all clusters for patterns
        pattern_results = await asyncio.to_thread(
            pattern_service.analyze_all_clusters,
            hours,
            min_cluster_size
        )
        
        analyses = pattern_results.get("analyses", {})
        
        # Classify each cluster
        classifications = {}
        for cluster_id, pattern_analysis in analyses.items():
            try:
                # Get cluster datapoints
                cluster_datapoints = storage_service.get_datapoints_by_cluster(cluster_id)
                
                # Classify
                classification_result = await asyncio.to_thread(
                    classification_service.classify_cluster,
                    cluster_id,
                    pattern_analysis,
                    cluster_datapoints
                )
                
                classifications[cluster_id] = classification_result.model_dump()
                
            except Exception as e:
                logger.error(f"Error classifying cluster {cluster_id}: {e}", exc_info=True)
                classifications[cluster_id] = {
                    "error": str(e),
                    "classification": "error"
                }
        
        # Summary statistics
        misinformation_count = sum(
            1 for c in classifications.values()
            if c.get("is_misinformation") is True
        )
        legitimate_count = sum(
            1 for c in classifications.values()
            if c.get("is_misinformation") is False and c.get("classification") == "legitimate"
        )
        uncertain_count = sum(
            1 for c in classifications.values()
            if c.get("classification") == "uncertain"
        )
        
        avg_confidence = sum(
            c.get("confidence", 0.0) for c in classifications.values()
            if "confidence" in c
        ) / len(classifications) if classifications else 0.0
        
        return {
            "status": "success",
            "summary": {
                "total_clusters_classified": len(classifications),
                "misinformation": misinformation_count,
                "legitimate": legitimate_count,
                "uncertain": uncertain_count,
                "average_confidence": round(avg_confidence, 3)
            },
            "classifications": classifications
        }
        
    except Exception as e:
        logger.error(f"Error classifying all clusters: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/misinformation-clusters")
async def get_misinformation_clusters(
    hours: int = Query(168, description="Look back this many hours for clusters"),
    min_cluster_size: int = Query(2, description="Minimum cluster size"),
    min_confidence: float = Query(0.7, description="Minimum confidence score"),
    classification_service: ClassificationService = Depends(get_classification_service),
    pattern_service: PatternDetectionService = Depends(get_pattern_detection_service),
    storage_service: StorageService = Depends(get_storage_service)
) -> Dict[str, Any]:
    """
    Get all clusters classified as misinformation with high confidence.
    
    Returns clusters that are:
    - Classified as misinformation
    - Have confidence >= min_confidence
    - Sorted by confidence (highest first)
    """
    try:
        # Analyze and classify all clusters
        pattern_results = await asyncio.to_thread(
            pattern_service.analyze_all_clusters,
            hours,
            min_cluster_size
        )
        
        analyses = pattern_results.get("analyses", {})
        
        misinformation_clusters = []
        
        for cluster_id, pattern_analysis in analyses.items():
            try:
                # Get cluster datapoints
                cluster_datapoints = storage_service.get_datapoints_by_cluster(cluster_id)
                
                # Classify
                classification_result = await asyncio.to_thread(
                    classification_service.classify_cluster,
                    cluster_id,
                    pattern_analysis,
                    cluster_datapoints
                )
                
                # Filter for misinformation with high confidence
                if (classification_result.is_misinformation and 
                    classification_result.confidence >= min_confidence):
                    misinformation_clusters.append({
                        "cluster_id": cluster_id,
                        "confidence": classification_result.confidence,
                        "classification": classification_result.classification,
                        "key_indicators": classification_result.key_indicators,
                        "reasoning": classification_result.reasoning[:200] + "..." if len(classification_result.reasoning) > 200 else classification_result.reasoning,
                        "risk_score": pattern_analysis.get("overall_risk_score", 0.0),
                        "datapoint_count": pattern_analysis.get("datapoint_count", 0)
                    })
                    
            except Exception as e:
                logger.error(f"Error processing cluster {cluster_id}: {e}", exc_info=True)
                continue
        
        # Sort by confidence (highest first)
        misinformation_clusters.sort(key=lambda x: x["confidence"], reverse=True)
        
        return {
            "status": "success",
            "misinformation_clusters": misinformation_clusters,
            "count": len(misinformation_clusters),
            "min_confidence": min_confidence
        }
        
    except Exception as e:
        logger.error(f"Error getting misinformation clusters: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

