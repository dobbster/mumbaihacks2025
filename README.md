# Mumbai Hacks 2025 LangGraph Server

A skeleton LangGraph server with a custom `/health` endpoint.

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   ├── graph.py         # LangGraph agent definition
│   └── routes/
│       ├── __init__.py
│       └── health.py    # Health check endpoint
├── langgraph.json       # LangGraph server configuration
├── pyproject.toml       # Project dependencies (uv)
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
   ```

## Running the Server

Start the LangGraph development server:

```bash
langgraph dev --allow-blocking --no-browser
```

The server will start and be available at the default LangGraph endpoint. The custom `/health` endpoint will be available at `/health`.

## Testing the Health Endpoint

Once the server is running, you can test the health endpoint:

```bash
curl http://localhost:8123/health
```

Expected response:
```json
{"status": "healthy"}
```

## Development

- Add your LangGraph agents in `app/graph.py`
- Add custom routes in `app/routes/`
- Configure the server in `langgraph.json`

## Dependencies

- `langgraph`: Core LangGraph library
- `langgraph-api`: LangGraph API server
- `fastapi`: Web framework for custom routes
- `uvicorn`: ASGI server
- `langchain-together`: Together AI embeddings integration
- `pymongo`: MongoDB driver
- `scikit-learn`: DBSCAN clustering

## Documentation

- `DOCKER_SETUP.md`: MongoDB Docker setup guide
- `TOGETHER_AI_SETUP.md`: Together AI configuration
- `INGESTION_PLAN.md`: Data ingestion workflow
- `CLUSTERING_RECOMMENDATIONS.md`: Clustering setup and tuning

