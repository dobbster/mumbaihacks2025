"""FastAPI application with custom routes for LangGraph server."""

from fastapi import FastAPI

from app.routes import health, ingestion, clustering, pattern_detection, classification, verification, public_updates

app = FastAPI(
    title="Mumbai Hacks 2025 LangGraph Server",
    description="LangGraph server for misinformation detection",
    version="0.1.0",
)

# Include custom routes
app.include_router(health.router, tags=["health"])
app.include_router(ingestion.router)
app.include_router(clustering.router)
app.include_router(pattern_detection.router)
app.include_router(classification.router)
app.include_router(verification.router)
app.include_router(public_updates.router)

