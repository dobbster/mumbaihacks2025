# Misinformation Detection System - Mumbai Hacks 2025

An AI-powered misinformation detection system that analyzes news articles, clusters them by topic, detects misinformation patterns, and classifies claims using LLMs and pattern analysis.

## System Overview

This system uses LangGraph to orchestrate a multi-stage misinformation detection pipeline:

1. **Planner**: Dynamically selects relevant news sources based on user query
2. **Tavily Search**: Fetches articles from selected sources
3. **Ingestion**: Processes and stores articles with embeddings
4. **Clustering**: Groups similar articles by topic using DBSCAN
5. **Pattern Detection**: Analyzes clusters for misinformation patterns (rapid growth, source credibility, contradictions, narrative evolution)
6. **Classification**: Uses LLM to classify claims as misinformation, legitimate, or uncertain

### System Architecture

![System Architecture Diagram](docs/images/system-architecture.png)

*The diagram above illustrates the complete data flow from user interaction through data ingestion, storage, clustering, and LLM-based analysis to provide fact/fake classification results.*

## Project Structure

```
.
├── app/
│   ├── core/            # Core services (ingestion, clustering, pattern detection, classification)
│   ├── graph.py         # LangGraph workflow definition
│   ├── main.py          # FastAPI application
│   └── routes/          # API endpoints
│       └── verify.py    # Main verification endpoint
├── frontend/             # React frontend application
├── langgraph.json       # LangGraph server configuration
├── pyproject.toml       # Project dependencies
└── README.md
```

## Setup

This project uses `uv` for dependency management.

1. Install `uv` if you haven't already:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Set up MongoDB with Docker:
   ```bash
   docker-compose up -d
   ```
   See `DOCKER_SETUP.md` for detailed instructions.

4. Create a `.env` file with your configuration:
   ```bash
   # MongoDB Configuration
   MONGODB_URL=mongodb://localhost:27017
   MONGODB_DB_NAME=misinformation_detection
   
   # Together AI Configuration
   TOGETHER_API_KEY=your_api_key_here
   TOGETHER_EMBEDDING_MODEL=BAAI/bge-base-en-v1.5
   TOGETHER_LLM_MODEL=meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo
   
   # Tavily Search API
   TAVILY_API_KEY=your_tavily_api_key_here
   ```

## Running the Server

Start the LangGraph development server:

```bash
langgraph dev --allow-blocking --no-browser
```

The server will start on `http://localhost:2024` (default LangGraph port).

## Using the Verification Endpoint

The main endpoint is `/verify` which runs the complete misinformation detection pipeline:

```bash
curl -X POST http://localhost:2024/verify \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Is it true that vaccines cause autism?"}'
```

**Response includes:**
- Classification result (misinformation/legitimate/uncertain)
- Confidence score (0.0-1.0)
- Source URLs from analyzed articles
- Evidence chain with reasoning
- Key indicators that led to the classification

## Frontend

The React frontend is in the `frontend/` directory:

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173` and connects to the backend API.

## Development

- Add your LangGraph agents in `app/graph.py`
- Add custom routes in `app/routes/`
- Configure the server in `langgraph.json`

## Key Features

- **Dynamic Source Selection**: LLM-powered selection of 3-8 relevant news sources (Indian + International)
- **Topic Clustering**: DBSCAN-based clustering of similar articles with relevance filtering
- **Pattern Detection**: Analyzes rapid growth, source credibility, contradictions, and narrative evolution
- **LLM Classification**: Uses Together AI's Llama models for intelligent classification
- **Confidence Scoring**: Provides validated confidence scores (0.0-1.0) for all classifications
- **Evidence Chains**: Transparent reasoning for every classification decision
- **Source Attribution**: Lists all source URLs from analyzed articles

## Dependencies

- `langgraph`: Core LangGraph library for workflow orchestration
- `langgraph-api`: LangGraph API server
- `fastapi`: Web framework for API endpoints
- `langchain-together`: Together AI embeddings and LLM integration
- `pymongo`: MongoDB driver
- `scikit-learn`: DBSCAN clustering algorithm
- `tavily-python`: Tavily search API client
- `together`: Together AI Python SDK

## Documentation

- `QUICKSTART.md`: Quick start guide (5 minutes to get running)
- `DOCKER_SETUP.md`: MongoDB Docker setup guide
- `INGESTION_PLAN.md`: Data ingestion workflow
- `CLUSTERING_GUIDE.md`: Topic clustering guide
- `PATTERN_DETECTION_GUIDE.md`: Pattern detection guide
- `CLASSIFICATION_GUIDE.md`: Classification guide
- `SYSTEM_CRITIQUE.md`: System architecture and status assessment

## LangGraph Workflow

The system follows this LangGraph workflow with detailed node descriptions:

```
┌─────────────────────────────────────────────────────────────────┐
│                        START                                     │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ 1. PLANNER NODE                                                  │
│    • Uses LLM (Together AI) to analyze user query               │
│    • Selects 3-8 most relevant news sources                     │
│    • Considers: topic, geographic focus, information type       │
│    • Sources: Indian (TOI, NDTV, The Hindu, etc.) +             │
│      International (BBC, Reuters, AP, CNN, etc.)                 │
│    • Generates search queries with site: filters                │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. TAVILY_SEARCH NODE                                            │
│    • Executes Tavily API searches for each query                │
│    • Fetches up to 5 results per query                           │
│    • Filters results to only include selected sources           │
│    • Normalizes domain names for accurate matching              │
│    • Extracts: title, content, URL, published date, author        │
│    • Generates unique IDs for each article                       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. INGESTION NODE                                                │
│    • Converts search results to DataPoint objects               │
│    • Generates embeddings using Together AI (BAAI/bge-base)      │
│    • Truncates text to 3000 chars (~400 tokens) for embeddings  │
│    • Stores in MongoDB with metadata                            │
│    • Detects and retrieves duplicate articles                    │
│    • Combines new + retrieved duplicates for downstream use      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. CLUSTERING NODE                                               │
│    • Extracts datapoint IDs from ingested results               │
│    • Runs DBSCAN clustering (eps=0.30, min_samples=2)           │
│    • Includes context from recent datapoints (7 days)            │
│    • Generates topic representation for each cluster            │
│    • Filters clusters by relevance to user query                 │
│    • Uses cosine similarity between cluster topics and query     │
│    • Only keeps clusters with similarity ≥ 0.5                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ 5. PATTERN_DETECTION NODE                                        │
│    • Identifies the most relevant cluster (highest score)       │
│    • Analyzes only the most relevant cluster                    │
│    • Detects rapid growth (10x threshold, tuned down)           │
│    • Analyzes source credibility (credible vs questionable)      │
│    • Detects contradictions (embedding + keyword-based)          │
│    • Tracks narrative evolution over time                       │
│    • Calculates overall risk score (0.0-1.0)                    │
│    • Flags: rapid_growth, low_credibility, contradictions, etc. │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ 6. CLASSIFICATION NODE                                            │
│    • Identifies the most relevant cluster (from pattern_analyses)│
│    • Filters cluster datapoints to current ingestion only       │
│    • Extracts source URLs from filtered datapoints              │
│    • Uses LLM (Meta-Llama-3.1-8B-Instruct-Turbo) to classify    │
│    • Considers: pattern analysis, source credibility, growth     │
│    • Returns: classification (misinformation/legitimate/uncertain)│
│    • Provides: confidence score, evidence chain, key indicators  │
│    • Includes: list of source URLs from analyzed articles        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                         END                                       │
│    Returns classifications with confidence scores and sources    │
└─────────────────────────────────────────────────────────────────┘
```

### Node Details

**State Management**: Each node receives and updates a shared `State` object containing:
- `messages`: User query
- `queries`: Generated search queries
- `selected_sources`: Dynamically selected news sources
- `results`: Raw search results from Tavily
- `ingested_results`: Processed datapoints (new + duplicates)
- `clusters`: Clustered datapoints with topic representations
- `pattern_analyses`: Pattern detection results
- `classifications`: Final classification results

## For Hackathon Judges

This system demonstrates:
- **Multi-stage AI pipeline** using LangGraph with 6 orchestrated nodes
- **Intelligent source selection** using LLM to choose relevant news sources
- **Pattern-based detection** of misinformation signals (growth, credibility, contradictions)
- **LLM-powered classification** with explainable reasoning and evidence chains
- **Real-time processing** of news articles from multiple sources
- **Confidence scoring** with validation for transparency
- **Topic clustering** with relevance filtering to focus on user queries
- **Source attribution** showing all analyzed article URLs

