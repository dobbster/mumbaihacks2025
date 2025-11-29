from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from app.graph import graph

router = APIRouter()

class VerifyRequest(BaseModel):
    prompt: str
    max_results: Optional[int] = 5

@router.post("/verify")
def verify(request: VerifyRequest) -> Dict[str, Any]:
    """
    Run the complete LangGraph pipeline and return public updates.
    
    This endpoint:
    1. Plans search queries from the prompt
    2. Searches using Tavily
    3. Ingests and stores datapoints
    4. Clusters datapoints by topic
    5. Detects misinformation patterns
    6. Classifies clusters
    7. Generates public updates
    
    Returns the public_updates from the final state.
    """
    # Initialize state with all required fields
    initial_state = {
        "messages": [request.prompt],
        "queries": [],
        "results": [],
        "ingested_results": None,
        "ingestion_stats": None,
        "clusters": None,
        "clustering_stats": None,
        "pattern_analyses": None,
        "classifications": None,
        "public_updates": None
    }
    
    # Run the complete LangGraph pipeline
    final_state = graph.invoke(initial_state)
    
    # Extract public updates from the final state
    public_updates = final_state.get("public_updates", [])
    
    # Return comprehensive results including public updates
    return {
        "status": "success",
        "prompt": request.prompt,
        "queries": final_state.get("queries"),
        "results": final_state.get("results"),
        "public_updates": public_updates,
        "summary": {
            "total_clusters": len(final_state.get("clusters", {})),
            "total_public_updates": len(public_updates),
            "ingestion_stats": final_state.get("ingestion_stats"),
            "clustering_stats": final_state.get("clustering_stats")
        },
        "clusters": final_state.get("clusters"),
        "pattern_analyses": final_state.get("pattern_analyses"),
        "classifications": final_state.get("classifications")
    }
