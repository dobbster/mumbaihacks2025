"""Simple LangGraph agent definition."""

from typing import Annotated, Optional, Dict, Any, List
import os
from dotenv import load_dotenv
import requests
from tavily import TavilyClient
from together import Together
from pymongo import MongoClient
from langchain_together import TogetherEmbeddings

from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict
from app.core.ingestion import IngestionService
from app.core.vectorization import VectorizationService
from app.core.storage import StorageService
from app.core.models import DataPoint
from app.dependencies import (
    get_clustering_service,
    get_pattern_detection_service,
    get_classification_service,
    get_verification_service,
    get_public_update_service,
    get_storage_service
)

load_dotenv()
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
tavily_client = TavilyClient(TAVILY_API_KEY)
together_client = Together(api_key=TOGETHER_API_KEY)

# Initialize MongoDB client with authentication support
mongo_url = os.getenv("MONGODB_URL")
username = os.getenv("MONGO_ROOT_USERNAME", "admin")
password = os.getenv("MONGO_ROOT_PASSWORD", "changeme")
db_name = os.getenv("MONGODB_DB_NAME", "misinformation_detection")

# If MONGODB_URL is set but doesn't contain credentials, construct authenticated URL
if mongo_url and "@" not in mongo_url and username and password:
    # MONGODB_URL provided but no credentials - add them
    # Extract host/port from MONGODB_URL or use defaults
    if "://" in mongo_url:
        # Extract everything after mongodb://
        parts = mongo_url.split("://", 1)[1]
        if "/" in parts:
            host_port = parts.split("/")[0]
        else:
            host_port = parts.split("?")[0] if "?" in parts else parts
    else:
        host_port = "localhost:27017"
    
    mongo_url = f"mongodb://{username}:{password}@{host_port}/{db_name}?authSource=admin"
elif not mongo_url:
    # No MONGODB_URL provided - construct from individual credentials
    if username and password:
        # Construct authenticated connection string
        mongo_url = f"mongodb://{username}:{password}@localhost:27017/{db_name}?authSource=admin"
    else:
        # No authentication
        mongo_url = "mongodb://localhost:27017"
# If MONGODB_URL is set and contains credentials, use it as-is

mongo_client = MongoClient(mongo_url)

# Initialize services
together_model = os.getenv("TOGETHER_EMBEDDING_MODEL", "BAAI/bge-base-en-v1.5")
vectorization_service = VectorizationService(
    TogetherEmbeddings(model=together_model, together_api_key=TOGETHER_API_KEY)
)
storage_service = StorageService(mongo_client)
ingestion_service = IngestionService(vectorization_service, storage_service)


class State(TypedDict):
    """State of the agent."""
    messages: Annotated[list, lambda x, y: x + y]
    queries: list
    results: list
    ingested_results: Optional[List[DataPoint]]
    ingestion_stats: Optional[Dict[str, Any]]
    clusters: Optional[Dict[str, List[Dict[str, Any]]]]
    clustering_stats: Optional[Dict[str, Any]]
    pattern_analyses: Optional[Dict[str, Dict[str, Any]]]
    classifications: Optional[Dict[str, Any]]
    verifications: Optional[Dict[str, Any]]
    public_updates: Optional[List[Dict[str, Any]]]


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


def clustering_node(state: State) -> State:
    """Cluster recent datapoints into topic groups using DBSCAN."""
    clustering_service = get_clustering_service()
    
    # Cluster recent datapoints (default: last 7 days, min cluster size 2)
    hours = 168  # 7 days
    min_cluster_size = 2
    eps = 0.30  # DBSCAN parameter
    
    # Update clustering service parameters
    clustering_service.eps = eps
    clustering_service.min_samples = min_cluster_size
    
    # Run clustering
    clusters = clustering_service.cluster_recent_datapoints(
        hours=hours,
        min_cluster_size=min_cluster_size,
        use_dbscan=True,
        force_recluster=False
    )
    
    # Get statistics
    stats = clustering_service.get_cluster_statistics(clusters)
    
    # Convert clusters to serializable format
    clusters_dict = {}
    for cluster_id, datapoints in clusters.items():
        clusters_dict[cluster_id] = [
            {
                "id": dp.get("_id") or dp.get("id"),
                "title": dp.get("title"),
                "source_name": dp.get("source_name"),
                "source_type": dp.get("source_type"),
                "published_at": str(dp.get("published_at")),
                "categories": dp.get("categories", [])
            }
            for dp in datapoints
        ]
    
    state["clusters"] = clusters_dict
    state["clustering_stats"] = {
        "clusters_found": len(clusters),
        "total_datapoints": stats.get("total_datapoints", 0),
        "statistics": stats
    }
    return state


def pattern_detection_node(state: State) -> State:
    """Analyze clusters for misinformation patterns."""
    pattern_service = get_pattern_detection_service()
    clusters = state.get("clusters", {})
    
    if not clusters:
        state["pattern_analyses"] = {}
        return state
    
    # Analyze all clusters
    hours = 168
    min_cluster_size = 2
    results = pattern_service.analyze_all_clusters(
        hours=hours,
        min_cluster_size=min_cluster_size
    )
    
    state["pattern_analyses"] = results.get("analyses", {})
    return state


def classification_node(state: State) -> State:
    """Classify clusters as misinformation, legitimate, or uncertain."""
    classification_service = get_classification_service()
    pattern_service = get_pattern_detection_service()
    storage_service = get_storage_service()
    
    clusters = state.get("clusters", {})
    pattern_analyses = state.get("pattern_analyses", {})
    
    if not clusters:
        state["classifications"] = {}
        return state
    
    classifications = {}
    
    # Classify each cluster
    for cluster_id in clusters.keys():
        try:
            # Get cluster datapoints
            cluster_datapoints = storage_service.get_datapoints_by_cluster(cluster_id)
            
            if not cluster_datapoints:
                continue
            
            # Get pattern analysis for this cluster (run if not available)
            pattern_analysis = pattern_analyses.get(cluster_id)
            if not pattern_analysis:
                # Run pattern detection for this cluster if not already done
                pattern_analysis = pattern_service.analyze_cluster(cluster_id)
            
            # Classify the cluster (pattern_analysis is required)
            classification_result = classification_service.classify_cluster(
                cluster_id=cluster_id,
                pattern_analysis=pattern_analysis,
                cluster_datapoints=cluster_datapoints
            )
            
            classifications[cluster_id] = classification_result.model_dump() if hasattr(classification_result, 'model_dump') else classification_result
            
        except Exception as e:
            print(f"Error classifying cluster {cluster_id}: {e}")
            continue
    
    state["classifications"] = classifications
    return state


def verification_node(state: State) -> State:
    """Verify clusters through fact-checking and cross-referencing."""
    verification_service = get_verification_service()
    classification_service = get_classification_service()
    storage_service = get_storage_service()
    
    clusters = state.get("clusters", {})
    classifications = state.get("classifications", {})
    
    if not clusters:
        state["verifications"] = {}
        return state
    
    verifications = {}
    
    # Verify each cluster
    for cluster_id in clusters.keys():
        try:
            # Get classification result for this cluster
            classification_result = classifications.get(cluster_id, {})
            
            # Verify the cluster
            verification_result = verification_service.verify_cluster(
                cluster_id=cluster_id,
                classification_result=classification_result
            )
            
            verifications[cluster_id] = verification_result.model_dump() if hasattr(verification_result, 'model_dump') else verification_result
            
        except Exception as e:
            print(f"Error verifying cluster {cluster_id}: {e}")
            continue
    
    state["verifications"] = verifications
    return state


def public_updates_node(state: State) -> State:
    """Generate user-friendly public updates for clusters."""
    public_update_service = get_public_update_service()
    clusters = state.get("clusters", {})
    
    if not clusters:
        state["public_updates"] = []
        return state
    
    public_updates = []
    
    # Generate update for each cluster
    for cluster_id in clusters.keys():
        try:
            update = public_update_service.generate_update(
                cluster_id=cluster_id,
                use_llm=True
            )
            
            public_updates.append(update.model_dump() if hasattr(update, 'model_dump') else update)
            
        except Exception as e:
            print(f"Error generating update for cluster {cluster_id}: {e}")
            continue
    
    state["public_updates"] = public_updates
    return state


# Create the graph
graph_builder = StateGraph(State)
graph_builder.add_node("planner", planner_node)
graph_builder.add_node("tavily_search", tavily_search_node)
graph_builder.add_node("ingestion", ingestion_node)
graph_builder.add_node("clustering", clustering_node)
graph_builder.add_node("pattern_detection", pattern_detection_node)
graph_builder.add_node("classification", classification_node)
graph_builder.add_node("verification", verification_node)
graph_builder.add_node("public_updates", public_updates_node)
graph_builder.add_node("echo", echo_node)

# Define the workflow
graph_builder.add_edge(START, "planner")
graph_builder.add_edge("planner", "tavily_search")
graph_builder.add_edge("tavily_search", "ingestion")
graph_builder.add_edge("ingestion", "clustering")
graph_builder.add_edge("clustering", "pattern_detection")
graph_builder.add_edge("pattern_detection", "classification")
graph_builder.add_edge("classification", "verification")
graph_builder.add_edge("verification", "public_updates")
graph_builder.add_edge("public_updates", "echo")
graph_builder.add_edge("echo", END)

graph = graph_builder.compile()

