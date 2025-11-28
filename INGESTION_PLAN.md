# Data Ingestion and Vectorization Plan

## Overview

This document outlines the plan for ingesting JSON datapoints, vectorizing them, and storing them in MongoDB for topic clustering.

## Data Flow

```
JSON List (RSS/Tavily) 
    ↓
Ingestion Service (load & validate)
    ↓
Vectorization Service (generate embeddings)
    ↓
Storage Service (store in MongoDB)
    ↓
Clustering Service (group similar datapoints)
```

## JSON Data Format

### Example Structure

See `examples/datapoints_example.json` for complete examples.

**Key Fields:**
- `id`: Unique identifier
- `source_type`: "rss" or "tavily"
- `title`: Article title
- `content`: Article content (main text)
- `published_at`: ISO datetime string
- `categories`: List of topic categories
- `embedding`: Generated vector (added during processing)

## Implementation Components

### 1. Ingestion Service (`app/core/ingestion.py`)

**Responsibilities:**
- Load datapoints from JSON (file or API request)
- Validate data structure
- Process each datapoint:
  - Prepare text for embedding (title + content)
  - Generate embedding via VectorizationService
  - Convert to StoredDataPoint format
  - Store in MongoDB via StorageService

**Key Methods:**
- `load_datapoints_from_json()`: Load from file
- `load_datapoints_from_dict()`: Load from Python dict
- `process_datapoint()`: Process single datapoint
- `ingest_datapoints()`: Batch processing

### 2. Vectorization Service (`app/core/vectorization.py`)

**Responsibilities:**
- Generate embeddings using OpenAI/LangChain
- Support single and batch embedding generation
- Handle embedding model configuration

**Key Methods:**
- `generate_embedding()`: Single text → embedding
- `generate_embeddings_batch()`: Multiple texts → embeddings

### 3. Storage Service (`app/core/storage.py`)

**Responsibilities:**
- MongoDB operations
- Create indexes for efficient queries
- Store datapoints with embeddings
- Retrieve datapoints for clustering

**Key Methods:**
- `store_datapoint()`: Store/upsert datapoint
- `get_recent_datapoints()`: Get datapoints by time window
- `get_unprocessed_datapoints()`: Get datapoints needing processing
- `update_cluster_id()`: Update cluster assignment

### 4. Clustering Service (`app/core/clustering.py`)

**Responsibilities:**
- Find similar datapoints using cosine similarity
- Group datapoints into clusters
- Update cluster assignments in MongoDB

**Key Methods:**
- `find_similar_datapoints()`: Find similar to query
- `cluster_datapoints()`: Group datapoints into clusters
- `cluster_recent_datapoints()`: Cluster unclustered datapoints

## Usage Examples

### 1. Ingest from JSON File

```python
from app.core.ingestion import IngestionService
from app.dependencies import get_ingestion_service

ingestion_service = get_ingestion_service()

# Load from file
datapoints = ingestion_service.load_datapoints_from_json("datapoints.json")

# Process and store
stats = ingestion_service.ingest_datapoints(datapoints)
print(f"Stored {stats['stored']} datapoints")
```

### 2. Ingest from API Request

```python
# POST /ingestion/datapoints
{
    "datapoints": [
        {
            "id": "rss_001",
            "source_type": "rss",
            "title": "...",
            "content": "...",
            ...
        }
    ]
}
```

### 3. Cluster Recent Datapoints

```python
from app.core.clustering import ClusteringService
from app.dependencies import get_storage_service

storage_service = get_storage_service()
clustering_service = ClusteringService(storage_service)

# Cluster datapoints from last 24 hours
clusters = clustering_service.cluster_recent_datapoints(hours=24)
print(f"Found {len(clusters)} clusters")
```

## MongoDB Schema

### Collection: `datapoints`

```json
{
    "_id": "rss_001",
    "source_type": "rss",
    "source_name": "BBC News",
    "title": "...",
    "content": "...",
    "url": "...",
    "published_at": ISODate("2025-01-15T10:30:00Z"),
    "ingested_at": ISODate("2025-01-15T10:35:00Z"),
    "embedding": [0.1, 0.2, ...],  // Vector array
    "embedding_model": "text-embedding-3-small",
    "vectorized_at": ISODate("2025-01-15T10:35:01Z"),
    "text_for_embedding": "title + content combined",
    "processed": false,
    "clustered": false,
    "cluster_id": null,
    "categories": ["health", "virus"]
}
```

### Indexes

- `published_at`: For temporal queries
- `ingested_at`: For processing order
- `source_type`: For filtering
- `processed`: For finding unprocessed items
- `cluster_id`: For cluster queries
- Text index on `title` and `content`

## Environment Variables

```bash
# MongoDB
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=misinformation_detection

# Together AI Embeddings
TOGETHER_API_KEY=your_together_api_key_here
TOGETHER_EMBEDDING_MODEL=BAAI/bge-base-en-v1.5  # Optional, defaults to bge-base
```

**Note**: Get your Together AI API key from https://api.together.xyz/

## Processing Pipeline

### Step 1: Ingestion
1. Receive JSON list of datapoints
2. Validate each datapoint
3. For each datapoint:
   - Combine title + content for embedding
   - Generate embedding vector
   - Store in MongoDB with metadata

### Step 2: Clustering (Separate Process)
1. Query unclustered datapoints
2. Calculate cosine similarity between embeddings
3. Group similar datapoints (similarity > threshold)
4. Update cluster_id in MongoDB

### Step 3: Pattern Detection (Uses Clusters)
1. Query datapoints by cluster
2. Analyze frequency trends within clusters
3. Detect emerging patterns
4. Flag for misinformation detection

## Error Handling

- Invalid datapoints: Log warning, skip, continue processing
- Embedding failures: Log error, mark as failed
- Storage failures: Retry logic, log errors
- Partial failures: Return statistics with error details

## Performance Considerations

- Batch processing: Process multiple datapoints in parallel
- Embedding caching: Consider caching for duplicate content
- MongoDB indexes: Ensure indexes are created for fast queries
- Batch embeddings: Use `embed_documents()` for multiple texts

## Next Steps

1. Set up MongoDB connection
2. Get Together AI API key from https://api.together.xyz/
3. Set environment variables (see TOGETHER_AI_SETUP.md)
4. Test ingestion with example JSON
5. Verify embeddings are stored correctly
6. Test clustering on sample data
7. Integrate with LangGraph workflow

See `TOGETHER_AI_SETUP.md` for detailed setup instructions.

