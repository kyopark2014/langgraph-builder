"""This file was generated using `langgraph-gen` version 0.0.3.

This file provides a placeholder implementation for the corresponding stub.

Replace the placeholder implementation with your own logic.
"""

from typing_extensions import TypedDict

from stub import CustomAgent


class SomeState(TypedDict):
    # define your attributes here
    foo: str


# Define stand-alone functions
def retrieve(state: SomeState) -> dict:
    print("In node: retrieve")
    return {
        # Add your state update logic here
    }


def grade_documents(state: SomeState) -> dict:
    print("In node: grade_documents")
    return {
        # Add your state update logic here
    }


def generate(state: SomeState) -> dict:
    print("In node: generate")
    return {
        # Add your state update logic here
    }


def rewrite(state: SomeState) -> dict:
    print("In node: rewrite")
    return {
        # Add your state update logic here
    }


def websearch(state: SomeState) -> dict:
    print("In node: websearch")
    return {
        # Add your state update logic here
    }


def conditional_edge_1(state: SomeState) -> str:
    print("In condition: conditional_edge_1")
    raise NotImplementedError("Implement me.")


agent = CustomAgent(
    state_schema=SomeState,
    impl=[
        ("retrieve", retrieve),
        ("grade_documents", grade_documents),
        ("generate", generate),
        ("rewrite", rewrite),
        ("websearch", websearch),
        ("conditional_edge_1", conditional_edge_1),
    ],
)

compiled_agent = agent.compile()

# print(compiled_agent.invoke({"foo": "bar"}))
