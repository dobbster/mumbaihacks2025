"""Simple LangGraph agent definition."""

from typing import Annotated, Optional, Dict, Any, List
import os
import logging
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
    get_public_update_service,
    get_storage_service
)

logger = logging.getLogger(__name__)

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
    import hashlib
    queries = state.get("queries", [])
    formatted_results = []
    for idx, q in enumerate(queries):
        try:
            response = tavily_client.search(query=q, num_results=3)
            for i, res in enumerate(response.get("results", [])):
                # Generate unique ID based on URL (if available) or fallback to deterministic ID
                article_url = res.get("url")
                if article_url:
                    # Use URL hash for unique, deterministic ID
                    url_hash = hashlib.md5(article_url.encode()).hexdigest()[:8]
                    datapoint_id = f"tavily_{url_hash}"
                else:
                    # Fallback to query-based ID if no URL
                    datapoint_id = f"tavily_{idx}_{i}_{int(datetime.datetime.utcnow().timestamp())}"
                
                formatted_results.append({
                    "id": datapoint_id,
                    "source_type": "tavily",
                    "source_name": "Tavily Search",
                    "source_url": "https://api.tavily.com",
                    "title": res.get("title"),
                    "content": res.get("content"),
                    "url": article_url,
                    "published_at": res.get("published_at",datetime.datetime.utcnow().isoformat() + "Z"),
                    "author": res.get("author"),
                    "categories": res.get("categories", []),
                    "search_query": q,
                    "relevance_score": res.get("score"),
                    "ingested_at": datetime.datetime.utcnow().isoformat() + "Z"
                })
        except Exception as e:
            # For errors, use timestamp-based ID to ensure uniqueness
            error_id = f"tavily_{idx}_error_{int(datetime.datetime.utcnow().timestamp() * 1000000)}"
            formatted_results.append({
                "id": error_id,
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
    
    # Combine newly ingested datapoints with retrieved duplicates
    all_datapoints = datapoints.copy()
    
    # Add retrieved duplicates from MongoDB (if any)
    retrieved_duplicates = stats.get("retrieved_duplicates_list", [])
    if retrieved_duplicates:
        for dup_dict in retrieved_duplicates:
            try:
                dup_datapoint = DataPoint(**dup_dict)
                all_datapoints.append(dup_datapoint)
            except Exception as e:
                print(f"Error converting retrieved duplicate to DataPoint: {e}")
                continue
    
    state["ingested_results"] = all_datapoints
    state["ingestion_stats"] = stats
    return state


def clustering_node(state: State) -> State:
    """Cluster datapoints from ingested_results into topic groups using DBSCAN."""
    clustering_service = get_clustering_service()
    storage_service = get_storage_service()
    
    # Get datapoints from current ingestion run (includes new + retrieved duplicates)
    ingested_results = state.get("ingested_results", [])
    
    if not ingested_results:
        logger.warning("No ingested results found in state, falling back to recent datapoints")
        # Fallback to recent datapoints if no ingested results
        hours = 168
        min_cluster_size = 2
        eps = 0.30
        
        clustering_service.eps = eps
        clustering_service.min_samples = min_cluster_size
        
        clusters = clustering_service.cluster_recent_datapoints(
            hours=hours,
            min_cluster_size=min_cluster_size,
            use_dbscan=True,
            force_recluster=False
        )
    else:
        # Extract datapoint IDs from ingested_results
        datapoint_ids = [dp.id for dp in ingested_results if hasattr(dp, 'id') and dp.id]
        
        if not datapoint_ids:
            logger.warning("No valid datapoint IDs found in ingested_results")
            state["clusters"] = {}
            state["clustering_stats"] = {"clusters_found": 0, "total_datapoints": 0}
            return state
        
        logger.info(f"Clustering {len(datapoint_ids)} datapoints from ingested_results")
        
        # Update clustering service parameters
        min_cluster_size = 2
        eps = 0.30
        clustering_service.eps = eps
        clustering_service.min_samples = min_cluster_size
        
        # Cluster specific datapoints by IDs, including context from recent datapoints
        clusters = clustering_service.cluster_datapoints_by_ids(
            datapoint_ids=datapoint_ids,
            min_cluster_size=min_cluster_size,
            use_dbscan=True,
            include_context=True,  # Include other recent datapoints for better clustering
            context_hours=168  # 7 days of context
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
    storage_service = get_storage_service()
    clusters = state.get("clusters", {})
    
    if not clusters:
        logger.info("No clusters found in state, skipping pattern detection")
        state["pattern_analyses"] = {}
        return state
    
    # Analyze each cluster from state
    analyses = {}
    for cluster_id in clusters.keys():
        try:
            analysis = pattern_service.analyze_cluster(cluster_id)
            analyses[cluster_id] = analysis
        except Exception as e:
            logger.error(f"Error analyzing cluster {cluster_id}: {e}", exc_info=True)
            analyses[cluster_id] = {
                "cluster_id": cluster_id,
                "error": str(e)
            }
    
    logger.info(f"Pattern detection complete: analyzed {len(analyses)} clusters")
    state["pattern_analyses"] = analyses
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


def public_updates_node(state: State) -> State:
    """Generate user-friendly public updates for clusters relevant to the user's query."""
    public_update_service = get_public_update_service()
    storage_service = get_storage_service()
    clusters = state.get("clusters", {})
    ingested_results = state.get("ingested_results", [])
    
    if not clusters:
        state["public_updates"] = []
        return state
    
    # Get IDs of datapoints ingested in this run (relevant to user's query)
    ingested_ids = set()
    if ingested_results:
        for datapoint in ingested_results:
            if hasattr(datapoint, 'id'):
                ingested_ids.add(datapoint.id)
            elif isinstance(datapoint, dict) and 'id' in datapoint:
                ingested_ids.add(datapoint['id'])
    
    # Filter clusters to only those containing datapoints from this run
    relevant_cluster_ids = []
    for cluster_id, cluster_datapoints in clusters.items():
        # Check if any datapoint in this cluster was ingested in this run
        cluster_contains_relevant = False
        for dp in cluster_datapoints:
            dp_id = dp.get("id") or dp.get("_id")
            if dp_id and dp_id in ingested_ids:
                cluster_contains_relevant = True
                break
        
        # Also check by querying the database for this cluster
        if not cluster_contains_relevant:
            try:
                db_cluster_datapoints = storage_service.get_datapoints_by_cluster(cluster_id)
                for db_dp in db_cluster_datapoints:
                    db_dp_id = db_dp.get("_id") or db_dp.get("id")
                    if db_dp_id and db_dp_id in ingested_ids:
                        cluster_contains_relevant = True
                        break
            except Exception as e:
                print(f"Error checking cluster {cluster_id} relevance: {e}")
        
        if cluster_contains_relevant:
            relevant_cluster_ids.append(cluster_id)
    
    # Only generate updates for relevant clusters
    public_updates = []
    for cluster_id in relevant_cluster_ids:
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
graph_builder.add_node("public_updates", public_updates_node)
graph_builder.add_node("echo", echo_node)

# Define the workflow
graph_builder.add_edge(START, "planner")
graph_builder.add_edge("planner", "tavily_search")
graph_builder.add_edge("tavily_search", "ingestion")
graph_builder.add_edge("ingestion", "clustering")
graph_builder.add_edge("clustering", "pattern_detection")
graph_builder.add_edge("pattern_detection", "classification")
graph_builder.add_edge("classification", "public_updates")
graph_builder.add_edge("public_updates", "echo")
graph_builder.add_edge("echo", END)

graph = graph_builder.compile()

