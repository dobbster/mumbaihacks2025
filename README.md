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

3. Create a `.env` file (optional, for environment variables):
   ```bash
   touch .env
   ```

## Running the Server

Start the LangGraph development server:

```bash
langgraph dev
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

