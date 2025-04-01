from typing import Callable, Any, Optional, Type

from langgraph.constants import START, END  # noqa: F401
from langgraph.graph import StateGraph

def Agent(
    *,
    state_schema: Optional[Type[Any]] = None,
    config_schema: Optional[Type[Any]] = None,
    input: Optional[Type[Any]] = None,
    output: Optional[Type[Any]] = None,
    impl: list[tuple[str, Callable]],
) -> StateGraph:
    """Create the state graph for Agent."""
    # Declare the state graph
    builder = StateGraph(
        state_schema, config_schema=config_schema, input=input, output=output
    )

    nodes_by_name = {name: imp for name, imp in impl}

    all_names = set(nodes_by_name)

    expected_implementations = {
        "retrieve",
        "grade_documents",
        "generate",
        "rewrite",
        "websearch",
        "decide_to_generate",
    }

    missing_nodes = expected_implementations - all_names
    if missing_nodes:
        raise ValueError(f"Missing implementations for: {missing_nodes}")

    extra_nodes = all_names - expected_implementations

    if extra_nodes:
        raise ValueError(
            f"Extra implementations for: {extra_nodes}. Please regenerate the stub."
        )

    # Add nodes
    builder.add_node("retrieve", nodes_by_name["retrieve"])
    builder.add_node("grade_documents", nodes_by_name["grade_documents"])
    builder.add_node("generate", nodes_by_name["generate"])
    builder.add_node("rewrite", nodes_by_name["rewrite"])
    builder.add_node("websearch", nodes_by_name["websearch"])

    # Add edges
    builder.add_edge(START, "retrieve")
    builder.add_edge("generate", END)
    builder.add_edge("retrieve", "grade_documents")
    builder.add_edge("rewrite", "websearch")
    builder.add_edge("websearch", "generate")
    builder.add_conditional_edges(
        "grade_documents",
        nodes_by_name["decide_to_generate"],
        [
            "generate",
            "rewrite",
        ],
    )
    return builder
