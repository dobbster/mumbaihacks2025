"""FastAPI application with custom routes for LangGraph server."""

from fastapi import FastAPI

from app.routes import health

app = FastAPI(
    title="Mumbai Hacks 2025 LangGraph Server",
    description="LangGraph server with custom health endpoint",
    version="0.1.0",
)

# Include custom routes
app.include_router(health.router, tags=["health"])

