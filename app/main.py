"""FastAPI application with custom routes for LangGraph server."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import health, verify, ingestion, clustering, pattern_detection, classification


app = FastAPI(
    title="Mumbai Hacks 2025 LangGraph Server",
    description="LangGraph server for misinformation detection",
    version="0.1.0",
)

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite default port
        "http://localhost:3000",  # Alternative React dev port
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include custom routes
app.include_router(health.router, tags=["health"])
app.include_router(ingestion.router)
app.include_router(clustering.router)
app.include_router(pattern_detection.router)
app.include_router(classification.router)
app.include_router(verify.router, tags=["verify"])

