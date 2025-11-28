#!/usr/bin/env python3
"""Test script for topic clustering functionality.

Run with: uv run python scripts/test_clustering.py
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.core.clustering import ClusteringService
from app.dependencies import get_storage_service

def test_clustering():
    """Test clustering functionality."""
    print("Testing Topic Clustering")
    print("=" * 60)
    
    # Get storage service
    try:
        storage_service = get_storage_service()
        print("✅ Storage service initialized")
    except Exception as e:
        print(f"❌ Failed to initialize storage service: {e}")
        return False
    
    # Get clustering service
    clustering_service = ClusteringService(
        storage_service=storage_service,
        eps=0.3,  # Adjust based on your data
        min_samples=2,
        metric="cosine"
    )
    print("✅ Clustering service initialized")
    print(f"   Configuration: eps={clustering_service.eps}, min_samples={clustering_service.min_samples}")
    
    # Check how many datapoints we have
    all_datapoints = list(storage_service.datapoints_collection.find({}))
    print(f"\n📊 Database Status:")
    print(f"   Total datapoints: {len(all_datapoints)}")
    
    with_embeddings = [dp for dp in all_datapoints if dp.get('embedding')]
    print(f"   Datapoints with embeddings: {len(with_embeddings)}")
    
    unclustered = [dp for dp in with_embeddings if not dp.get('clustered', False)]
    print(f"   Unclustered datapoints: {len(unclustered)}")
    
    if len(unclustered) < 2:
        print(f"\n⚠️  Need at least 2 unclustered datapoints to test clustering")
        print(f"   Try ingesting more datapoints first")
        return False
    
    # Test clustering
    print(f"\n🔍 Running DBSCAN clustering on {len(unclustered)} datapoints...")
    try:
        clusters = clustering_service.cluster_recent_datapoints(
            hours=168,  # Last 7 days
            min_cluster_size=2,
            use_dbscan=True
        )
        
        if not clusters:
            print("❌ No clusters found. Try:")
            print("   1. Adjusting eps (lower = stricter, higher = looser)")
            print("   2. Lowering min_samples (currently 2)")
            print("   3. Ingesting more similar datapoints")
            return False
        
        # Get statistics
        stats = clustering_service.get_cluster_statistics(clusters)
        
        print(f"\n✅ Clustering Complete!")
        print(f"\n📈 Cluster Statistics:")
        print(f"   Total clusters: {stats['total_clusters']}")
        print(f"   Total clustered datapoints: {stats['total_datapoints']}")
        print(f"   Average cluster size: {stats['avg_cluster_size']:.2f}")
        print(f"   Largest cluster: {stats['largest_cluster']} datapoints")
        print(f"   Smallest cluster: {stats['smallest_cluster']} datapoints")
        print(f"\n   Size distribution:")
        print(f"     Small (<5): {stats['cluster_size_distribution']['small']}")
        print(f"     Medium (5-19): {stats['cluster_size_distribution']['medium']}")
        print(f"     Large (20+): {stats['cluster_size_distribution']['large']}")
        
        # Show sample clusters
        print(f"\n📋 Sample Clusters:")
        for i, (cluster_id, datapoints) in enumerate(list(clusters.items())[:5], 1):
            print(f"\n   Cluster {i} ({cluster_id}): {len(datapoints)} datapoints")
            # Show first datapoint as example
            if datapoints:
                sample = datapoints[0]
                print(f"     Sample: {sample.get('title', 'N/A')[:60]}...")
                print(f"     Source: {sample.get('source_name', 'N/A')}")
                print(f"     Categories: {', '.join(sample.get('categories', [])[:3])}")
        
        if len(clusters) > 5:
            print(f"\n   ... and {len(clusters) - 5} more clusters")
        
        return True
        
    except Exception as e:
        print(f"❌ Clustering failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def show_cluster_details():
    """Show detailed information about clusters."""
    print("\n" + "=" * 60)
    print("Cluster Details")
    print("=" * 60)
    
    try:
        storage_service = get_storage_service()
        
        # Get all clustered datapoints grouped by cluster
        pipeline = [
            {"$match": {"clustered": True, "cluster_id": {"$exists": True}}},
            {"$group": {
                "_id": "$cluster_id",
                "count": {"$sum": 1},
                "sources": {"$addToSet": "$source_name"},
                "categories": {"$addToSet": "$categories"}
            }},
            {"$sort": {"count": -1}}
        ]
        
        cluster_groups = list(storage_service.datapoints_collection.aggregate(pipeline))
        
        if not cluster_groups:
            print("No clusters found in database")
            return
        
        print(f"\nFound {len(cluster_groups)} clusters:\n")
        
        for group in cluster_groups:
            cluster_id = group["_id"]
            count = group["count"]
            sources = group.get("sources", [])
            categories = set()
            for cat_list in group.get("categories", []):
                if isinstance(cat_list, list):
                    categories.update(cat_list)
            
            print(f"  {cluster_id}:")
            print(f"    Size: {count} datapoints")
            print(f"    Sources: {', '.join(sources[:3])}")
            print(f"    Topics: {', '.join(list(categories)[:5])}")
            print()
        
    except Exception as e:
        print(f"❌ Failed to get cluster details: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    success = test_clustering()
    if success:
        show_cluster_details()
    sys.exit(0 if success else 1)

