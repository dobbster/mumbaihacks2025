#!/usr/bin/env python3
"""Test script for public updates functionality.

Run with: uv run python scripts/test_public_updates.py
"""

import os
import sys
from pathlib import Path
import logging
import json

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.dependencies import get_public_update_service, get_storage_service

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def test_public_updates():
    """Test public updates generation."""
    print("Testing Public Updates Service")
    print("=" * 60)
    
    try:
        # Initialize services
        public_update_service = get_public_update_service()
        storage_service = get_storage_service()
        
        print("✅ Public update service initialized")
        
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
        print(f"\n🔍 Testing public update generation for cluster: {test_cluster_id}")
        print(f"   Datapoints: {len(clusters_map[test_cluster_id])}")
        
        # Generate update (without LLM for speed)
        print("\n📝 Generating public update (template-based)...")
        update = public_update_service.generate_update(test_cluster_id, use_llm=False)
        
        print("\n" + "=" * 60)
        print("PUBLIC UPDATE (JSON FORMAT)")
        print("=" * 60)
        
        # Print as formatted JSON
        update_dict = update.model_dump()
        print(json.dumps(update_dict, indent=2))
        
        print("\n" + "=" * 60)
        print("HUMAN-READABLE SUMMARY")
        print("=" * 60)
        
        print(f"\n📰 Title: {update.title}")
        print(f"\n📋 Summary: {update.summary}")
        print(f"\n🏷️  Status: {update.status.upper()} (Severity: {update.severity.upper()})")
        print(f"   Confidence: {update.confidence:.1%}")
        print(f"   Risk Score: {update.risk_score:.3f}")
        
        print(f"\n💭 Explanation:")
        print(f"   {update.explanation}")
        
        print(f"\n🔍 Key Findings:")
        for finding in update.key_findings:
            print(f"   • {finding}")
        
        print(f"\n💡 Recommendations:")
        for rec in update.recommendations:
            print(f"   • {rec}")
        
        print(f"\n✅ Credible Sources: {len(update.credible_sources)}")
        for source in update.credible_sources[:5]:
            print(f"   - {source}")
        
        print(f"\n🔍 Fact-Check Sources: {len(update.fact_check_sources)}")
        for fc in update.fact_check_sources[:3]:
            print(f"   - [{fc.get('source', 'Unknown')}] {fc.get('verdict', 'unknown')}")
            print(f"     {fc.get('title', 'No title')[:60]}...")
        
        print(f"\n📊 Evidence Summary: {update.evidence_summary}")
        
        print(f"\n🔗 Sources ({len(update.sources)}):")
        for i, url in enumerate(update.sources[:5], 1):
            print(f"   {i}. {url[:80]}...")
        
        print("\n✅ Public update test completed successfully!")
        
        # Test alerts
        print("\n" + "=" * 60)
        print("MISINFORMATION ALERTS TEST")
        print("=" * 60)
        
        alerts = public_update_service.generate_misinformation_alerts(
            hours=8760,
            min_confidence=0.5
        )
        
        print(f"\n🚨 Found {len(alerts)} misinformation alerts")
        
        if alerts:
            print("\nTop 3 Alerts:")
            for i, alert in enumerate(alerts[:3], 1):
                print(f"\n   {i}. {alert.title}")
                print(f"      Status: {alert.status}, Severity: {alert.severity}")
                print(f"      Confidence: {alert.confidence:.1%}")
                print(f"      Summary: {alert.summary[:80]}...")
        
        # API endpoint info
        print("\n" + "=" * 60)
        print("API ENDPOINT TEST")
        print("=" * 60)
        print("\nTo test via API, run:")
        print(f"   curl 'http://localhost:2024/public-updates/cluster/{test_cluster_id}'")
        print("\nTo get all updates:")
        print("   curl 'http://localhost:2024/public-updates/all?hours=8760'")
        print("\nTo get alerts:")
        print("   curl 'http://localhost:2024/public-updates/alerts?min_confidence=0.7'")
        print("\nTo get summary:")
        print("   curl 'http://localhost:2024/public-updates/summary'")
        print("\nTo get feed:")
        print("   curl 'http://localhost:2024/public-updates/feed?hours=24&limit=10'")
        
    except Exception as e:
        logger.error(f"An error occurred during public updates test: {e}", exc_info=True)
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    test_public_updates()

