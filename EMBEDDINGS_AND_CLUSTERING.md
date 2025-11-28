# Embeddings and Topic Clustering

## ✅ Yes, Topic Clustering Uses Embeddings!

Your topic clustering system **already uses embeddings** and is fully configured. Here's how it works:

## How Embeddings Are Used in Clustering

### 1. **Embedding Generation (During Ingestion)**

When datapoints are ingested, embeddings are automatically generated:

```
Ingestion Pipeline:
┌─────────────────┐
│  Raw Datapoint  │
│  (title +       │
│   content)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Vectorization   │
│ Service         │
│ (Together AI)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Embedding      │
│  Vector (768D)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  MongoDB        │
│  (stored with   │
│   datapoint)    │
└─────────────────┘
```

**Code Location**: `app/core/ingestion.py`
- Line 96: `embedding = self.vectorization_service.generate_embedding(text_for_embedding)`
- Embeddings are stored in MongoDB with each datapoint

### 2. **Clustering Uses Stored Embeddings**

When clustering runs, it:
1. Retrieves datapoints from MongoDB
2. Extracts the stored embeddings
3. Uses DBSCAN algorithm on the embedding vectors
4. Groups similar embeddings (which represent similar topics)

**Code Location**: `app/core/clustering.py`
- Lines 122-146: Extracts embeddings from datapoints
- Line 146: Converts to numpy array: `embeddings_array = np.array(embeddings)`
- Line 164: Runs DBSCAN: `cluster_labels = dbscan.fit_predict(embeddings_array)`

## Current Embedding Model Configuration

### **Model**: `BAAI/bge-base-en-v1.5` (Together AI)

**Specifications:**
- **Provider**: Together AI
- **Dimensions**: 768
- **Quality**: High-quality semantic embeddings
- **Language**: English
- **Integration**: Via `langchain-together` package

**Configuration Location**: `app/dependencies.py`
```python
@lru_cache()
def get_embeddings_model() -> TogetherEmbeddings:
    together_api_key = os.getenv("TOGETHER_API_KEY")
    together_model = os.getenv("TOGETHER_EMBEDDING_MODEL", "BAAI/bge-base-en-v1.5")
    
    return TogetherEmbeddings(
        model=together_model,
        together_api_key=together_api_key
    )
```

## Why Embeddings Are Essential for Clustering

### Without Embeddings (Not Recommended):
- Would need to use simple text matching (keywords, exact phrases)
- Cannot capture semantic similarity
- "virus variant" and "new strain" wouldn't be recognized as similar
- Poor clustering quality

### With Embeddings (Current Implementation):
- ✅ Captures semantic meaning
- ✅ "virus variant" and "new strain" are recognized as similar
- ✅ Groups related topics even with different wording
- ✅ Works across languages (with multilingual models)
- ✅ Handles synonyms and related concepts

## How DBSCAN Uses Embeddings

DBSCAN (Density-Based Spatial Clustering of Applications with Noise) works on embedding vectors:

1. **Distance Calculation**: Uses cosine similarity between embedding vectors
   - Similar topics → similar embeddings → small distance
   - Different topics → different embeddings → large distance

2. **Clustering**: Groups embeddings that are close together
   - `eps` parameter: Maximum distance between embeddings in same cluster
   - `min_samples`: Minimum embeddings needed to form a cluster

3. **Example**:
   ```
   Embedding Space (simplified 2D view):
   
   [Virus articles]  ●●●●  ← Cluster 1 (close embeddings)
   
   [Vaccine articles]  ●●●●  ← Cluster 2 (close embeddings)
   
   [Economy articles]  ●●●●  ← Cluster 3 (close embeddings)
   
   [Random article]  ●  ← Noise (far from all clusters)
   ```

## Verification: Check if Embeddings Are Working

### 1. Check During Ingestion

```bash
# Ingest data and check response
curl -X POST http://localhost:2024/ingestion/datapoints \
  -H "Content-Type: application/json" \
  -d @examples/raw_data.json

# Response should show "stored" count > 0
```

### 2. Verify in MongoDB

```python
from app.dependencies import get_storage_service

storage = get_storage_service()
datapoint = storage.datapoints_collection.find_one({})

if datapoint and datapoint.get('embedding'):
    print(f"✅ Embedding found: {len(datapoint['embedding'])} dimensions")
    print(f"   Model: {datapoint.get('embedding_model')}")
else:
    print("❌ No embedding found")
```

### 3. Check Clustering Uses Embeddings

```python
from app.dependencies import get_storage_service, get_clustering_service

storage = get_storage_service()
clustering = get_clustering_service()

# Get datapoints
recent = storage.get_recent_datapoints(hours=8760)
datapoints_with_embeddings = [dp for dp in recent if dp.get('embedding')]

print(f"Datapoints with embeddings: {len(datapoints_with_embeddings)}")

# Clustering will only work on datapoints with embeddings
clusters = clustering.cluster_datapoints(datapoints_with_embeddings)
print(f"Clusters found: {len(clusters)}")
```

## Alternative Embedding Models (Optional)

If you want to experiment with different models, you can change the `TOGETHER_EMBEDDING_MODEL` environment variable:

### Available Together AI Models:

1. **BAAI/bge-base-en-v1.5** (Current, Recommended)
   - 768 dimensions
   - Good balance of quality and speed
   - Best for general topic clustering

2. **BAAI/bge-large-en-v1.5**
   - 1024 dimensions
   - Higher quality, slower
   - Use for more nuanced clustering

3. **BAAI/bge-small-en-v1.5**
   - 384 dimensions
   - Faster, lower quality
   - Use for speed-critical applications

4. **togethercomputer/m2-bert-80M-8k-retrieval**
   - Together's own model
   - Optimized for retrieval tasks

### To Change Model:

```bash
# In your .env file
TOGETHER_EMBEDDING_MODEL=BAAI/bge-large-en-v1.5

# Then restart the LangGraph server
uv run langgraph dev --allow-blocking
```

**Note**: Changing the model will require re-ingesting all datapoints to generate new embeddings.

## Summary

✅ **Your system already uses embeddings**
- Embeddings are generated during ingestion
- Stored in MongoDB with each datapoint
- Used by DBSCAN for clustering
- Current model: `BAAI/bge-base-en-v1.5` (768 dimensions)

✅ **No action needed** - Everything is configured correctly!

✅ **Embeddings enable semantic clustering** - Topics are grouped by meaning, not just keywords

## Technical Details

### Embedding Generation Flow:

1. **Text Preparation** (`app/core/ingestion.py:200`)
   - Combines `title + content` into single text
   - Cleans and normalizes text

2. **Embedding Generation** (`app/core/vectorization.py:33`)
   - Uses Together AI API
   - Returns 768-dimensional vector
   - Stored as `List[float]` in MongoDB

3. **Clustering** (`app/core/clustering.py:102`)
   - Extracts embeddings from MongoDB
   - Converts to numpy array
   - Runs DBSCAN with cosine similarity
   - Groups similar embeddings into clusters

### Embedding Storage:

```json
{
  "id": "datapoint_123",
  "title": "...",
  "content": "...",
  "embedding": [0.123, -0.456, 0.789, ...],  // 768 numbers
  "embedding_model": "BAAI/bge-base-en-v1.5",
  "vectorized_at": "2025-11-28T21:27:00Z"
}
```

## Troubleshooting

### Issue: No embeddings in datapoints

**Check:**
1. Is `TOGETHER_API_KEY` set?
2. Did ingestion complete successfully?
3. Check MongoDB: `db.datapoints.findOne({embedding: {$exists: true}})`

### Issue: Clustering finds no clusters

**Check:**
1. Do datapoints have embeddings? (see above)
2. Are embeddings valid? (should be list of 768 floats)
3. Try adjusting `eps` parameter (current: 0.30)

### Issue: Poor clustering quality

**Solutions:**
1. Try larger model: `BAAI/bge-large-en-v1.5`
2. Adjust DBSCAN parameters (`eps`, `min_samples`)
3. Ensure text quality (title + content should be meaningful)

