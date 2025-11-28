# Quick Start Guide

Get up and running with the misinformation detection system in 5 minutes.

## Prerequisites

- Docker and Docker Compose installed
- Python 3.11+ and `uv` package manager
- Together AI API key ([Get one here](https://api.together.xyz/))

## Step 1: Clone and Setup

```bash
# Install dependencies (includes langchain-together)
uv sync
```

## Step 2: Configure Environment

Create a `.env` file in the project root:

**Option 1: With MongoDB Authentication (Recommended)**
```bash
# MongoDB Configuration
# Option A: Full connection string with credentials
MONGODB_URL=mongodb://admin:changeme@localhost:27017/misinformation_detection?authSource=admin
MONGODB_DB_NAME=misinformation_detection

# Option B: Or use individual credentials (code will construct URL)
MONGO_ROOT_USERNAME=admin
MONGO_ROOT_PASSWORD=changeme
MONGODB_DB_NAME=misinformation_detection

# Together AI Configuration
TOGETHER_API_KEY=your_together_api_key_here
TOGETHER_EMBEDDING_MODEL=BAAI/bge-base-en-v1.5
```

**Option 2: Without MongoDB Authentication (Development Only)**
```bash
# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=misinformation_detection

# Together AI Configuration
TOGETHER_API_KEY=your_together_api_key_here
TOGETHER_EMBEDDING_MODEL=BAAI/bge-base-en-v1.5
```

**Note:** If your MongoDB container has authentication enabled (check `docker-compose.yml`), you MUST use Option 1 with credentials.

## Step 3: Start MongoDB

```bash
docker-compose up -d
```

Verify MongoDB is running:
```bash
docker-compose ps
```

## Step 4: Verify Setup

```bash
# Make script executable (if needed)
chmod +x scripts/verify_mongodb.py

# Run verification
python scripts/verify_mongodb.py
```

You should see:
```
✅ MongoDB connection successful!
✅ Database 'misinformation_detection' accessible
✅ Collection 'datapoints' has X indexes
```

## Step 5: Test Ingestion

```bash
# Start the LangGraph server
langgraph dev

# In another terminal, test ingestion
# The API accepts both formats: raw array or wrapped in {"datapoints": [...]}
curl -X POST http://localhost:2024/ingestion/datapoints \
  -H "Content-Type: application/json" \
  -d @examples/datapoints_example.json

# Or test Together AI connection (use uv run for proper environment)
uv run python scripts/check_together_api.py
```

## Step 6: Test Clustering

```python
from app.core.clustering import ClusteringService
from app.dependencies import get_storage_service

storage_service = get_storage_service()
clustering_service = ClusteringService(storage_service)
clusters = clustering_service.cluster_recent_datapoints(hours=24)
print(f"Found {len(clusters)} clusters")
```

## Troubleshooting

### MongoDB won't start
```bash
docker-compose logs mongodb
```

### Can't connect to MongoDB
- Check if container is running: `docker-compose ps`
- Verify port 27017 is not in use
- Check `MONGODB_URL` in `.env`

### Together AI errors
- Verify `TOGETHER_API_KEY` is set correctly
- Check your API key at https://api.together.xyz/

## Next Steps

- Read `DOCKER_SETUP.md` for detailed MongoDB setup
- Read `TOGETHER_AI_SETUP.md` for embedding configuration
- Read `INGESTION_PLAN.md` for data ingestion workflow
- Read `CLUSTERING_RECOMMENDATIONS.md` for clustering tuning

## Common Commands

```bash
# Start MongoDB
docker-compose up -d

# Stop MongoDB (keeps data)
docker-compose stop

# View MongoDB logs
docker-compose logs -f mongodb

# Access MongoDB shell
docker exec -it misinformation_mongodb mongosh

# Verify setup
python scripts/verify_mongodb.py
```

