#!/usr/bin/env python3
"""Test script for classification functionality.

Run with: uv run python scripts/test_classification.py
"""

import os
import sys
from pathlib import Path
import logging

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.dependencies import (
    get_classification_service,
    get_pattern_detection_service,
    get_storage_service
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def test_classification():
    """Test classification on existing clusters."""
    print("Testing Classification Service")
    print("=" * 60)
    
    try:
        # Initialize services
        classification_service = get_classification_service()
        pattern_service = get_pattern_detection_service()
        storage_service = get_storage_service()
        
        print(f"✅ Classification service initialized")
        print(f"   Model: {classification_service.model_name}")
        print(f"   Temperature: {classification_service.temperature}")
        
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
        print(f"\n🔍 Testing classification on cluster: {test_cluster_id}")
        print(f"   Datapoints: {len(clusters_map[test_cluster_id])}")
        
        # Run pattern detection
        print("\n📊 Running pattern detection...")
        pattern_analysis = pattern_service.analyze_cluster(test_cluster_id)
        
        print(f"   Risk Score: {pattern_analysis.get('overall_risk_score', 0.0):.3f}")
        print(f"   Risk Level: {pattern_analysis.get('risk_level', 'unknown').upper()}")
        print(f"   Flags: {pattern_analysis.get('flag_count', 0)}/4")
        
        # Classify using LLM
        print("\n🤖 Classifying using LLM...")
        print("   (This may take 10-30 seconds)")
        
        cluster_datapoints = storage_service.get_datapoints_by_cluster(test_cluster_id)
        classification_result = classification_service.classify_cluster(
            test_cluster_id,
            pattern_analysis,
            cluster_datapoints
        )
        
        print("\n" + "=" * 60)
        print("CLASSIFICATION RESULTS")
        print("=" * 60)
        
        print(f"\n✅ Classification: {classification_result.classification.upper()}")
        print(f"   Is Misinformation: {classification_result.is_misinformation}")
        print(f"   Confidence: {classification_result.confidence:.3f} ({classification_result.confidence*100:.1f}%)")
        
        print(f"\n📋 Key Indicators:")
        for indicator in classification_result.key_indicators[:5]:
            print(f"   - {indicator}")
        
        print(f"\n🔗 Evidence Chain ({len(classification_result.evidence_chain)} steps):")
        for i, evidence in enumerate(classification_result.evidence_chain[:3], 1):
            print(f"   Step {evidence.get('step', i)}:")
            print(f"      Evidence: {evidence.get('evidence', 'N/A')[:80]}...")
            print(f"      Weight: {evidence.get('weight', 0.0):.2f}")
            print(f"      Indicator: {evidence.get('indicator', 'unknown')}")
        
        if len(classification_result.evidence_chain) > 3:
            print(f"   ... {len(classification_result.evidence_chain) - 3} more steps")
        
        print(f"\n💭 Reasoning:")
        reasoning_lines = classification_result.reasoning.split('\n')[:5]
        for line in reasoning_lines:
            print(f"   {line}")
        if len(classification_result.reasoning.split('\n')) > 5:
            print(f"   ... (truncated)")
        
        if classification_result.supporting_evidence:
            print(f"\n✅ Supporting Evidence:")
            for evidence in classification_result.supporting_evidence[:3]:
                print(f"   - {evidence[:80]}...")
        
        if classification_result.contradictory_evidence:
            print(f"\n❌ Contradictory Evidence:")
            for evidence in classification_result.contradictory_evidence[:3]:
                print(f"   - {evidence[:80]}...")
        
        print("\n✅ Classification test completed successfully!")
        
        # Test API endpoint
        print("\n" + "=" * 60)
        print("API ENDPOINT TEST")
        print("=" * 60)
        print("\nTo test via API, run:")
        print(f"   curl -X POST 'http://localhost:2024/classification/cluster/{test_cluster_id}'")
        print("\nTo get all misinformation clusters:")
        print("   curl 'http://localhost:2024/classification/misinformation-clusters?min_confidence=0.7'")
        
    except Exception as e:
        logger.error(f"An error occurred during classification test: {e}", exc_info=True)
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure TOGETHER_API_KEY is set in environment")
        print("2. Check that langchain-community is installed: uv add langchain-community")
        print("3. Verify MongoDB is running and has clusters")
        sys.exit(1)


if __name__ == "__main__":
    test_classification()

