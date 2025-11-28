# Topic Clustering & Representation Guide

## Overview

Topic clustering groups semantically similar news articles and datapoints together, enabling:
1. **Pattern Detection**: Identify emerging misinformation patterns within clusters
2. **Temporal Analysis**: Track how misinformation evolves within topic clusters
3. **Verification**: Cross-reference claims within the same cluster
4. **Public Updates**: Generate contextual summaries of related information

## How to Cluster Datapoints

### Step 1: Ensure You Have Data

First, make sure you have ingested datapoints with embeddings:

```bash
# Ingest sample data (6 datapoints)
curl -X POST http://localhost:2024/ingestion/datapoints \
  -H "Content-Type: application/json" \
  -d @examples/datapoints_example.json

# Or ingest all topic-specific data (20 datapoints across 5 topics)
curl -X POST http://localhost:2024/ingestion/datapoints \
  -H "Content-Type: application/json" \
  -d @examples/datapoints_all_topics.json

# Or use the ingestion script
./scripts/ingest_all_topics.sh
```

### Step 2: Cluster Datapoints

#### Option A: Via API (Recommended)

**Cluster with recommended parameters (eps=0.30, min_samples=2):**
```bash
# For recent data (last 7 days)
curl -X POST "http://localhost:2024/clustering/cluster?eps=0.30&min_cluster_size=2&hours=168"

# For older data (last year) - use larger hours window
curl -X POST "http://localhost:2024/clustering/cluster?eps=0.30&min_cluster_size=2&hours=8760&force_recluster=true"
```

**Response:**
```json
{
  "status": "success",
  "clusters_found": 3,
  "total_datapoints_clustered": 26,
  "statistics": {
    "total_clusters": 3,
    "total_datapoints": 26,
    "avg_cluster_size": 8.67,
    "largest_cluster": 16,
    "smallest_cluster": 5,
    "cluster_size_distribution": {
      "small": 0,
      "medium": 3,
      "large": 0
    }
  },
  "clusters": {
    "cluster_0": [
      {"id": "vaccine_001", "title": "Study finds no link..."},
      ...
    ],
    "cluster_1": [...],
    "cluster_2": [...]
  }
}
```

#### Option B: Via Python Script

```bash
# Run clustering test script
uv run python scripts/test_clustering.py
```

This will:
- Check database status
- Run DBSCAN clustering on unclustered datapoints
- Show cluster statistics
- Display sample clusters with titles

**Example Output:**
```
Testing Topic Clustering
============================================================
✅ Storage service initialized
✅ Clustering service initialized
   Configuration: eps=0.30, min_samples=2

📊 Database Status:
   Total datapoints: 26
   Datapoints with embeddings: 26
   Unclustered datapoints: 20

🔍 Running DBSCAN clustering on 20 datapoints...

✅ Clustering successful! Found 3 clusters.

📊 Cluster Statistics:
   total_clusters: 3
   total_datapoints: 26
   avg_cluster_size: 8.67
   largest_cluster: 16
   smallest_cluster: 5

Detailed Clusters:
--- cluster_0 (16 datapoints) ---
  - ID: vaccine_001, Title: Study finds no link between vaccines...
  - ID: misinfo_001, Title: Social media claims about vaccine dangers...
  ...
```

### Step 3: Test Clustering Parameters

**Find optimal parameters for your data:**
```bash
# Run comprehensive parameter testing
uv run python scripts/test_clustering_params.py
```

This script:
- Tests 36 parameter combinations (9 eps values × 4 min_samples values)
- Analyzes embedding similarities
- Scores each configuration
- Recommends optimal parameters
- Shows parameter sensitivity analysis

**Example Output:**
```
Clustering Parameter Testing & Recommendations
======================================================================
✅ Storage service initialized

📊 Database Status:
   Total datapoints: 26
   Datapoints with valid embeddings: 26

🔍 Analyzing embedding similarities...
   Similarity range: 0.3989 - 1.0000
   Mean similarity: 0.5898
   Median similarity: 0.5752

🧪 Testing Parameter Combinations:
   ✅ eps=0.30, min_samples=2: 3 clusters, 26 clustered, 0.0% noise, score=79.00

🏆 Top 10 Parameter Configurations (by score):
----------------------------------------------------------------------
Rank   eps    min_samples  Clusters   Clustered    Noise%     Avg Size   Score   
----------------------------------------------------------------------
1      0.30   2            3          26           0.0        8.67       79.00   

✅ Recommended Configuration (for Misinformation Detection):
   eps = 0.30
   min_samples = 2
   Results: 3 clusters, 26 datapoints clustered
   Noise: 0.0%
   Average cluster size: 8.7
   Score: 79.00
```

### Step 4: View Cluster Statistics

#### Option A: Via API

**Get cluster statistics:**
```bash
# Get statistics for recent data (last 7 days)
curl "http://localhost:2024/clustering/stats?hours=168"

# Get statistics for older data (last year)
curl "http://localhost:2024/clustering/stats?hours=8760"
```

**Response:**
```json
{
  "status": "success",
  "total_clustered_datapoints_in_db": 26,
  "statistics": {
    "total_clusters": 3,
    "total_datapoints": 26,
    "avg_cluster_size": 8.67,
    "largest_cluster": 16,
    "smallest_cluster": 5,
    "cluster_size_distribution": {
      "small": 0,
      "medium": 3,
      "large": 0
    }
  }
}
```

#### Option B: Via MongoDB

View clusters directly in MongoDB (using VSCode MongoDB extension or MongoDB Compass):

```javascript
// Count clusters
db.datapoints.distinct("cluster_id")

// View datapoints by cluster
db.datapoints.find({cluster_id: "cluster_0"})

// Get cluster statistics
db.datapoints.aggregate([
  { $match: { clustered: true } },
  { $group: {
      _id: "$cluster_id",
      count: { $sum: 1 },
      titles: { $push: "$title" }
    }
  },
  { $sort: { count: -1 } }
])
```

#### Option C: Via Python Script

```python
from app.dependencies import get_storage_service
from app.core.clustering import ClusteringService

storage = get_storage_service()
clustering = ClusteringService(storage, eps=0.30, min_samples=2)

# Get recent datapoints
recent = storage.get_recent_datapoints(hours=8760)  # Last year
clustered = [dp for dp in recent if dp.get('clustered')]

# Group by cluster
clusters_map = {}
for dp in clustered:
    cid = dp.get('cluster_id')
    if cid:
        if cid not in clusters_map:
            clusters_map[cid] = []
        clusters_map[cid].append(dp)

# Get statistics
stats = clustering.get_cluster_statistics(clusters_map)
print(f"Total clusters: {stats['total_clusters']}")
print(f"Average cluster size: {stats['avg_cluster_size']}")
print(f"Largest cluster: {stats['largest_cluster']}")
print(f"Smallest cluster: {stats['smallest_cluster']}")
```

### Step 5: Analyze Cluster Quality

**Check if clusters are meaningful:**

1. **Cluster Size Distribution:**
   - Small clusters (2-4): May be outliers or very specific topics
   - Medium clusters (5-10): Good for topic analysis
   - Large clusters (10+): May need tighter `eps` to split

2. **Cluster Coherence:**
   - Review titles within each cluster
   - They should discuss similar topics
   - If too diverse, decrease `eps`

3. **Coverage:**
   - High coverage (90%+): Good, most data is clustered
   - Low coverage (<50%): Increase `eps` or decrease `min_samples`

4. **Noise Percentage:**
   - Low noise (<10%): Good clustering
   - High noise (>30%): Decrease `eps` to be more strict

## Understanding Clustering Parameters

### Recommended Parameters (Based on Testing)

**For Misinformation Detection:**
```python
eps = 0.30
min_samples = 2
```

These parameters were optimized through comprehensive testing on 26 datapoints across 5 topics:
- ✅ 3 clusters found
- ✅ 26 datapoints clustered (100% coverage)
- ✅ 0.0% noise/outliers
- ✅ Average cluster size: 8.7 datapoints

### DBSCAN Parameters

- **eps** (0.0-1.0): Maximum distance between samples in same cluster
  - **0.20-0.25**: Very strict, many small clusters, some noise
  - **0.30** (Recommended): Balanced, good topic diversity
  - **0.35-0.40**: Looser, fewer but larger clusters
  - **0.45+**: Too loose, merges distinct topics
  - **Default**: 0.30 (optimized for misinformation detection)

- **min_samples**: Minimum datapoints to form a cluster
  - **1**: Allows single-datapoint clusters (not recommended)
  - **2** (Recommended): Ensures meaningful clusters
  - **3-4**: More strict, only significant clusters
  - **Default**: 2

### Parameter Tuning Guide

**Use `test_clustering_params.py` to find optimal parameters:**
```bash
uv run python scripts/test_clustering_params.py
```

This will test all combinations and recommend the best for your data.

### Tuning Tips

1. **Too many small clusters?** → Increase `eps` or `min_samples`
2. **Too few clusters?** → Decrease `eps` or `min_samples`
3. **Many noise points?** → Decrease `eps` to be more strict
4. **Clusters too large/loose?** → Decrease `eps`

## Cluster Representation

### What Clusters Represent

Each cluster groups datapoints that are semantically similar, meaning they discuss:
- The same topic/event
- Related claims or narratives
- Similar misinformation patterns

### Cluster Metadata

Each cluster contains:
- **Cluster ID**: Unique identifier (e.g., `cluster_0`, `cluster_1`)
- **Size**: Number of datapoints in cluster
- **Sources**: Which news sources contributed
- **Topics**: Categories/topics covered
- **Temporal Range**: Earliest to latest publication dates

### Example Cluster

```json
{
  "cluster_id": "cluster_0",
  "size": 5,
  "sources": ["BBC News", "Reuters Health", "Tavily Search"],
  "topics": ["health", "vaccines", "misinformation"],
  "datapoints": [
    {
      "title": "Study finds no link between vaccines...",
      "source": "Reuters Health",
      "published_at": "2025-01-15T09:15:00Z"
    },
    // ... more related articles
  ]
}
```

## How Clustering Fits into Misinformation Detection

### Current Pipeline

```
1. Ingestion
   ↓
2. Vectorization (embeddings)
   ↓
3. Storage in MongoDB
   ↓
4. Clustering (groups similar topics) ← YOU ARE HERE
   ↓
5. Pattern Detection (analyze clusters)
   ↓
6. Classification (misinformation vs. fact)
   ↓
7. Verification (cross-reference claims)
   ↓
8. Public Updates (contextual summaries)
```

### What's Next: Pattern Detection

After clustering, you should:

1. **Analyze Cluster Growth**: Track which clusters are growing rapidly
   - Rapid growth = potential misinformation spread
   - Use temporal analysis on cluster sizes

2. **Compare Sources**: Within each cluster, compare:
   - Credible sources vs. questionable sources
   - Official statements vs. social media claims
   - Fact-checked vs. unverified

3. **Detect Contradictions**: Within clusters, identify:
   - Conflicting claims about the same topic
   - Claims that contradict verified facts
   - Evolving narratives (how story changes)

4. **Temporal Patterns**: Track:
   - When misinformation first appeared
   - How it spread across sources
   - Evolution of the narrative

## API Endpoints

### POST `/clustering/cluster`

Cluster recent unclustered datapoints using DBSCAN algorithm.

**Parameters:**
- `hours` (int): Look back this many hours (default: 168 = 7 days)
  - For recent data: `168` (7 days)
  - For older data: `8760` (365 days) or `87600` (10 years)
- `min_cluster_size` (int): Minimum cluster size (default: 2)
- `eps` (float): DBSCAN eps parameter (default: 0.30, recommended: 0.30)
- `use_dbscan` (bool): Use DBSCAN or simple similarity (default: true)
- `force_recluster` (bool): Re-cluster even already-clustered datapoints (default: false)

**Example Request:**
```bash
curl -X POST "http://localhost:2024/clustering/cluster?eps=0.30&min_cluster_size=2&hours=8760&force_recluster=true"
```

**Response:**
```json
{
  "status": "success",
  "clusters_found": 3,
  "total_datapoints_clustered": 26,
  "statistics": {
    "total_clusters": 3,
    "total_datapoints": 26,
    "avg_cluster_size": 8.67,
    "largest_cluster": 16,
    "smallest_cluster": 5,
    "cluster_size_distribution": {
      "small": 0,
      "medium": 3,
      "large": 0
    }
  },
  "clusters": {
    "cluster_0": [
      {
        "id": "vaccine_001",
        "title": "Study finds no link between vaccines and serious side effects",
        "source_name": "Reuters Health",
        "source_type": "rss",
        "published_at": "2025-01-15 09:15:00",
        "categories": ["health", "vaccines", "research"]
      },
      ...
    ],
    "cluster_1": [...],
    "cluster_2": [...]
  }
}
```

**Response Fields:**
- `clusters_found`: Number of clusters discovered
- `total_datapoints_clustered`: Total datapoints assigned to clusters
- `statistics`: Detailed cluster statistics
  - `total_clusters`: Number of clusters
  - `avg_cluster_size`: Average number of datapoints per cluster
  - `largest_cluster`: Size of largest cluster
  - `smallest_cluster`: Size of smallest cluster
  - `cluster_size_distribution`: Distribution by size (small: 2-4, medium: 5-10, large: 10+)
- `clusters`: Dictionary mapping cluster_id to list of datapoints

### GET `/clustering/stats`

Get statistics about existing clusters in the database.

**Parameters:**
- `hours` (int): Look back this many hours (default: 168 = 7 days)

**Example Request:**
```bash
curl "http://localhost:2024/clustering/stats?hours=8760"
```

**Response:**
```json
{
  "status": "success",
  "total_clustered_datapoints_in_db": 26,
  "statistics": {
    "total_clusters": 3,
    "total_datapoints": 26,
    "avg_cluster_size": 8.67,
    "largest_cluster": 16,
    "smallest_cluster": 5,
    "cluster_size_distribution": {
      "small": 0,
      "medium": 3,
      "large": 0
    }
  }
}
```

## Complete Testing Workflow

### 1. Ingest Diverse Data

```bash
# Ingest all topic-specific datapoints
./scripts/ingest_all_topics.sh

# Or manually ingest
curl -X POST http://localhost:2024/ingestion/datapoints \
  -H "Content-Type: application/json" \
  -d @examples/datapoints_all_topics.json
```

### 2. Test Clustering Parameters (Optional but Recommended)

```bash
# Find optimal parameters for your data
uv run python scripts/test_clustering_params.py
```

This will:
- Test 36 parameter combinations
- Analyze embedding similarities
- Recommend optimal `eps` and `min_samples`
- Show parameter sensitivity analysis

### 3. Run Clustering

```bash
# Use recommended parameters
curl -X POST "http://localhost:2024/clustering/cluster?eps=0.30&min_cluster_size=2&hours=8760&force_recluster=true"
```

Or use the test script:
```bash
uv run python scripts/test_clustering.py
```

### 4. Review Cluster Statistics

```bash
# Get statistics via API
curl "http://localhost:2024/clustering/stats?hours=8760"

# Or view in MongoDB
# Use VSCode MongoDB extension or MongoDB Compass
```

### 5. Analyze Cluster Quality

Check:
- ✅ Cluster sizes are reasonable (5-10 datapoints average)
- ✅ Clusters are coherent (similar topics within each cluster)
- ✅ Coverage is high (>90% datapoints clustered)
- ✅ Noise is low (<10%)

### 6. Adjust Parameters if Needed

If clusters are not optimal:
- **Too many small clusters?** → Increase `eps` (e.g., 0.35-0.40)
- **Too few clusters?** → Decrease `eps` (e.g., 0.25)
- **Many noise points?** → Decrease `eps` (e.g., 0.25-0.30)
- **Clusters too large/loose?** → Decrease `eps` (e.g., 0.25-0.30)

### 7. Re-cluster and Compare

```bash
# Re-cluster with adjusted parameters
curl -X POST "http://localhost:2024/clustering/cluster?eps=0.25&min_cluster_size=2&hours=8760&force_recluster=true"

# Compare statistics
curl "http://localhost:2024/clustering/stats?hours=8760"
```

### 8. Analyze Clusters for Patterns

Once clustering is optimal:
- Review cluster contents (titles, sources, categories)
- Identify emerging patterns within clusters
- Track cluster growth over time
- Compare sources within clusters for contradictions

## Next Steps for Misinformation Detection

After clustering works, implement:

1. **Pattern Detection Node** (LangGraph):
   - Query clusters by growth rate
   - Identify rapidly growing clusters
   - Flag clusters with conflicting sources

2. **Classification Node** (LangGraph):
   - For each cluster, classify misinformation likelihood
   - Use LLM to analyze cluster content
   - Consider source credibility within cluster

3. **Verification Node** (LangGraph):
   - Cross-reference claims within clusters
   - Check against fact-checking databases
   - Identify contradictions

4. **Public Update Node** (LangGraph):
   - Generate summaries of cluster topics
   - Explain why information is flagged
   - Provide context and verified facts

## Troubleshooting

### No Clusters Found

**Symptoms:** API returns `clusters_found: 0`

**Solutions:**
1. **Check data availability:**
   ```bash
   # Check if you have datapoints
   curl "http://localhost:2024/clustering/stats?hours=8760"
   ```

2. **Check embeddings:**
   ```python
   from app.dependencies import get_storage_service
   storage = get_storage_service()
   dps_with_embeddings = storage.datapoints_collection.count_documents({
       "embedding": {"$exists": True, "$ne": []}
   })
   print(f"Datapoints with embeddings: {dps_with_embeddings}")
   ```

3. **Try different parameters:**
   ```bash
   # More lenient clustering
   curl -X POST "http://localhost:2024/clustering/cluster?eps=0.40&min_cluster_size=2&hours=8760&force_recluster=true"
   
   # Or use diagnostic script
   uv run python scripts/diagnose_clustering.py
   ```

4. **Check time window:**
   - If datapoints are old, use larger `hours` parameter (e.g., 8760 for 1 year)

### Too Many Small Clusters

**Symptoms:** Many clusters with 2-3 datapoints each

**Solutions:**
- **Increase `eps`** (e.g., 0.35-0.40):
  ```bash
  curl -X POST "http://localhost:2024/clustering/cluster?eps=0.35&min_cluster_size=2&hours=8760&force_recluster=true"
  ```
- **Increase `min_samples`** (e.g., 3-4):
  ```bash
  curl -X POST "http://localhost:2024/clustering/cluster?eps=0.30&min_cluster_size=3&hours=8760&force_recluster=true"
  ```

### Clusters Too Large/Loose

**Symptoms:** Few clusters (1-2) with many datapoints, unrelated topics merged

**Solutions:**
- **Decrease `eps`** (e.g., 0.25-0.30):
  ```bash
  curl -X POST "http://localhost:2024/clustering/cluster?eps=0.25&min_cluster_size=2&hours=8760&force_recluster=true"
  ```
- **Check embeddings:** Verify embeddings are working correctly
- **Run parameter testing:**
  ```bash
  uv run python scripts/test_clustering_params.py
  ```

### High Noise Percentage

**Symptoms:** Many datapoints not assigned to any cluster (noise)

**Solutions:**
- **Decrease `eps`** to be more strict (e.g., 0.25-0.30)
- **Decrease `min_samples`** (e.g., 2)
- **Check similarity:** Run diagnostic to see if datapoints are too dissimilar
  ```bash
  uv run python scripts/diagnose_clustering.py
  ```

### Clustering Takes Too Long

**Symptoms:** API request times out or takes >30 seconds

**Solutions:**
- **Normal:** DBSCAN is O(n log n) - acceptable for <10k datapoints
- **Optimize:** Use `min_samples=2` for faster clustering
- **Batch processing:** Cluster in smaller time windows:
  ```bash
  # Cluster last 7 days
  curl -X POST "http://localhost:2024/clustering/cluster?eps=0.30&min_cluster_size=2&hours=168"
  ```

### Datapoints Not Clustered (Already Clustered Flag)

**Symptoms:** API returns 0 clusters but you know there's unclustered data

**Solutions:**
- **Use `force_recluster=true`:**
  ```bash
  curl -X POST "http://localhost:2024/clustering/cluster?eps=0.30&min_cluster_size=2&hours=8760&force_recluster=true"
  ```
- **Reset clustering status in MongoDB:**
  ```python
  from app.dependencies import get_storage_service
  storage = get_storage_service()
  storage.datapoints_collection.update_many(
      {},
      {"$set": {"clustered": False, "cluster_id": None}}
  )
  ```

### Old Data Not Included

**Symptoms:** Clustering only finds recent datapoints, missing older ones

**Solutions:**
- **Increase `hours` parameter:**
  ```bash
  # Last year
  curl -X POST "http://localhost:2024/clustering/cluster?eps=0.30&min_cluster_size=2&hours=8760"
  
  # Last 10 years
  curl -X POST "http://localhost:2024/clustering/cluster?eps=0.30&min_cluster_size=2&hours=87600"
  ```

