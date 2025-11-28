from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import Optional
from app.graph import graph

router = APIRouter()

class VerifyRequest(BaseModel):
    prompt: str
    max_results: Optional[int] = 5

@router.post("/verify")
def verify(request: VerifyRequest):
    # Run the LangGraph flow with the user's prompt
    state = {"messages": [request.prompt], "queries": [], "results": []}
    result = graph.invoke(state)
    # Limit the number of results returned
    results = result["results"][:request.max_results]
    return {"queries": result["queries"], "results": results}
