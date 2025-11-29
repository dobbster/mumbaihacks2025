"""API routes for public updates and reports."""

import logging
import asyncio
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Dict, Any, List, Optional

from app.core.public_updates import PublicUpdateService, PublicUpdate
from app.dependencies import (
    get_public_update_service
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/public-updates", tags=["public-updates"])


@router.get("/cluster/{cluster_id}", response_model=Dict[str, Any])
async def get_cluster_update(
    cluster_id: str,
    use_llm: bool = Query(True, description="Use LLM for natural language generation"),
    public_update_service: PublicUpdateService = Depends(get_public_update_service)
) -> Dict[str, Any]:
    """
    Get a user-friendly public update for a specific cluster.
    
    Returns a JSON-formatted update with:
    - Easy-to-understand summary
    - Key findings
    - Recommendations
    - Evidence summary
    - Source links
    """
    try:
        update = await asyncio.to_thread(
            public_update_service.generate_update,
            cluster_id,
            use_llm
        )
        
        return {
            "status": "success",
            "update": update.model_dump()
        }
        
    except Exception as e:
        logger.error(f"Error generating update for cluster {cluster_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/all", response_model=Dict[str, Any])
async def get_all_updates(
    hours: int = Query(168, description="Look back this many hours for clusters"),
    min_cluster_size: int = Query(2, description="Minimum cluster size"),
    use_llm: bool = Query(False, description="Use LLM for generation (slower but better quality)"),
    public_update_service: PublicUpdateService = Depends(get_public_update_service)
) -> Dict[str, Any]:
    """
    Get public updates for all clusters.
    
    Returns a list of JSON-formatted updates.
    """
    try:
        updates = await asyncio.to_thread(
            public_update_service.generate_updates_for_all_clusters,
            hours,
            min_cluster_size,
            use_llm
        )
        
        return {
            "status": "success",
            "total_updates": len(updates),
            "updates": [update.model_dump() for update in updates]
        }
        
    except Exception as e:
        logger.error(f"Error generating all updates: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/alerts", response_model=Dict[str, Any])
async def get_misinformation_alerts(
    hours: int = Query(168, description="Look back this many hours"),
    min_confidence: float = Query(0.7, description="Minimum confidence for alerts"),
    public_update_service: PublicUpdateService = Depends(get_public_update_service)
) -> Dict[str, Any]:
    """
    Get alerts for high-confidence misinformation.
    
    Returns JSON-formatted alerts sorted by severity and confidence.
    """
    try:
        alerts = await asyncio.to_thread(
            public_update_service.generate_misinformation_alerts,
            hours,
            min_confidence
        )
        
        # Group by severity
        high_severity = [a for a in alerts if a.severity == "high"]
        medium_severity = [a for a in alerts if a.severity == "medium"]
        low_severity = [a for a in alerts if a.severity == "low"]
        
        return {
            "status": "success",
            "total_alerts": len(alerts),
            "high_severity": len(high_severity),
            "medium_severity": len(medium_severity),
            "low_severity": len(low_severity),
            "alerts": [alert.model_dump() for alert in alerts]
        }
        
    except Exception as e:
        logger.error(f"Error generating alerts: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/summary", response_model=Dict[str, Any])
async def get_system_summary(
    hours: int = Query(168, description="Look back this many hours"),
    min_cluster_size: int = Query(2, description="Minimum cluster size"),
    public_update_service: PublicUpdateService = Depends(get_public_update_service)
) -> Dict[str, Any]:
    """
    Get a high-level summary of all detected misinformation.
    
    Returns a JSON summary with statistics and key findings.
    """
    try:
        updates = await asyncio.to_thread(
            public_update_service.generate_updates_for_all_clusters,
            hours,
            min_cluster_size,
            use_llm=False  # Faster for summary
        )
        
        # Calculate statistics
        total_clusters = len(updates)
        misinformation_count = sum(1 for u in updates if u.status == "misinformation")
        legitimate_count = sum(1 for u in updates if u.status == "legitimate")
        uncertain_count = sum(1 for u in updates if u.status == "uncertain")
        
        high_severity = sum(1 for u in updates if u.severity == "high")
        medium_severity = sum(1 for u in updates if u.severity == "medium")
        low_severity = sum(1 for u in updates if u.severity == "low")
        
        avg_confidence = sum(u.confidence for u in updates) / len(updates) if updates else 0.0
        avg_risk_score = sum(u.risk_score for u in updates) / len(updates) if updates else 0.0
        
        # Top alerts
        top_alerts = sorted(
            [u for u in updates if u.status == "misinformation"],
            key=lambda x: (x.confidence, x.risk_score),
            reverse=True
        )[:5]
        
        return {
            "status": "success",
            "summary": {
                "total_clusters_analyzed": total_clusters,
                "misinformation_detected": misinformation_count,
                "legitimate_news": legitimate_count,
                "uncertain": uncertain_count,
                "severity_breakdown": {
                    "high": high_severity,
                    "medium": medium_severity,
                    "low": low_severity
                },
                "average_confidence": round(avg_confidence, 3),
                "average_risk_score": round(avg_risk_score, 3)
            },
            "top_alerts": [alert.model_dump() for alert in top_alerts],
            "timestamp": updates[0].timestamp if updates else None
        }
        
    except Exception as e:
        logger.error(f"Error generating summary: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/feed", response_model=Dict[str, Any])
async def get_public_feed(
    hours: int = Query(24, description="Look back this many hours"),
    limit: int = Query(10, description="Maximum number of updates to return"),
    severity: Optional[str] = Query(None, description="Filter by severity: 'high', 'medium', or 'low'"),
    status: Optional[str] = Query(None, description="Filter by status: 'misinformation', 'legitimate', or 'uncertain'"),
    public_update_service: PublicUpdateService = Depends(get_public_update_service)
) -> Dict[str, Any]:
    """
    Get a public feed of updates (RSS-like format).
    
    Returns JSON-formatted updates suitable for public consumption.
    """
    try:
        updates = await asyncio.to_thread(
            public_update_service.generate_updates_for_all_clusters,
            hours,
            min_cluster_size=2,
            use_llm=False  # Faster for feed
        )
        
        # Apply filters
        if severity:
            updates = [u for u in updates if u.severity == severity]
        
        if status:
            updates = [u for u in updates if u.status == status]
        
        # Sort by timestamp (newest first)
        updates.sort(key=lambda x: x.timestamp, reverse=True)
        
        # Limit results
        updates = updates[:limit]
        
        return {
            "status": "success",
            "feed": {
                "title": "Misinformation Detection Updates",
                "description": "Real-time updates on detected misinformation",
                "last_updated": updates[0].timestamp if updates else None,
                "total_items": len(updates),
                "items": [update.model_dump() for update in updates]
            }
        }
        
    except Exception as e:
        logger.error(f"Error generating feed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

