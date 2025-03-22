"""This file was generated using `langgraph-gen` version 0.0.6.

This file provides a placeholder implementation for the corresponding stub.

Replace the placeholder implementation with your own logic.
"""

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
    ],
)

compiled_agent = agent.compile()

print(compiled_agent.invoke({"foo": "bar"}))
