#!/usr/bin/env python3
"""Test script for verification functionality.

Run with: uv run python scripts/test_verification.py
"""

import os
import sys
from pathlib import Path
import logging

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.dependencies import (
    get_verification_service,
    get_storage_service,
    get_classification_service,
    get_pattern_detection_service
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def test_verification():
    """Test verification on existing clusters."""
    print("Testing Verification Service")
    print("=" * 60)
    
    try:
        # Initialize services
        verification_service = get_verification_service()
        storage_service = get_storage_service()
        classification_service = get_classification_service()
        pattern_service = get_pattern_detection_service()
        
        print("✅ Verification service initialized")
        
        # Get all clusters
        all_datapoints = storage_service.datapoints_collection.find(
            {"cluster_id": {"$exists": True, "$ne": None}}
        )
        clusters_map = {}
        
        for dp in all_datapoints:
            cluster_id = dp.get("cluster_id")
            if cluster_id:
                if cluster_id not in clusters_map:
                    clusters_map[cluster_id] = []
                clusters_map[cluster_id].append(dp)
        
        print(f"\n📊 Found {len(clusters_map)} clusters in database")
        
        if not clusters_map:
            print("\n⚠️ No clusters found. Please run clustering first:")
            print("   curl -X POST 'http://localhost:2024/clustering/cluster?hours=8760&eps=0.30&min_cluster_size=2'")
            return
        
        # Test on first cluster
        test_cluster_id = list(clusters_map.keys())[0]
        print(f"\n🔍 Testing verification on cluster: {test_cluster_id}")
        print(f"   Datapoints: {len(clusters_map[test_cluster_id])}")
        
        # Run pattern detection and classification for context
        print("\n📊 Running pattern detection and classification...")
        pattern_analysis = pattern_service.analyze_cluster(test_cluster_id)
        cluster_datapoints = storage_service.get_datapoints_by_cluster(test_cluster_id)
        classification_result = classification_service.classify_cluster(
            test_cluster_id,
            pattern_analysis,
            cluster_datapoints
        )
        classification_dict = classification_result.model_dump()
        
        print(f"   Classification: {classification_result.classification}")
        print(f"   Confidence: {classification_result.confidence:.3f}")
        
        # Verify cluster
        print("\n✅ Verifying cluster...")
        verification_result = verification_service.verify_cluster(
            test_cluster_id,
            classification_dict
        )
        
        # Build evidence chain
        evidence_chain = verification_service.build_evidence_chain(
            test_cluster_id,
            verification_result
        )
        
        print("\n" + "=" * 60)
        print("VERIFICATION RESULTS")
        print("=" * 60)
        
        print(f"\n✅ Verification Status: {verification_result.verification_status.upper()}")
        print(f"   Is Verified: {verification_result.is_verified}")
        print(f"   Confidence: {verification_result.confidence:.3f} ({verification_result.confidence*100:.1f}%)")
        
        print(f"\n📋 Fact-Check Sources: {len(verification_result.fact_check_sources)}")
        for i, fc in enumerate(verification_result.fact_check_sources[:3], 1):
            print(f"   {i}. [{fc.get('source', 'Unknown')}] {fc.get('title', 'No title')[:60]}...")
            print(f"      Verdict: {fc.get('verdict', 'unknown')}")
            print(f"      URL: {fc.get('url', 'N/A')[:60]}...")
        
        print(f"\n🔗 Cross-References: {len(verification_result.cross_references)}")
        for i, cr in enumerate(verification_result.cross_references[:3], 1):
            print(f"   {i}. {cr.get('source', 'Unknown')} ({cr.get('count', 0)} articles)")
            print(f"      Credibility: {cr.get('credibility', 0.0):.2f}")
        
        print(f"\n✅ Evidence For: {len(verification_result.evidence_for)}")
        for evidence in verification_result.evidence_for:
            print(f"   - {evidence}")
        
        print(f"\n❌ Evidence Against: {len(verification_result.evidence_against)}")
        for evidence in verification_result.evidence_against:
            print(f"   - {evidence}")
        
        print(f"\n📝 Verification Summary:")
        print(f"   {verification_result.verification_summary}")
        
        print(f"\n🔗 Evidence Chain ({len(evidence_chain)} steps):")
        for step in evidence_chain:
            print(f"   Step {step.get('step', '?')} ({step.get('type', 'unknown')}):")
            print(f"      {step.get('description', 'N/A')}")
            print(f"      Weight: {step.get('weight', 0.0):.2f}")
        
        print(f"\n📎 Sources ({len(verification_result.sources)}):")
        for i, url in enumerate(verification_result.sources[:5], 1):
            print(f"   {i}. {url[:80]}...")
        
        print("\n✅ Verification test completed successfully!")
        
        # Test claim verification
        print("\n" + "=" * 60)
        print("CLAIM VERIFICATION TEST")
        print("=" * 60)
        
        test_claim = "Vaccines cause autism"
        print(f"\n🔍 Verifying claim: '{test_claim}'")
        claim_result = verification_service.verify_claim(test_claim)
        
        print(f"   Status: {claim_result.verification_status.upper()}")
        print(f"   Confidence: {claim_result.confidence:.3f}")
        print(f"   Summary: {claim_result.verification_summary}")
        
        print("\n✅ Claim verification test completed!")
        
        # API endpoint info
        print("\n" + "=" * 60)
        print("API ENDPOINT TEST")
        print("=" * 60)
        print("\nTo test via API, run:")
        print(f"   curl -X POST 'http://localhost:2024/verification/cluster/{test_cluster_id}'")
        print("\nTo verify a claim:")
        print("   curl -X POST 'http://localhost:2024/verification/claim?claim=Vaccines%20are%20safe'")
        print("\nTo get verified clusters:")
        print("   curl 'http://localhost:2024/verification/verified-clusters?min_confidence=0.7'")
        
    except Exception as e:
        logger.error(f"An error occurred during verification test: {e}", exc_info=True)
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    test_verification()

