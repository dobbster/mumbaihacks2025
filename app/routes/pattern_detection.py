"""API routes for pattern detection."""

import logging
import asyncio
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Dict, Any, Optional

from app.core.pattern_detection import PatternDetectionService
from app.dependencies import get_pattern_detection_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/pattern-detection", tags=["pattern-detection"])


@router.get("/cluster/{cluster_id}")
async def analyze_cluster(
    cluster_id: str,
    pattern_service: PatternDetectionService = Depends(get_pattern_detection_service)
) -> Dict[str, Any]:
    """
    Analyze a specific cluster for misinformation patterns.
    
    Returns comprehensive analysis including:
    - Rapid growth detection
    - Source credibility analysis
    - Contradiction detection
    - Narrative evolution tracking
    - Overall risk score
    """
    try:
        analysis = await asyncio.to_thread(
            pattern_service.analyze_cluster,
            cluster_id
        )
        return {
            "status": "success",
            "analysis": analysis
        }
    except Exception as e:
        logger.error(f"Error analyzing cluster {cluster_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cluster/{cluster_id}/rapid-growth")
async def detect_rapid_growth(
    cluster_id: str,
    time_window_hours: int = Query(6, description="Time window in hours for growth analysis"),
    pattern_service: PatternDetectionService = Depends(get_pattern_detection_service)
) -> Dict[str, Any]:
    """
    Detect rapid growth in a cluster (indicator of misinformation spread).
    """
    try:
        analysis = await asyncio.to_thread(
            pattern_service.detect_rapid_growth,
            cluster_id,
            time_window_hours
        )
        return {
            "status": "success",
            "cluster_id": cluster_id,
            "rapid_growth_analysis": analysis
        }
    except Exception as e:
        logger.error(f"Error detecting rapid growth for cluster {cluster_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cluster/{cluster_id}/credibility")
async def analyze_source_credibility(
    cluster_id: str,
    pattern_service: PatternDetectionService = Depends(get_pattern_detection_service)
) -> Dict[str, Any]:
    """
    Analyze source credibility within a cluster.
    """
    try:
        analysis = await asyncio.to_thread(
            pattern_service.analyze_source_credibility,
            cluster_id
        )
        return {
            "status": "success",
            "cluster_id": cluster_id,
            "credibility_analysis": analysis
        }
    except Exception as e:
        logger.error(f"Error analyzing credibility for cluster {cluster_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cluster/{cluster_id}/contradictions")
async def detect_contradictions(
    cluster_id: str,
    similarity_threshold: float = Query(0.7, description="Minimum similarity threshold for contradiction detection"),
    pattern_service: PatternDetectionService = Depends(get_pattern_detection_service)
) -> Dict[str, Any]:
    """
    Detect contradictory claims within a cluster.
    """
    try:
        analysis = await asyncio.to_thread(
            pattern_service.detect_contradictions,
            cluster_id,
            similarity_threshold
        )
        return {
            "status": "success",
            "cluster_id": cluster_id,
            "contradiction_analysis": analysis
        }
    except Exception as e:
        logger.error(f"Error detecting contradictions for cluster {cluster_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cluster/{cluster_id}/evolution")
async def track_narrative_evolution(
    cluster_id: str,
    pattern_service: PatternDetectionService = Depends(get_pattern_detection_service)
) -> Dict[str, Any]:
    """
    Track how the narrative/story evolves over time within a cluster.
    """
    try:
        analysis = await asyncio.to_thread(
            pattern_service.track_narrative_evolution,
            cluster_id
        )
        return {
            "status": "success",
            "cluster_id": cluster_id,
            "evolution_analysis": analysis
        }
    except Exception as e:
        logger.error(f"Error tracking evolution for cluster {cluster_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-all")
async def analyze_all_clusters(
    hours: int = Query(168, description="Look back this many hours for clusters"),
    min_cluster_size: int = Query(2, description="Minimum cluster size to analyze"),
    pattern_service: PatternDetectionService = Depends(get_pattern_detection_service)
) -> Dict[str, Any]:
    """
    Analyze all clusters found in recent datapoints.
    
    Returns summary statistics and detailed analysis for each cluster.
    """
    try:
        results = await asyncio.to_thread(
            pattern_service.analyze_all_clusters,
            hours,
            min_cluster_size
        )
        return {
            "status": "success",
            "summary": {
                "total_clusters_analyzed": results.get("total_clusters_analyzed", 0),
                "high_risk_clusters": results.get("high_risk_clusters", 0),
                "medium_risk_clusters": results.get("medium_risk_clusters", 0),
                "low_risk_clusters": results.get("low_risk_clusters", 0),
                "average_risk_score": results.get("average_risk_score", 0.0),
                "high_risk_cluster_ids": results.get("high_risk_cluster_ids", [])
            },
            "analyses": results.get("analyses", {})
        }
    except Exception as e:
        logger.error(f"Error analyzing all clusters: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/high-risk-clusters")
async def get_high_risk_clusters(
    hours: int = Query(168, description="Look back this many hours for clusters"),
    min_cluster_size: int = Query(2, description="Minimum cluster size to analyze"),
    risk_threshold: float = Query(0.6, description="Minimum risk score to consider high-risk"),
    pattern_service: PatternDetectionService = Depends(get_pattern_detection_service)
) -> Dict[str, Any]:
    """
    Get all high-risk clusters (potential misinformation).
    
    Returns clusters with risk score above threshold, sorted by risk.
    """
    try:
        results = await asyncio.to_thread(
            pattern_service.analyze_all_clusters,
            hours,
            min_cluster_size
        )
        
        analyses = results.get("analyses", {})
        
        # Filter high-risk clusters
        high_risk = []
        for cluster_id, analysis in analyses.items():
            risk_score = analysis.get("overall_risk_score", 0.0)
            if risk_score >= risk_threshold:
                high_risk.append({
                    "cluster_id": cluster_id,
                    "risk_score": risk_score,
                    "risk_level": analysis.get("risk_level", "unknown"),
                    "flags": analysis.get("flags", {}),
                    "datapoint_count": analysis.get("datapoint_count", 0),
                    "recommendation": analysis.get("recommendation", "")
                })
        
        # Sort by risk score (highest first)
        high_risk.sort(key=lambda x: x["risk_score"], reverse=True)
        
        return {
            "status": "success",
            "high_risk_clusters": high_risk,
            "count": len(high_risk),
            "risk_threshold": risk_threshold
        }
    except Exception as e:
        logger.error(f"Error getting high-risk clusters: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

