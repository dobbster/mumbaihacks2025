#!/usr/bin/env python3
"""Test script for pattern detection functionality.

Run with: uv run python scripts/test_pattern_detection.py
"""

import os
import sys
from pathlib import Path
import logging

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.dependencies import get_pattern_detection_service, get_storage_service

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def test_pattern_detection():
    """Test pattern detection on existing clusters."""
    print("Testing Pattern Detection Service")
    print("=" * 60)
    
    try:
        # Initialize services
        pattern_service = get_pattern_detection_service()
        storage_service = get_storage_service()
        
        print("✅ Pattern detection service initialized")
        
        # Get all clusters
        all_datapoints = storage_service.datapoints_collection.find({"cluster_id": {"$exists": True, "$ne": None}})
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
        print(f"\n🔍 Analyzing cluster: {test_cluster_id}")
        print(f"   Datapoints: {len(clusters_map[test_cluster_id])}")
        
        # Run comprehensive analysis
        analysis = pattern_service.analyze_cluster(test_cluster_id)
        
        print("\n" + "=" * 60)
        print("COMPREHENSIVE ANALYSIS RESULTS")
        print("=" * 60)
        
        print(f"\n📈 Overall Risk Score: {analysis.get('overall_risk_score', 0.0):.3f}")
        print(f"   Risk Level: {analysis.get('risk_level', 'unknown').upper()}")
        print(f"   Flag Count: {analysis.get('flag_count', 0)}/4")
        print(f"   Recommendation: {analysis.get('recommendation', 'N/A')}")
        
        # Growth analysis
        growth = analysis.get('growth_analysis', {})
        print(f"\n📊 Rapid Growth Detection:")
        print(f"   Is Rapid Growth: {growth.get('is_rapid_growth', False)}")
        print(f"   Growth Rate: {growth.get('growth_rate', 0.0):.2f}x")
        print(f"   Datapoints/Hour: {growth.get('datapoints_per_hour', 0.0):.2f}")
        print(f"   Risk Score: {growth.get('risk_score', 0.0):.3f}")
        
        # Credibility analysis
        credibility = analysis.get('credibility_analysis', {})
        print(f"\n🔍 Source Credibility Analysis:")
        print(f"   Credible Ratio: {credibility.get('credible_ratio', 0.0):.3f}")
        print(f"   Credible Sources: {len(credibility.get('credible_sources', []))}")
        print(f"   Questionable Sources: {len(credibility.get('questionable_sources', []))}")
        print(f"   Source Diversity: {credibility.get('source_diversity', 0)}")
        print(f"   Risk Score: {credibility.get('risk_score', 0.0):.3f}")
        
        # Contradiction analysis
        contradictions = analysis.get('contradiction_analysis', {})
        print(f"\n⚠️ Contradiction Detection:")
        print(f"   Has Contradictions: {contradictions.get('has_contradictions', False)}")
        print(f"   Contradiction Count: {contradictions.get('contradiction_count', 0)}")
        print(f"   Risk Score: {contradictions.get('risk_score', 0.0):.3f}")
        
        # Evolution analysis
        evolution = analysis.get('evolution_analysis', {})
        print(f"\n📅 Narrative Evolution:")
        print(f"   Has Evolution: {evolution.get('has_evolution', False)}")
        print(f"   Evolution Stages: {evolution.get('total_stages', 0)}")
        print(f"   Key Changes: {evolution.get('change_count', 0)}")
        print(f"   Risk Score: {evolution.get('risk_score', 0.0):.3f}")
        
        # Flags
        flags = analysis.get('flags', {})
        print(f"\n🚩 Red Flags:")
        print(f"   Rapid Growth: {flags.get('rapid_growth', False)}")
        print(f"   Low Credibility: {flags.get('low_credibility', False)}")
        print(f"   Has Contradictions: {flags.get('has_contradictions', False)}")
        print(f"   Narrative Evolution: {flags.get('narrative_evolution', False)}")
        
        # Test analyze all clusters
        print("\n" + "=" * 60)
        print("ANALYZING ALL CLUSTERS")
        print("=" * 60)
        
        all_analyses = pattern_service.analyze_all_clusters(hours=8760, min_cluster_size=2)
        
        print(f"\n📊 Summary:")
        print(f"   Total Clusters Analyzed: {all_analyses.get('total_clusters_analyzed', 0)}")
        print(f"   High Risk: {all_analyses.get('high_risk_clusters', 0)}")
        print(f"   Medium Risk: {all_analyses.get('medium_risk_clusters', 0)}")
        print(f"   Low Risk: {all_analyses.get('low_risk_clusters', 0)}")
        print(f"   Average Risk Score: {all_analyses.get('average_risk_score', 0.0):.3f}")
        
        high_risk_ids = all_analyses.get('high_risk_cluster_ids', [])
        if high_risk_ids:
            print(f"\n⚠️ High-Risk Clusters:")
            for cluster_id in high_risk_ids[:5]:  # Show top 5
                cluster_analysis = all_analyses.get('analyses', {}).get(cluster_id, {})
                risk_score = cluster_analysis.get('overall_risk_score', 0.0)
                print(f"   - {cluster_id}: Risk Score {risk_score:.3f}")
        
        print("\n✅ Pattern detection test completed successfully!")
        
    except Exception as e:
        logger.error(f"An error occurred during pattern detection test: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    test_pattern_detection()

