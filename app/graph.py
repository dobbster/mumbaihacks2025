"""Simple LangGraph agent definition."""

from typing import Annotated
import os
from dotenv import load_dotenv
import requests
from tavily import TavilyClient
from together import Together

from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict

load_dotenv()
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
tavily_client = TavilyClient(TAVILY_API_KEY)
together_client = Together(api_key=TOGETHER_API_KEY)


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
                    "published_at": res.get("published_at"),
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


# Create the graph
graph_builder = StateGraph(State)
graph_builder.add_node("planner", planner_node)
graph_builder.add_node("tavily_search", tavily_search_node)
graph_builder.add_node("echo", echo_node)
graph_builder.add_edge(START, "planner")
graph_builder.add_edge("planner", "tavily_search")
graph_builder.add_edge("tavily_search", "echo")
graph_builder.add_edge("echo", END)

graph = graph_builder.compile()

