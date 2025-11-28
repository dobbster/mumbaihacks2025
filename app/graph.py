"""Simple LangGraph agent definition."""

from typing import Annotated

from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict


class State(TypedDict):
    """State of the agent."""
    messages: Annotated[list, lambda x, y: x + y]


def echo_node(state: State) -> State:
    """Echo the last message."""
    return {"messages": state["messages"]}


# Create the graph
graph_builder = StateGraph(State)
graph_builder.add_node("echo", echo_node)
graph_builder.add_edge(START, "echo")
graph_builder.add_edge("echo", END)

graph = graph_builder.compile()

