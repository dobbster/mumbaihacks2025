#!/usr/bin/env python3
"""Test clustering with different parameters and recommend optimal settings.

Run with: uv run python scripts/test_clustering_params.py
"""

import os
import sys
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.dependencies import get_storage_service
from app.core.clustering import ClusteringService

def test_parameter_combinations():
    """Test different parameter combinations and recommend best settings."""
    print("Clustering Parameter Testing & Recommendations")
    print("=" * 70)
    
    # Get storage service
    try:
        storage_service = get_storage_service()
        print("✅ Storage service initialized\n")
    except Exception as e:
        print(f"❌ Failed to initialize storage service: {e}")
        return None
    
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
        print("❌ Need at least 2 datapoints with embeddings to test clustering")
        print("   Try ingesting more datapoints first:")
        print("   ./scripts/ingest_all_topics.sh")
        return None
    
    # Calculate similarity matrix for analysis
    print("🔍 Analyzing embedding similarities...")
    clustering_service = ClusteringService(storage_service)
    
    similarities = []
    for i, dp1 in enumerate(datapoints_with_embeddings):
        for j, dp2 in enumerate(datapoints_with_embeddings[i+1:], start=i+1):
            similarity = clustering_service.cosine_similarity(
                dp1['embedding'],
                dp2['embedding']
            )
            similarities.append(similarity)
    
    if similarities:
        sim_array = np.array(similarities)
        print(f"   Similarity range: {sim_array.min():.4f} - {sim_array.max():.4f}")
        print(f"   Mean similarity: {sim_array.mean():.4f}")
        print(f"   Median similarity: {np.median(sim_array):.4f}")
        print(f"   Std deviation: {sim_array.std():.4f}\n")
    
    # Test different parameter combinations
    print("🧪 Testing Parameter Combinations:")
    print("-" * 70)
    
    # Parameter ranges to test
    eps_values = [0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6]
    min_samples_values = [1, 2, 3, 4]
    
    results = []
    
    # Get unclustered datapoints (for testing, we'll use all datapoints but won't save)
    # Create deep copies to avoid modifying original data during testing
    import copy
    test_datapoints = [copy.deepcopy(dp) for dp in datapoints_with_embeddings]
    
    # Reset clustered flags for testing
    for dp in test_datapoints:
        dp['clustered'] = False
        if 'cluster_id' in dp:
            del dp['cluster_id']
    
    print(f"   Testing on {len(test_datapoints)} datapoints\n")
    
    # Create a temporary clustering service that won't update database
    class TestClusteringService(ClusteringService):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._test_mode = True
        
        def cluster_datapoints(self, datapoints, min_cluster_size=None):
            """Override to not update database during testing."""
            # Call parent but skip database updates
            result = super().cluster_datapoints(datapoints, min_cluster_size)
            # Don't actually update database in test mode
            return result
    
    for eps in eps_values:
        for min_samples in min_samples_values:
            try:
                # Use regular service but we'll create fresh copies each time
                test_dps = [copy.deepcopy(dp) for dp in test_datapoints]
                
                clustering_service = ClusteringService(
                    storage_service=storage_service,
                    eps=eps,
                    min_samples=min_samples
                )
                
                # Temporarily disable database updates by monkey-patching
                original_update = clustering_service.storage_service.update_cluster_id
                clustering_service.storage_service.update_cluster_id = lambda *args, **kwargs: None
                
                # Cluster the datapoints
                clusters = clustering_service.cluster_datapoints(test_dps)
                
                # Restore original method
                clustering_service.storage_service.update_cluster_id = original_update
                
                num_clusters = len(clusters)
                total_clustered = sum(len(c) for c in clusters.values())
                noise_count = len(test_dps) - total_clustered
                noise_percentage = (noise_count / len(test_dps) * 100) if test_dps else 0
                
                # Calculate cluster size statistics
                if clusters:
                    cluster_sizes = [len(c) for c in clusters.values()]
                    avg_size = np.mean(cluster_sizes)
                    min_size = min(cluster_sizes)
                    max_size = max(cluster_sizes)
                else:
                    avg_size = min_size = max_size = 0
                
                # Score this configuration
                score = calculate_score(
                    num_clusters=num_clusters,
                    total_clustered=total_clustered,
                    noise_percentage=noise_percentage,
                    avg_cluster_size=avg_size,
                    min_cluster_size=min_size,
                    total_datapoints=len(test_dps)
                )
                
                results.append({
                    'eps': eps,
                    'min_samples': min_samples,
                    'num_clusters': num_clusters,
                    'total_clustered': total_clustered,
                    'noise_count': noise_count,
                    'noise_percentage': noise_percentage,
                    'avg_cluster_size': avg_size,
                    'min_cluster_size': min_size,
                    'max_cluster_size': max_size,
                    'score': score
                })
                
                # Print progress for key combinations
                if eps in [0.3, 0.4, 0.5] and min_samples == 2:
                    status = "✅" if num_clusters > 0 else "❌"
                    print(f"   {status} eps={eps:.2f}, min_samples={min_samples}: "
                          f"{num_clusters} clusters, {total_clustered} clustered, "
                          f"{noise_percentage:.1f}% noise, score={score:.2f}")
                
            except Exception as e:
                print(f"   ❌ eps={eps:.2f}, min_samples={min_samples}: ERROR - {e}")
                continue
    
    print("\n" + "=" * 70)
    print("📊 Results Summary")
    print("=" * 70)
    
    if not results:
        print("❌ No successful clustering results")
        return None
    
    # Sort by score (higher is better)
    results.sort(key=lambda x: x['score'], reverse=True)
    
    # Show top 10 configurations
    print("\n🏆 Top 10 Parameter Configurations (by score):")
    print("-" * 70)
    print(f"{'Rank':<6} {'eps':<6} {'min_samples':<12} {'Clusters':<10} {'Clustered':<12} {'Noise%':<10} {'Avg Size':<10} {'Score':<8}")
    print("-" * 70)
    
    for i, result in enumerate(results[:10], 1):
        print(f"{i:<6} {result['eps']:<6.2f} {result['min_samples']:<12} "
              f"{result['num_clusters']:<10} {result['total_clustered']:<12} "
              f"{result['noise_percentage']:<10.1f} {result['avg_cluster_size']:<10.2f} "
              f"{result['score']:<8.2f}")
    
    # Recommendations
    print("\n" + "=" * 70)
    print("💡 Recommendations")
    print("=" * 70)
    
    # For misinformation detection, prefer min_samples >= 2 (more meaningful clusters)
    # Filter for configurations with min_samples >= 2 and reasonable cluster sizes
    meaningful_results = [
        r for r in results 
        if r['min_samples'] >= 2 
        and r['num_clusters'] > 0
        and r['avg_cluster_size'] >= 2
    ]
    
    if meaningful_results:
        best_meaningful = max(meaningful_results, key=lambda x: x['score'])
        best = best_meaningful
        print(f"\n✅ Recommended Configuration (for Misinformation Detection):")
        print(f"   eps = {best['eps']:.2f}")
        print(f"   min_samples = {best['min_samples']}")
        print(f"   Results: {best['num_clusters']} clusters, {best['total_clustered']} datapoints clustered")
        print(f"   Noise: {best['noise_percentage']:.1f}%")
        print(f"   Average cluster size: {best['avg_cluster_size']:.1f}")
        print(f"   Score: {best['score']:.2f}")
        print(f"\n   Why this configuration?")
        print(f"   - min_samples >= 2 ensures meaningful clusters (not single outliers)")
        print(f"   - Good balance between topic diversity and cluster quality")
        print(f"   - Suitable for pattern detection in misinformation analysis")
    else:
        best = results[0]
        print(f"\n✅ Best Overall Configuration:")
        print(f"   eps = {best['eps']:.2f}")
        print(f"   min_samples = {best['min_samples']}")
        print(f"   Results: {best['num_clusters']} clusters, {best['total_clustered']} datapoints clustered")
        print(f"   Noise: {best['noise_percentage']:.1f}%")
        print(f"   Average cluster size: {best['avg_cluster_size']:.1f}")
        print(f"   Score: {best['score']:.2f}")
    
    # Find configurations for specific goals
    print(f"\n🎯 Configuration for Specific Goals:")
    
    # Most clusters (topic diversity)
    most_clusters = max(results, key=lambda x: x['num_clusters'])
    if most_clusters['num_clusters'] > best['num_clusters']:
        print(f"\n   For Maximum Topic Diversity:")
        print(f"   eps = {most_clusters['eps']:.2f}, min_samples = {most_clusters['min_samples']}")
        print(f"   → {most_clusters['num_clusters']} clusters")
    
    # Least noise
    least_noise = min([r for r in results if r['num_clusters'] > 0], 
                     key=lambda x: x['noise_percentage'], default=None)
    if least_noise and least_noise['noise_percentage'] < best['noise_percentage']:
        print(f"\n   For Minimum Noise/Outliers:")
        print(f"   eps = {least_noise['eps']:.2f}, min_samples = {least_noise['min_samples']}")
        print(f"   → {least_noise['noise_percentage']:.1f}% noise")
    
    # Balanced (good clusters, reasonable noise)
    balanced = [r for r in results 
                if r['num_clusters'] >= 2 
                and r['noise_percentage'] < 30 
                and r['avg_cluster_size'] >= 2]
    if balanced:
        balanced_best = max(balanced, key=lambda x: x['score'])
        if balanced_best['eps'] != best['eps'] or balanced_best['min_samples'] != best['min_samples']:
            print(f"\n   For Balanced Clustering:")
            print(f"   eps = {balanced_best['eps']:.2f}, min_samples = {balanced_best['min_samples']}")
            print(f"   → {balanced_best['num_clusters']} clusters, {balanced_best['noise_percentage']:.1f}% noise")
    
    # Parameter sensitivity analysis
    print(f"\n📈 Parameter Sensitivity Analysis:")
    
    # eps sensitivity (with min_samples=2)
    eps_results = [r for r in results if r['min_samples'] == 2]
    if eps_results:
        print(f"\n   Effect of eps (with min_samples=2):")
        for r in sorted(eps_results, key=lambda x: x['eps']):
            marker = " ← Best" if r['eps'] == best['eps'] and r['min_samples'] == best['min_samples'] else ""
            print(f"   eps={r['eps']:.2f}: {r['num_clusters']} clusters, {r['total_clustered']} clustered{marker}")
    
    # min_samples sensitivity (with best eps)
    min_samples_results = [r for r in results if abs(r['eps'] - best['eps']) < 0.01]
    if min_samples_results:
        print(f"\n   Effect of min_samples (with eps={best['eps']:.2f}):")
        for r in sorted(min_samples_results, key=lambda x: x['min_samples']):
            marker = " ← Best" if r['min_samples'] == best['min_samples'] else ""
            print(f"   min_samples={r['min_samples']}: {r['num_clusters']} clusters, {r['total_clustered']} clustered{marker}")
    
    print(f"\n" + "=" * 70)
    print("✅ Testing Complete!")
    print("=" * 70)
    
    return best

def calculate_score(
    num_clusters: int,
    total_clustered: int,
    noise_percentage: float,
    avg_cluster_size: float,
    min_cluster_size: int,
    total_datapoints: int
) -> float:
    """
    Calculate a score for clustering quality.
    
    Higher score = better configuration
    Factors:
    - More clusters (topic diversity) = better
    - More datapoints clustered = better
    - Less noise = better
    - Reasonable cluster sizes (2-10) = better
    - Penalize too many tiny clusters or one huge cluster
    """
    if num_clusters == 0:
        return 0.0
    
    # Base score from number of clusters (encourage diversity)
    cluster_score = min(num_clusters / 10.0, 1.0) * 30
    
    # Coverage score (how many datapoints are clustered)
    coverage_score = (total_clustered / total_datapoints) * 30
    
    # Noise penalty (less noise is better)
    noise_score = max(0, (100 - noise_percentage) / 100) * 20
    
    # Cluster size score (prefer 2-10 datapoints per cluster)
    if 2 <= avg_cluster_size <= 10:
        size_score = 20
    elif avg_cluster_size < 2:
        size_score = 10 * (avg_cluster_size / 2)
    else:
        # Penalize very large clusters (might be too loose)
        size_score = max(0, 20 * (1 - (avg_cluster_size - 10) / 20))
    
    # Penalty for too many tiny clusters
    if min_cluster_size < 2:
        size_score *= 0.8
    
    total_score = cluster_score + coverage_score + noise_score + size_score
    
    return total_score

if __name__ == "__main__":
    best_config = test_parameter_combinations()
    
    if best_config:
        print(f"\n🎯 Recommended Configuration:")
        print(f"   ClusteringService(")
        print(f"       storage_service=storage_service,")
        print(f"       eps={best_config['eps']:.2f},")
        print(f"       min_samples={best_config['min_samples']}")
        print(f"   )")
        print(f"\n   Or via API:")
        print(f"   curl -X POST \"http://localhost:2024/clustering/cluster?eps={best_config['eps']:.2f}&min_cluster_size={best_config['min_samples']}\"")
    
    sys.exit(0 if best_config else 1)
