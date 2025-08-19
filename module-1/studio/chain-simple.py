from typing_extensions import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    num: int
    arr: Annotated[list[str], add]  # Using add as reducer for arr

def node_1(state: State) -> State:
    return {"num": 2}

def node_2(state: State) -> State:
    return {"arr": ["bye"]}

# Build graph
builder = StateGraph(State)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)

# Add edges
builder.add_edge(START, "node_1")
builder.add_edge("node_1", "node_2")
builder.add_edge("node_2", END)

# Compile graph
graph = builder.compile()
