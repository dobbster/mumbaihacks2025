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
TOGETHER_LLM_MODEL=meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo

# Tavily Search API
TAVILY_API_KEY=your_tavily_api_key_here
```

**Option 2: Without MongoDB Authentication (Development Only)**
```bash
# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=misinformation_detection

# Together AI Configuration
TOGETHER_API_KEY=your_together_api_key_here
TOGETHER_EMBEDDING_MODEL=BAAI/bge-base-en-v1.5
TOGETHER_LLM_MODEL=meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo

# Tavily Search API
TAVILY_API_KEY=your_tavily_api_key_here
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

## Step 5: Start the LangGraph Server

```bash
# Start the LangGraph server
langgraph dev --allow-blocking --no-browser
```

The server will start on `http://localhost:2024`.

## Step 6: Test the Verification Endpoint

The main endpoint is `/verify` which runs the complete misinformation detection pipeline:

```bash
# Test with a simple query
curl -X POST http://localhost:2024/verify \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Is it true that vaccines cause autism?", "max_results": 5}'
```

**Response includes:**
- Classification result (misinformation/legitimate/uncertain)
- Confidence score
- Fact-check results from external sources
- Source URLs
- Evidence chain

### Alternative: Test Individual Components

You can also test individual components:

```bash
# Test ingestion
curl -X POST http://localhost:2024/ingestion/datapoints \
  -H "Content-Type: application/json" \
  -d @examples/datapoints_example.json

# Test clustering
curl -X POST "http://localhost:2024/clustering/cluster?hours=8760&eps=0.30&min_cluster_size=2"
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

## Frontend (Optional)

To run the React frontend:

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173` and connects to the backend API.

## Next Steps

- Read `README.md` for system overview
- Read `DOCKER_SETUP.md` for detailed MongoDB setup
- Read `INGESTION_PLAN.md` for data ingestion workflow
- Read `CLUSTERING_GUIDE.md` for clustering details
- Read `PATTERN_DETECTION_GUIDE.md` for pattern detection
- Read `CLASSIFICATION_GUIDE.md` for classification
- Read `VERIFICATION_GUIDE.md` for fact-checking

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

