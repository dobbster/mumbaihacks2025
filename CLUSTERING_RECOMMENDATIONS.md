# Clustering Recommendations: DBSCAN, Embeddings & Vector DB

## DBSCAN for Topic Clustering

### Why DBSCAN is Excellent for Topic Clustering

✅ **Automatic Cluster Detection**: No need to specify number of clusters upfront  
✅ **Noise Handling**: Identifies outliers (datapoints that don't fit any cluster)  
✅ **Variable Density**: Finds clusters of different sizes and densities  
✅ **High-Dimensional**: Works well with embedding vectors (typically 1536 dimensions)  
✅ **Robust**: Less sensitive to initialization than K-means  

### DBSCAN Parameters Explained

```python
DBSCAN(eps=0.3, min_samples=2, metric='cosine')
```

**`eps` (epsilon)**: Maximum distance between samples in the same neighborhood
- **Range**: 0.0 - 1.0 (for cosine similarity)
- **Lower (0.2-0.3)**: Stricter clustering → fewer, tighter clusters
- **Higher (0.4-0.5)**: Looser clustering → more, larger clusters
- **Recommended for topics**: 0.25-0.35

**`min_samples`**: Minimum samples in a neighborhood to form a cluster
- **Lower (2-3)**: More small clusters, more noise
- **Higher (5-10)**: Only large clusters, less noise
- **Recommended for topics**: 3-5

**`metric`**: Distance metric
- **'cosine'**: Best for embeddings (normalized vectors)
- **'euclidean'**: For non-normalized vectors
- **Recommended**: 'cosine' for text embeddings

### Tuning DBSCAN for Your Use Case

**For Misinformation Detection:**
```python
# Stricter clustering to catch similar narratives
ClusteringService(eps=0.25, min_samples=3)
```

**For General Topic Clustering:**
```python
# Balanced approach
ClusteringService(eps=0.3, min_samples=2)
```

**For Broad Topic Discovery:**
```python
# Looser clustering to find related topics
ClusteringService(eps=0.4, min_samples=2)
```

## Embedding Model Recommendations

### Best Models for Topic Clustering

#### 1. **Together AI BAAI/bge-base-en-v1.5** (Recommended for Hackathon)
- **Dimensions**: 768
- **Cost**: Very low (free tier available)
- **Quality**: Excellent for semantic similarity
- **Speed**: Fast
- **Use Case**: General purpose, good balance
- **No OpenAI API Key Required**: Uses Together AI

```python
# Configured via environment variables
TOGETHER_API_KEY=your_key
TOGETHER_EMBEDDING_MODEL=BAAI/bge-base-en-v1.5
```

#### 2. **Together AI BAAI/bge-large-en-v1.5**
- **Dimensions**: 1024
- **Cost**: Low (free tier available)
- **Quality**: Best semantic understanding
- **Speed**: Moderate
- **Use Case**: When accuracy is critical

#### 3. **Together AI BAAI/bge-small-en-v1.5**
- **Dimensions**: 384
- **Cost**: Very low (free tier available)
- **Quality**: Good
- **Speed**: Very fast
- **Use Case**: High-volume, cost-sensitive applications

#### 4. **Sentence Transformers (Open Source)**
- **Models**: `all-MiniLM-L6-v2`, `all-mpnet-base-v2`
- **Dimensions**: 384-768
- **Cost**: Free (runs locally)
- **Quality**: Good for general use
- **Use Case**: When you want to avoid API costs

```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-mpnet-base-v2')
```

### Model Comparison for Topic Clustering

| Model | Dimensions | Cost | Quality | Speed | Best For |
|-------|-----------|------|---------|-------|----------|
| BAAI/bge-base-en-v1.5 | 768 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | **Hackathon, Production** |
| BAAI/bge-large-en-v1.5 | 1024 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | High accuracy needs |
| BAAI/bge-small-en-v1.5 | 384 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | High volume, speed |
| all-mpnet-base-v2 | 768 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Cost-sensitive, local |

### Recommendation for Your Hackathon

**Use `BAAI/bge-base-en-v1.5` (Together AI)**:
- Best cost/quality ratio (free tier available!)
- Fast enough for real-time processing
- Good semantic understanding for topic clustering
- Works well with DBSCAN
- No OpenAI API key required

## Vector Database Recommendations

### Option 1: MongoDB with Vector Search (Recommended for Hackathon)

**Pros:**
- ✅ You already have MongoDB
- ✅ No additional service to set up
- ✅ Stores metadata alongside vectors
- ✅ Good for hackathon timeline

**Cons:**
- ⚠️ Requires MongoDB Atlas (cloud) for native vector search
- ⚠️ Local MongoDB needs manual similarity calculation (what we implemented)

**Implementation:**
```python
# Current implementation (works with local MongoDB)
# Stores embeddings as arrays, calculates similarity in Python
# Good enough for hackathon scale (hundreds to thousands of datapoints)
```

**For Production (MongoDB Atlas Vector Search):**
```python
# MongoDB Atlas has native vector search
# Create vector search index:
{
  "fields": [{
    "type": "vector",
    "path": "embedding",
    "numDimensions": 1536,
    "similarity": "cosine"
  }]
}
```

### Option 2: Dedicated Vector Databases

#### Pinecone
- **Pros**: Managed, easy to use, great performance
- **Cons**: Additional service, costs money
- **Best For**: Production systems with high volume

#### Weaviate
- **Pros**: Open source, self-hosted option, good features
- **Cons**: More setup complexity
- **Best For**: When you need advanced features

#### Qdrant
- **Pros**: Open source, fast, good performance
- **Cons**: Requires deployment
- **Best For**: Self-hosted solutions

### Recommendation for Hackathon

**Use MongoDB (current implementation)**:
1. ✅ Already set up
2. ✅ No additional services
3. ✅ Sufficient for hackathon scale
4. ✅ Can upgrade to Atlas Vector Search later

**When to Consider Dedicated Vector DB:**
- Processing millions of datapoints
- Need sub-millisecond search latency
- Complex filtering requirements
- Production deployment

## Complete Setup Example

### 1. Embedding Model Configuration

```python
# app/dependencies.py
from langchain_openai import OpenAIEmbeddings

def get_embeddings_model() -> OpenAIEmbeddings:
    return OpenAIEmbeddings(
        base_url="https://api.together.xyz/v1",
        api_key=os.getenv("TOGETHER_API_KEY"),
        model=os.getenv("TOGETHER_EMBEDDING_MODEL", "BAAI/bge-base-en-v1.5")
    )
```

### 2. DBSCAN Clustering Configuration

```python
# app/core/clustering.py
clustering_service = ClusteringService(
    storage_service=storage_service,
    eps=0.3,           # Balanced clustering
    min_samples=3,     # Require at least 3 similar items
    metric='cosine'    # Best for embeddings
)
```

### 3. Usage

```python
# Cluster recent datapoints
clusters = clustering_service.cluster_recent_datapoints(
    hours=24,
    use_dbscan=True  # Use DBSCAN algorithm
)

# Get statistics
stats = clustering_service.get_cluster_statistics(clusters)
print(f"Found {stats['total_clusters']} clusters")
print(f"Average cluster size: {stats['avg_cluster_size']:.1f}")
```

## Performance Considerations

### DBSCAN Performance
- **Time Complexity**: O(n log n) with spatial indexing, O(n²) without
- **For 1000 datapoints**: ~1-5 seconds
- **For 10,000 datapoints**: ~30-60 seconds
- **Optimization**: Use `n_jobs=-1` for parallel processing

### Embedding Generation
- **text-embedding-3-small**: ~100-200ms per batch of 100 texts
- **Batch processing**: Use `embed_documents()` for efficiency
- **Caching**: Consider caching embeddings for duplicate content

### MongoDB Queries
- **Indexes**: Ensure indexes on `published_at`, `clustered`
- **Limit queries**: Use `limit` parameter to avoid loading too much data
- **Pagination**: For large datasets, process in batches

## Tuning Guide

### If Clusters Are Too Small
- **Increase `eps`**: Try 0.35-0.4
- **Decrease `min_samples`**: Try 2

### If Too Many Noise Points
- **Decrease `eps`**: Try 0.25-0.3
- **Increase `min_samples`**: Try 4-5

### If Clusters Are Too Large
- **Decrease `eps`**: Try 0.2-0.25
- **Keep `min_samples`**: 2-3

### If Clustering Is Too Slow
- **Reduce dataset size**: Filter by time window
- **Use batch processing**: Process in chunks
- **Consider simpler method**: Use `cluster_datapoints_simple()` for comparison

## Summary

**For Your Hackathon:**
1. ✅ **DBSCAN**: Use the updated clustering service
2. ✅ **Embedding**: `text-embedding-3-small` (best cost/quality)
3. ✅ **Vector DB**: MongoDB (current implementation, sufficient for hackathon)

**For Production:**
1. Consider MongoDB Atlas Vector Search or dedicated vector DB
2. Use `text-embedding-3-large` if accuracy is critical
3. Tune DBSCAN parameters based on your data

The implementation is ready to use DBSCAN with your current MongoDB setup!

