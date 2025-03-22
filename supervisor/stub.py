"""This is an automatically generated file. Do not modify it.

This file was generated using `langgraph-gen` version 0.0.6.
To regenerate this file, run `langgraph-gen` with the source `yaml` file as an argument.

Usage:

1. Add the generated file to your project.
2. Create a new agent using the stub.

Below is a sample implementation of the generated stub:

```python
from typing_extensions import TypedDict

from stub import CustomAgent

class SomeState(TypedDict):
    # define your attributes here
    foo: str

# Define stand-alone functions
def Supervisor(state: SomeState) -> dict:
    print("In node: Supervisor")
    return {
        # Add your state update logic here
    }


def RAG(state: SomeState) -> dict:
    print("In node: RAG")
    return {
        # Add your state update logic here
    }


def Websearch(state: SomeState) -> dict:
    print("In node: Websearch")
    return {
        # Add your state update logic here
    }


def conditional_edge_1(state: SomeState) -> str:
    print("In condition: conditional_edge_1")
    raise NotImplementedError("Implement me.")


agent = CustomAgent(
    state_schema=SomeState,
    impl=[
        ("Supervisor", Supervisor),
        ("RAG", RAG),
        ("Websearch", Websearch),
        ("conditional_edge_1", conditional_edge_1),
    ]
)

compiled_agent = agent.compile()

print(compiled_agent.invoke({"foo": "bar"}))
"""

from typing import Callable, Any, Optional, Type

from langgraph.constants import START, END  # noqa: F401
from langgraph.graph import StateGraph


def CustomAgent(
    *,
    state_schema: Optional[Type[Any]] = None,
    config_schema: Optional[Type[Any]] = None,
    input: Optional[Type[Any]] = None,
    output: Optional[Type[Any]] = None,
    impl: list[tuple[str, Callable]],
) -> StateGraph:
    """Create the state graph for CustomAgent."""
    # Declare the state graph
    builder = StateGraph(
        state_schema, config_schema=config_schema, input=input, output=output
    )

    nodes_by_name = {name: imp for name, imp in impl}

    all_names = set(nodes_by_name)

    expected_implementations = {
        "Supervisor",
        "RAG",
        "Websearch",
        "conditional_edge_1",
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
    builder.add_node("Supervisor", nodes_by_name["Supervisor"])
    builder.add_node("RAG", nodes_by_name["RAG"])
    builder.add_node("Websearch", nodes_by_name["Websearch"])

    # Add edges
    builder.add_edge(START, "Supervisor")
    builder.add_edge("RAG", "Supervisor")
    builder.add_edge("Websearch", "Supervisor")
    builder.add_conditional_edges(
        "Supervisor",
        nodes_by_name["conditional_edge_1"],
        [
            "RAG",
            "Websearch",
            END,
        ],
    )
    return builder
