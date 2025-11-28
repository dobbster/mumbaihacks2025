"""Simple LangGraph agent definition."""

from typing import Annotated
import os
from dotenv import load_dotenv
import requests
from tavily import TavilyClient
from together import Together
from pymongo import MongoClient
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict
from app.core.ingestion import IngestionService
from app.core.vectorization import VectorizationService
from app.core.storage import StorageService
from app.core.models import DataPoint

load_dotenv()
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
tavily_client = TavilyClient(TAVILY_API_KEY)
together_client = Together(api_key=TOGETHER_API_KEY)

# Initialize services (adjust model and DB details as needed)
mongo_client = MongoClient("mongodb://localhost:27017/")
vectorization_service = VectorizationService(HuggingFaceBgeEmbeddings(model_name="BAAI/bge-base-en-v1.5"))
storage_service = StorageService(mongo_client)
ingestion_service = IngestionService(vectorization_service, storage_service)


class State(TypedDict):
    """State of the agent."""
    messages: Annotated[list, lambda x, y: x + y]
    queries: list
    results: list


def echo_node(state: State) -> State:
    """Echo the last message."""
    return {"messages": state["messages"]}


def planner_node(state: State) -> State:
    """Generate search queries from the user's prompt using Together Python SDK, limited to Indian news outlets."""
    user_message = state["messages"][-1] if state["messages"] else ""
    # List of trusted Indian news domains
    indian_news_sites = [
        "timesofindia.indiatimes.com",
        "ndtv.com",
        "thehindu.com",
        "indianexpress.com",
        "hindustantimes.com",
        "livemint.com",
        "business-standard.com",
        "news18.com",
        "scroll.in",
        "deccanherald.com"
    ]
    # Generate queries for each site
    queries = [f"site:{site} {user_message}" for site in indian_news_sites]
    state["queries"] = queries
    return state


def tavily_search_node(state: State) -> State:
    """Fetch results from Tavily using queries and format them for the API response."""
    import datetime
    queries = state.get("queries", [])
    formatted_results = []
    for idx, q in enumerate(queries):
        try:
            response = tavily_client.search(query=q, num_results=3)
            for i, res in enumerate(response.get("results", [])):
                formatted_results.append({
                    "id": f"tavily_{idx}_{i}",
                    "source_type": "tavily",
                    "source_name": "Tavily Search",
                    "source_url": "https://api.tavily.com",
                    "title": res.get("title"),
                    "content": res.get("content"),
                    "url": res.get("url"),
                    "published_at": res.get("published_at",datetime.datetime.utcnow().isoformat() + "Z"),
                    "author": res.get("author"),
                    "categories": res.get("categories", []),
                    "search_query": q,
                    "relevance_score": res.get("score"),
                    "ingested_at": datetime.datetime.utcnow().isoformat() + "Z"
                })
        except Exception as e:
            formatted_results.append({
                "id": f"tavily_{idx}_error",
                "source_type": "tavily",
                "source_name": "Tavily Search",
                "source_url": "https://api.tavily.com",
                "title": None,
                "content": str(e),
                "url": None,
                "published_at": None,
                "author": None,
                "categories": [],
                "search_query": q,
                "relevance_score": None,
                "ingested_at": datetime.datetime.utcnow().isoformat() + "Z"
            })
    state["results"] = formatted_results
    return state


def ingestion_node(state: State) -> State:
    """Ingest results from Tavily search node using full pipeline."""
    raw_results = state.get("results", [])
    # Convert raw results to DataPoint objects
    # print("Ingesting results:", raw_results)
    datapoints = []
    for item in raw_results:
        try:
            # print("Processing item:", item)
            datapoint = DataPoint(**item)
            datapoints.append(datapoint)
        except Exception as e:
            # Optionally log or collect errors
            print("Error processing item:", item, "Error:", e)
            continue
    # Ingest datapoints (vectorize and store)
    stats = ingestion_service.ingest_datapoints(datapoints)
    state["ingested_results"] = datapoints
    state["ingestion_stats"] = stats
    return state


# Create the graph
graph_builder = StateGraph(State)
graph_builder.add_node("planner", planner_node)
graph_builder.add_node("tavily_search", tavily_search_node)
graph_builder.add_node("ingestion", ingestion_node)
graph_builder.add_node("echo", echo_node)
graph_builder.add_edge(START, "planner")
graph_builder.add_edge("planner", "tavily_search")
graph_builder.add_edge("tavily_search", "ingestion")
graph_builder.add_edge("ingestion", "echo")
graph_builder.add_edge("echo", END)

graph = graph_builder.compile()

