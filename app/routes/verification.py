"""API routes for verification and fact-checking."""

import logging
import asyncio
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Dict, Any, Optional

from app.core.verification import VerificationService
from app.core.classification import ClassificationService
from app.core.pattern_detection import PatternDetectionService
from app.dependencies import (
    get_verification_service,
    get_classification_service,
    get_pattern_detection_service,
    get_storage_service
)
from app.core.storage import StorageService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/verification", tags=["verification"])


@router.post("/cluster/{cluster_id}")
async def verify_cluster(
    cluster_id: str,
    include_classification: bool = Query(True, description="Include classification results in verification"),
    verification_service: VerificationService = Depends(get_verification_service),
    classification_service: ClassificationService = Depends(get_classification_service),
    pattern_service: PatternDetectionService = Depends(get_pattern_detection_service),
    storage_service: StorageService = Depends(get_storage_service)
) -> Dict[str, Any]:
    """
    Verify a cluster through fact-checking and cross-referencing.
    
    This endpoint:
    1. Finds fact-checking sources in the cluster
    2. Cross-references with credible sources
    3. Analyzes evidence for/against claims
    4. Provides verification status and confidence
    """
    try:
        # Get classification result if requested
        classification_result = None
        if include_classification:
            try:
                # Run pattern detection first
                pattern_analysis = await asyncio.to_thread(
                    pattern_service.analyze_cluster,
                    cluster_id
                )
                
                # Get cluster datapoints for classification
                cluster_datapoints = storage_service.get_datapoints_by_cluster(cluster_id)
                
                # Classify
                classification = await asyncio.to_thread(
                    classification_service.classify_cluster,
                    cluster_id,
                    pattern_analysis,
                    cluster_datapoints
                )
                classification_result = classification.model_dump()
            except Exception as e:
                logger.warning(f"Failed to get classification for verification: {e}")
        
        # Verify cluster
        verification_result = await asyncio.to_thread(
            verification_service.verify_cluster,
            cluster_id,
            classification_result
        )
        
        # Build evidence chain
        evidence_chain = await asyncio.to_thread(
            verification_service.build_evidence_chain,
            cluster_id,
            verification_result
        )
        
        return {
            "status": "success",
            "cluster_id": cluster_id,
            "verification": verification_result.model_dump(),
            "evidence_chain": evidence_chain,
            "classification": classification_result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error verifying cluster {cluster_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/claim")
async def verify_claim(
    claim: str = Query(..., description="The claim to verify"),
    context: Optional[str] = Query(None, description="Optional context about the claim"),
    verification_service: VerificationService = Depends(get_verification_service)
) -> Dict[str, Any]:
    """
    Verify a specific claim through fact-checking.
    
    This endpoint analyzes a claim and searches for fact-checking sources.
    """
    try:
        verification_result = await asyncio.to_thread(
            verification_service.verify_claim,
            claim,
            context
        )
        
        return {
            "status": "success",
            "claim": claim,
            "verification": verification_result.model_dump()
        }
        
    except Exception as e:
        logger.error(f"Error verifying claim: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/verify-all")
async def verify_all_clusters(
    hours: int = Query(168, description="Look back this many hours for clusters"),
    min_cluster_size: int = Query(2, description="Minimum cluster size"),
    include_classification: bool = Query(True, description="Include classification in verification"),
    verification_service: VerificationService = Depends(get_verification_service),
    classification_service: ClassificationService = Depends(get_classification_service),
    pattern_service: PatternDetectionService = Depends(get_pattern_detection_service),
    storage_service: StorageService = Depends(get_storage_service)
) -> Dict[str, Any]:
    """
    Verify all clusters found in recent datapoints.
    
    Returns verification results for all clusters.
    """
    try:
        # Get all clusters
        pattern_results = await asyncio.to_thread(
            pattern_service.analyze_all_clusters,
            hours,
            min_cluster_size
        )
        
        analyses = pattern_results.get("analyses", {})
        
        # Verify each cluster
        verifications = {}
        for cluster_id, pattern_analysis in analyses.items():
            try:
                # Get classification if requested
                classification_result = None
                if include_classification:
                    cluster_datapoints = storage_service.get_datapoints_by_cluster(cluster_id)
                    classification = await asyncio.to_thread(
                        classification_service.classify_cluster,
                        cluster_id,
                        pattern_analysis,
                        cluster_datapoints
                    )
                    classification_result = classification.model_dump()
                
                # Verify
                verification_result = await asyncio.to_thread(
                    verification_service.verify_cluster,
                    cluster_id,
                    classification_result
                )
                
                verifications[cluster_id] = {
                    "verification": verification_result.model_dump(),
                    "pattern_analysis": pattern_analysis,
                    "classification": classification_result
                }
                
            except Exception as e:
                logger.error(f"Error verifying cluster {cluster_id}: {e}", exc_info=True)
                verifications[cluster_id] = {
                    "error": str(e)
                }
        
        # Summary statistics
        verified_count = sum(
            1 for v in verifications.values()
            if v.get("verification", {}).get("is_verified", False)
        )
        false_count = sum(
            1 for v in verifications.values()
            if v.get("verification", {}).get("verification_status") == "false"
        )
        unverified_count = sum(
            1 for v in verifications.values()
            if v.get("verification", {}).get("verification_status") == "unverified"
        )
        
        avg_confidence = sum(
            v.get("verification", {}).get("confidence", 0.0)
            for v in verifications.values()
            if "verification" in v
        ) / len(verifications) if verifications else 0.0
        
        return {
            "status": "success",
            "summary": {
                "total_clusters_verified": len(verifications),
                "verified": verified_count,
                "false": false_count,
                "unverified": unverified_count,
                "average_confidence": round(avg_confidence, 3)
            },
            "verifications": verifications
        }
        
    except Exception as e:
        logger.error(f"Error verifying all clusters: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/verified-clusters")
async def get_verified_clusters(
    hours: int = Query(168, description="Look back this many hours"),
    min_confidence: float = Query(0.7, description="Minimum confidence score"),
    verification_service: VerificationService = Depends(get_verification_service),
    pattern_service: PatternDetectionService = Depends(get_pattern_detection_service),
    storage_service: StorageService = Depends(get_storage_service)
) -> Dict[str, Any]:
    """
    Get all clusters with high-confidence verification results.
    
    Returns clusters that are verified or confirmed as false.
    """
    try:
        # Get all clusters
        pattern_results = await asyncio.to_thread(
            pattern_service.analyze_all_clusters,
            hours,
            2
        )
        
        analyses = pattern_results.get("analyses", {})
        
        verified_clusters = []
        
        for cluster_id in analyses.keys():
            try:
                verification_result = await asyncio.to_thread(
                    verification_service.verify_cluster,
                    cluster_id,
                    None
                )
                
                if (verification_result.confidence >= min_confidence and
                    verification_result.verification_status != "unverified"):
                    verified_clusters.append({
                        "cluster_id": cluster_id,
                        "verification_status": verification_result.verification_status,
                        "confidence": verification_result.confidence,
                        "is_verified": verification_result.is_verified,
                        "summary": verification_result.verification_summary,
                        "fact_check_count": len(verification_result.fact_check_sources),
                        "cross_reference_count": len(verification_result.cross_references)
                    })
                    
            except Exception as e:
                logger.error(f"Error processing cluster {cluster_id}: {e}", exc_info=True)
                continue
        
        # Sort by confidence (highest first)
        verified_clusters.sort(key=lambda x: x["confidence"], reverse=True)
        
        return {
            "status": "success",
            "verified_clusters": verified_clusters,
            "count": len(verified_clusters),
            "min_confidence": min_confidence
        }
        
    except Exception as e:
        logger.error(f"Error getting verified clusters: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

