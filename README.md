# Misinformation Detection System - Mumbai Hacks 2025

An AI-powered misinformation detection system that analyzes news articles, clusters them by topic, detects misinformation patterns, and classifies claims using LLMs and external fact-checking sources.

## System Overview

This system uses LangGraph to orchestrate a multi-stage misinformation detection pipeline:

1. **Planner**: Dynamically selects relevant news sources based on user query
2. **Tavily Search**: Fetches articles from selected sources
3. **Ingestion**: Processes and stores articles with embeddings
4. **Clustering**: Groups similar articles by topic using DBSCAN
5. **Pattern Detection**: Analyzes clusters for misinformation patterns (rapid growth, source credibility, contradictions, narrative evolution)
6. **Fact-Checking**: Searches external fact-checking organizations (Snopes, PolitiFact, etc.)
7. **Classification**: Uses LLM to classify claims as misinformation, legitimate, or uncertain

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
- Confidence score
- Fact-check results from external sources
- Source URLs
- Evidence chain

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

- **Dynamic Source Selection**: LLM-powered selection of relevant news sources
- **Topic Clustering**: DBSCAN-based clustering of similar articles
- **Pattern Detection**: Analyzes rapid growth, source credibility, contradictions, and narrative evolution
- **External Fact-Checking**: Integrates with Snopes, PolitiFact, FactCheck.org, and other fact-checkers
- **LLM Classification**: Uses Together AI's Llama models for intelligent classification
- **Confidence Scoring**: Provides confidence scores (0.0-1.0) for all classifications
- **Evidence Chains**: Transparent reasoning for every classification decision

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
- `VERIFICATION_GUIDE.md`: Fact-checking and verification guide

## Workflow

The system follows this workflow:

```
User Query
    ↓
Planner (Select Sources)
    ↓
Tavily Search (Fetch Articles)
    ↓
Ingestion (Process & Store)
    ↓
Clustering (Group by Topic)
    ↓
Pattern Detection (Analyze Patterns)
    ↓
Fact-Checking (External Verification)
    ↓
Classification (Final Verdict)
    ↓
Results
```

## For Hackathon Judges

This system demonstrates:
- **Multi-stage AI pipeline** using LangGraph
- **Intelligent source selection** based on query context
- **Pattern-based detection** of misinformation signals
- **External fact-checking integration** for verification
- **LLM-powered classification** with explainable reasoning
- **Real-time processing** of news articles
- **Confidence scoring** for transparency

