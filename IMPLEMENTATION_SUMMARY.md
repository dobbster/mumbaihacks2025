# Implementation Summary: Data Ingestion & Vectorization Plan

## Overview

This plan implements a complete pipeline for ingesting JSON datapoints from RSS feeds and Tavily MCP server, vectorizing them, and storing them in MongoDB for topic clustering.

## What Was Created

### 1. JSON Example (`examples/datapoints_example.json`)
- Sample datapoints from RSS and Tavily sources
- Shows expected data structure
- Includes all required fields for processing

### 2. Core Models (`app/core/models.py`)
- `DataPoint`: Input model for incoming datapoints
- `StoredDataPoint`: Model for MongoDB storage with embeddings
- `Claim`: Model for extracted claims (for future use)

### 3. Ingestion Service (`app/core/ingestion.py`)
- Loads datapoints from JSON (file or dict)
- Processes each datapoint:
  - Prepares text (title + content) for embedding
  - Generates embedding via VectorizationService
  - Converts to StoredDataPoint format
  - Stores in MongoDB
- Batch processing support
- Error handling and statistics

### 4. Vectorization Service (`app/core/vectorization.py`)
- Generates embeddings using OpenAI/LangChain
- Supports single and batch embedding generation
- Configurable embedding model

### 5. Storage Service (`app/core/storage.py`)
- MongoDB operations
- Automatic index creation for efficient queries
- Methods for:
  - Storing datapoints
  - Retrieving recent datapoints
  - Finding unprocessed datapoints
  - Updating cluster assignments

### 6. Clustering Service (`app/core/clustering.py`)
- Cosine similarity calculation
- Find similar datapoints
- Cluster datapoints into groups
- Update cluster IDs in MongoDB

### 7. API Route (`app/routes/ingestion.py`)
- POST `/ingestion/datapoints` endpoint
- Accepts JSON list of datapoints
- Returns ingestion statistics

### 8. Dependencies (`app/dependencies.py`)
- Dependency injection for services
- MongoDB client setup
- Embeddings model configuration
- Service initialization

## Data Flow

```
1. JSON List (from RSS/Tavily)
   ↓
2. IngestionService.load_datapoints_from_dict()
   ↓
3. For each datapoint:
   - Prepare text (title + content)
   - Generate embedding
   - Store in MongoDB
   ↓
4. ClusteringService.cluster_recent_datapoints()
   - Find similar datapoints
   - Group into clusters
   - Update cluster_id in MongoDB
   ↓
5. Ready for pattern detection & misinformation analysis
```

## Key Features

### ✅ Handles Both Source Types
- RSS feeds: Standard news article format
- Tavily MCP: Includes search_query and relevance_score

### ✅ Vectorization Strategy
- Combines title + content for better semantic understanding
- Stores embedding vector in MongoDB
- Uses configurable embedding model

### ✅ Efficient Storage
- MongoDB indexes for fast queries:
  - Temporal queries (published_at, ingested_at)
  - Source filtering (source_type, source_name)
  - Processing status (processed, clustered)
  - Cluster queries (cluster_id)
  - Text search (title, content)

### ✅ Clustering Ready
- Cosine similarity for finding similar datapoints
- Configurable similarity threshold (default: 0.75)
- Minimum cluster size support
- Automatic cluster ID assignment

## Usage

### 1. Ingest from JSON File

```python
from app.core.ingestion import IngestionService
from app.dependencies import get_ingestion_service

ingestion_service = get_ingestion_service()
datapoints = ingestion_service.load_datapoints_from_json("datapoints.json")
stats = ingestion_service.ingest_datapoints(datapoints)
```

### 2. Ingest via API

```bash
curl -X POST http://localhost:8123/ingestion/datapoints \
  -H "Content-Type: application/json" \
  -d @examples/datapoints_example.json
```

### 3. Cluster Datapoints

```python
from app.core.clustering import ClusteringService
from app.dependencies import get_storage_service

storage_service = get_storage_service()
clustering_service = ClusteringService(storage_service)
clusters = clustering_service.cluster_recent_datapoints(hours=24)
```

## MongoDB Schema

Each datapoint is stored with:
- Original fields (id, title, content, source, etc.)
- `embedding`: Vector array for similarity search
- `text_for_embedding`: Combined text used for embedding
- `processed`: Boolean flag
- `clustered`: Boolean flag
- `cluster_id`: Assigned cluster identifier

## Environment Setup

```bash
# MongoDB
export MONGODB_URL="mongodb://localhost:27017"
export MONGODB_DB_NAME="misinformation_detection"

# Embeddings (choose one)
export OPENAI_API_KEY="your_key"
export OPENAI_BASE_URL="https://your-llm-gateway.com"  # Optional
```

## Next Steps

1. **Set up MongoDB**: Ensure MongoDB is running and accessible
2. **Configure Embeddings**: Set up OpenAI API key or LLM Gateway
3. **Test Ingestion**: Use example JSON to test the pipeline
4. **Verify Storage**: Check MongoDB for stored datapoints with embeddings
5. **Test Clustering**: Run clustering on sample data
6. **Integrate with LangGraph**: Connect to your misinformation detection workflow

## Integration with LangGraph Workflow

The stored datapoints with embeddings are ready for:
- Pattern detection node: Query similar datapoints
- Classification node: Use cluster metadata
- Verification node: Cross-reference with stored claims
- Public update node: Generate contextual explanations

## Error Handling

- Invalid datapoints: Logged and skipped
- Embedding failures: Logged with error details
- Storage failures: Retry logic and error reporting
- Partial failures: Statistics returned with error list

## Performance Notes

- Batch processing: Process multiple datapoints efficiently
- Batch embeddings: Use `embed_documents()` for multiple texts
- MongoDB indexes: Created automatically for fast queries
- Similarity threshold: Adjustable (default 0.75)

This implementation ensures every datapoint from your JSON list is:
1. ✅ Validated
2. ✅ Vectorized with embeddings
3. ✅ Stored in MongoDB
4. ✅ Ready for topic clustering
5. ✅ Available for pattern detection

