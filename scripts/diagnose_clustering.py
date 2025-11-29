#!/usr/bin/env python3
"""Diagnose why clustering isn't finding clusters.

Run with: uv run python scripts/diagnose_clustering.py
"""

import os
import sys
import numpy as np
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.dependencies import get_storage_service
from app.core.clustering import ClusteringService

def diagnose_clustering():
    """Diagnose clustering issues."""
    print("Clustering Diagnosis")
    print("=" * 60)
    
    # Get storage service
    try:
        storage_service = get_storage_service()
        print("✅ Storage service initialized\n")
    except Exception as e:
        print(f"❌ Failed to initialize storage service: {e}")
        return False
    
    # Get all datapoints with embeddings
    all_datapoints = list(storage_service.datapoints_collection.find({}))
    datapoints_with_embeddings = [
        dp for dp in all_datapoints 
        if dp.get('embedding') and isinstance(dp.get('embedding'), list) and len(dp.get('embedding', [])) > 0
    ]
    
    print(f"📊 Database Status:")
    print(f"   Total datapoints: {len(all_datapoints)}")
    print(f"   Datapoints with valid embeddings: {len(datapoints_with_embeddings)}\n")
    
    if len(datapoints_with_embeddings) < 2:
        print("❌ Need at least 2 datapoints with embeddings to cluster")
        return False
    
    # Check embedding dimensions
    embedding_dims = [len(dp['embedding']) for dp in datapoints_with_embeddings]
    if len(set(embedding_dims)) > 1:
        print(f"⚠️  Warning: Inconsistent embedding dimensions: {set(embedding_dims)}")
    else:
        print(f"✅ All embeddings have dimension: {embedding_dims[0]}\n")
    
    # Calculate pairwise similarities
    print("🔍 Calculating Pairwise Similarities...")
    clustering_service = ClusteringService(storage_service)
    
    similarities = []
    for i, dp1 in enumerate(datapoints_with_embeddings):
        for j, dp2 in enumerate(datapoints_with_embeddings[i+1:], start=i+1):
            similarity = clustering_service.cosine_similarity(
                dp1['embedding'],
                dp2['embedding']
            )
            similarities.append({
                'dp1': dp1.get('title', dp1.get('_id', 'unknown'))[:40],
                'dp2': dp2.get('title', dp2.get('_id', 'unknown'))[:40],
                'similarity': similarity
            })
    
    if similarities:
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        
        print(f"\n📈 Similarity Statistics:")
        sim_values = [s['similarity'] for s in similarities]
        print(f"   Highest similarity: {max(sim_values):.4f}")
        print(f"   Lowest similarity: {min(sim_values):.4f}")
        print(f"   Average similarity: {np.mean(sim_values):.4f}")
        print(f"   Median similarity: {np.median(sim_values):.4f}")
        
        print(f"\n🔝 Top 5 Most Similar Pairs:")
        for i, pair in enumerate(similarities[:5], 1):
            print(f"   {i}. {pair['similarity']:.4f}")
            print(f"      - {pair['dp1']}")
            print(f"      - {pair['dp2']}")
        
        print(f"\n🔻 Bottom 5 Least Similar Pairs:")
        for i, pair in enumerate(similarities[-5:], 1):
            print(f"   {i}. {pair['similarity']:.4f}")
            print(f"      - {pair['dp1']}")
            print(f"      - {pair['dp2']}")
    
    # Test different eps values
    print(f"\n🧪 Testing Different DBSCAN Parameters:")
    print(f"   Current: eps=0.3, min_samples=2")
    
    test_configs = [
        (0.2, 2, "Stricter"),
        (0.3, 2, "Current"),
        (0.4, 2, "Looser"),
        (0.5, 2, "Very loose"),
        (0.3, 1, "Lower min_samples"),
    ]
    
    for eps, min_samples, label in test_configs:
        clustering_service = ClusteringService(
            storage_service=storage_service,
            eps=eps,
            min_samples=min_samples
        )
        
        try:
            clusters = clustering_service.cluster_datapoints(datapoints_with_embeddings)
            num_clusters = len(clusters)
            total_clustered = sum(len(c) for c in clusters.values())
            
            print(f"   {label:15} eps={eps:.1f}, min_samples={min_samples}: "
                  f"{num_clusters} clusters, {total_clustered} datapoints")
        except Exception as e:
            print(f"   {label:15} eps={eps:.1f}, min_samples={min_samples}: ERROR - {e}")
    
    # Recommendations
    print(f"\n💡 Recommendations:")
    if similarities:
        max_sim = max(sim_values)
        avg_sim = np.mean(sim_values)
        
        if max_sim < 0.3:
            print(f"   ⚠️  Your datapoints are very dissimilar (max similarity: {max_sim:.3f})")
            print(f"   → Try eps=0.15-0.2 for very strict clustering")
            print(f"   → Or ingest more similar/related datapoints")
        elif max_sim < 0.5:
            print(f"   ⚠️  Datapoints are moderately similar (max similarity: {max_sim:.3f})")
            print(f"   → Try eps=0.2-0.3")
        elif max_sim < 0.7:
            print(f"   ✅ Datapoints are reasonably similar (max similarity: {max_sim:.3f})")
            print(f"   → Try eps=0.3-0.4")
        else:
            print(f"   ✅ Datapoints are very similar (max similarity: {max_sim:.3f})")
            print(f"   → Try eps=0.4-0.5")
        
        if avg_sim < 0.3:
            print(f"   → Consider: Your datapoints cover very different topics")
            print(f"   → This is normal if they're from diverse sources")
            print(f"   → You may need topic-specific clustering or more data")
    
    return True

if __name__ == "__main__":
    success = diagnose_clustering()
    sys.exit(0 if success else 1)

