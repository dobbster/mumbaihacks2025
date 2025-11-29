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
    get_storage_service,
    get_vectorization_service
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


def generate_topic_representation(cluster_datapoints: List[Dict[str, Any]]) -> str:
    """
    Generate a concise topic representation for a cluster based on its datapoints.
    
    Args:
        cluster_datapoints: List of datapoint documents in the cluster
        
    Returns:
        Concise topic representation string
    """
    if not cluster_datapoints:
        return "Unknown topic"
    
    # Extract titles and first sentences from content
    titles = []
    keywords = []
    
    for dp in cluster_datapoints[:5]:  # Use first 5 datapoints
        title = dp.get("title", "").strip()
        if title:
            titles.append(title)
        
        content = dp.get("content", "").strip()
        if content:
            # Get first sentence
            first_sentence = content.split('.')[0].strip()
            if len(first_sentence) > 20:
                keywords.append(first_sentence[:100])  # Limit length
    
    # Combine titles and keywords
    all_text = " ".join(titles + keywords)
    
    # Extract common keywords (simple approach)
    words = all_text.lower().split()
    # Filter common stop words
    stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "do", "does", "did", "will", "would", "should", "could", "may", "might", "must", "can"}
    meaningful_words = [w for w in words if len(w) > 3 and w not in stop_words]
    
    # Count word frequency
    from collections import Counter
    word_freq = Counter(meaningful_words)
    top_words = [word for word, count in word_freq.most_common(5)]
    
    # Create topic representation
    if top_words:
        topic = " ".join(top_words).title()
        # Add context from first title if available
        if titles:
            first_title_words = titles[0].split()[:3]
            topic = f"{' '.join(first_title_words)} - {topic}"
        return topic[:150]  # Limit length
    
    # Fallback to first title
    if titles:
        return titles[0][:150]
    
    return "Uncategorized topic"


def filter_clusters_by_relevance(
    clusters: Dict[str, Any],
    user_prompt: str,
    vectorization_service: VectorizationService,
    similarity_threshold: float = 0.5
) -> Dict[str, Any]:
    """
    Filter clusters to only include those relevant to the user's prompt.
    
    Args:
        clusters: Dictionary of clusters with topic_representations
        user_prompt: User's original query/prompt
        vectorization_service: Service for generating embeddings
        similarity_threshold: Minimum cosine similarity to be considered relevant
        
    Returns:
        Filtered clusters dictionary
    """
    if not clusters or not user_prompt:
        return clusters
    
    # Generate embedding for user prompt
    try:
        prompt_embedding = vectorization_service.generate_embedding(user_prompt.lower())
    except Exception as e:
        logger.warning(f"Failed to generate embedding for prompt, returning all clusters: {e}")
        return clusters
    
    # Calculate cosine similarity
    import numpy as np
    
    def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return float(dot_product / (norm1 * norm2))
    
    filtered_clusters = {}
    
    for cluster_id, cluster_data in clusters.items():
        # Get topic_representation from cluster metadata
        if isinstance(cluster_data, dict) and "topic_representation" in cluster_data:
            topic_repr = cluster_data["topic_representation"]
        elif isinstance(cluster_data, list) and len(cluster_data) > 0:
            # Generate topic representation from datapoints if not present
            topic_repr = generate_topic_representation(cluster_data)
        else:
            continue
        
        # Generate embedding for topic representation
        try:
            topic_embedding = vectorization_service.generate_embedding(topic_repr.lower())
            similarity = cosine_similarity(prompt_embedding, topic_embedding)
            
            if similarity >= similarity_threshold:
                # Add similarity score to cluster metadata
                if isinstance(cluster_data, dict):
                    cluster_data["relevance_score"] = similarity
                    filtered_clusters[cluster_id] = cluster_data
                else:
                    # Wrap in dict if it's a list
                    filtered_clusters[cluster_id] = {
                        "datapoints": cluster_data,
                        "topic_representation": topic_repr,
                        "relevance_score": similarity
                    }
                logger.info(f"Cluster {cluster_id} is relevant (similarity: {similarity:.3f}, topic: {topic_repr})")
            else:
                logger.debug(f"Cluster {cluster_id} filtered out (similarity: {similarity:.3f} < {similarity_threshold}, topic: {topic_repr})")
        except Exception as e:
            logger.warning(f"Failed to check relevance for cluster {cluster_id}: {e}")
            # Include cluster if relevance check fails (fail open)
            filtered_clusters[cluster_id] = cluster_data
    
    logger.info(f"Filtered clusters: {len(filtered_clusters)}/{len(clusters)} relevant to prompt")
    return filtered_clusters


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
    
    # Convert clusters to serializable format and add topic_representation
    vectorization_service = get_vectorization_service()
    clusters_dict = {}
    for cluster_id, datapoints in clusters.items():
        # Generate topic representation for this cluster
        topic_repr = generate_topic_representation(datapoints)
        
        clusters_dict[cluster_id] = {
            "topic_representation": topic_repr,
            "datapoints": [
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
        }
    
    # Filter clusters by relevance to user prompt
    user_prompt = state.get("messages", [""])[-1] if state.get("messages") else ""
    if user_prompt:
        clusters_dict = filter_clusters_by_relevance(
            clusters_dict,
            user_prompt,
            vectorization_service,
            similarity_threshold=0.5
        )
    
    state["clusters"] = clusters_dict
    state["clustering_stats"] = {
        "clusters_found": len(clusters),
        "total_datapoints": stats.get("total_datapoints", 0),
        "statistics": stats
    }
    return state


def pattern_detection_node(state: State) -> State:
    """Analyze clusters for misinformation patterns - only on the most relevant cluster."""
    pattern_service = get_pattern_detection_service()
    storage_service = get_storage_service()
    clusters = state.get("clusters", {})
    
    if not clusters:
        logger.info("No clusters found in state, skipping pattern detection")
        state["pattern_analyses"] = {}
        return state
    
    # Find the most relevant cluster (highest relevance_score)
    most_relevant_cluster_id = None
    highest_relevance = -1.0
    
    for cluster_id, cluster_data in clusters.items():
        if isinstance(cluster_data, dict):
            relevance_score = cluster_data.get("relevance_score", 0.0)
            if relevance_score > highest_relevance:
                highest_relevance = relevance_score
                most_relevant_cluster_id = cluster_id
    
    # If no relevance_score found, use the first cluster
    if most_relevant_cluster_id is None:
        most_relevant_cluster_id = list(clusters.keys())[0] if clusters else None
    
    if most_relevant_cluster_id is None:
        logger.warning("No cluster found for pattern detection")
        state["pattern_analyses"] = {}
        return state
    
    # Analyze only the most relevant cluster
    cluster_data = clusters[most_relevant_cluster_id]
    topic_repr = "Unknown"
    if isinstance(cluster_data, dict):
        topic_repr = cluster_data.get("topic_representation", "Unknown")
    
    logger.info(f"Analyzing most relevant cluster {most_relevant_cluster_id} (topic: {topic_repr}, relevance: {highest_relevance:.3f})")
    
    analyses = {}
    try:
        analysis = pattern_service.analyze_cluster(most_relevant_cluster_id)
        analyses[most_relevant_cluster_id] = analysis
    except Exception as e:
        logger.error(f"Error analyzing cluster {most_relevant_cluster_id}: {e}", exc_info=True)
        analyses[most_relevant_cluster_id] = {
            "cluster_id": most_relevant_cluster_id,
            "error": str(e)
        }
    
    logger.info(f"Pattern detection complete: analyzed 1 most relevant cluster")
    state["pattern_analyses"] = analyses
    return state


def classification_node(state: State) -> State:
    """Classify the most relevant cluster as misinformation, legitimate, or uncertain."""
    classification_service = get_classification_service()
    pattern_service = get_pattern_detection_service()
    storage_service = get_storage_service()
    
    clusters = state.get("clusters", {})
    pattern_analyses = state.get("pattern_analyses", {})
    
    if not clusters:
        state["classifications"] = {}
        return state
    
    # Find the most relevant cluster (should match the one analyzed in pattern_detection_node)
    # Use the cluster that has pattern analysis (from pattern_detection_node)
    most_relevant_cluster_id = None
    
    if pattern_analyses:
        # Use the cluster that was analyzed in pattern_detection_node
        most_relevant_cluster_id = list(pattern_analyses.keys())[0]
    else:
        # Fallback: find cluster with highest relevance_score
        highest_relevance = -1.0
        for cluster_id, cluster_data in clusters.items():
            if isinstance(cluster_data, dict):
                relevance_score = cluster_data.get("relevance_score", 0.0)
                if relevance_score > highest_relevance:
                    highest_relevance = relevance_score
                    most_relevant_cluster_id = cluster_id
        
        # If no relevance_score found, use the first cluster
        if most_relevant_cluster_id is None:
            most_relevant_cluster_id = list(clusters.keys())[0] if clusters else None
    
    if most_relevant_cluster_id is None:
        logger.warning("No cluster found for classification")
        state["classifications"] = {}
        return state
    
    # Classify only the most relevant cluster
    classifications = {}
    try:
        # Get cluster datapoints
        all_cluster_datapoints = storage_service.get_datapoints_by_cluster(most_relevant_cluster_id)
        
        if not all_cluster_datapoints:
            logger.warning(f"No datapoints found for cluster {most_relevant_cluster_id}")
            state["classifications"] = {}
            return state
        
        # Filter to only include datapoints from the current ingestion run
        # This ensures sources are only from datapoints relevant to the user's query
        ingested_results = state.get("ingested_results", [])
        ingested_ids = {dp.id for dp in ingested_results if hasattr(dp, 'id') and dp.id}
        
        # Filter cluster datapoints to only those from current ingestion
        relevant_cluster_datapoints = []
        for dp in all_cluster_datapoints:
            dp_id = dp.get("_id") or dp.get("id")
            if dp_id in ingested_ids:
                relevant_cluster_datapoints.append(dp)
        
        if not relevant_cluster_datapoints:
            logger.warning(f"No relevant datapoints found in cluster {most_relevant_cluster_id} from current ingestion")
            # Fallback to all cluster datapoints if no matches
            relevant_cluster_datapoints = all_cluster_datapoints
        else:
            logger.info(f"Filtered cluster datapoints: {len(relevant_cluster_datapoints)}/{len(all_cluster_datapoints)} from current ingestion")
        
        # Get pattern analysis for this cluster (should already exist from pattern_detection_node)
        pattern_analysis = pattern_analyses.get(most_relevant_cluster_id)
        if not pattern_analysis:
            # Run pattern detection if not already done
            logger.warning(f"Pattern analysis not found for {most_relevant_cluster_id}, running pattern detection")
            pattern_analysis = pattern_service.analyze_cluster(most_relevant_cluster_id)
        
        # Classify the cluster (pattern_analysis is required)
        # Pass only relevant datapoints for source extraction
        classification_result = classification_service.classify_cluster(
            cluster_id=most_relevant_cluster_id,
            pattern_analysis=pattern_analysis,
            cluster_datapoints=relevant_cluster_datapoints  # Only datapoints from current ingestion
        )
        
        classifications[most_relevant_cluster_id] = classification_result.model_dump() if hasattr(classification_result, 'model_dump') else classification_result
        
        logger.info(f"Classification complete for most relevant cluster: {most_relevant_cluster_id}")
        
    except Exception as e:
        logger.error(f"Error classifying cluster {most_relevant_cluster_id}: {e}", exc_info=True)
    
    state["classifications"] = classifications
    return state


# Create the graph
graph_builder = StateGraph(State)
graph_builder.add_node("planner", planner_node)
graph_builder.add_node("tavily_search", tavily_search_node)
graph_builder.add_node("ingestion", ingestion_node)
graph_builder.add_node("clustering", clustering_node)
graph_builder.add_node("pattern_detection", pattern_detection_node)
graph_builder.add_node("classification", classification_node)

# Define the workflow
graph_builder.add_edge(START, "planner")
graph_builder.add_edge("planner", "tavily_search")
graph_builder.add_edge("tavily_search", "ingestion")
graph_builder.add_edge("ingestion", "clustering")
graph_builder.add_edge("clustering", "pattern_detection")
graph_builder.add_edge("pattern_detection", "classification")
graph_builder.add_edge("classification", END)

graph = graph_builder.compile()

