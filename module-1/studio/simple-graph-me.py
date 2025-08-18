import random 
from typing import Literal
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

# State
class State(TypedDict):
    graph_state: str

def node_1(state):
    print("** node_1 **")
    return {"graph_state": state["graph_state"] + " I like "} 

def node_2(state): 
    print("** node_2 **")
    return {"graph_state": state["graph_state"] + "Apples"}

def node_3(state): 
    print("** node_3 **")
    return {"graph_state": state["graph_state"] + "Oranges"} 

def decide_fruit(state) -> Literal["node_2", "node_3"]:
    user_input = state["graph_state"]
    if random.random() < 0.5: 
        return "node_2"
    return "node_3"

# Build graph
builder = StateGraph(State)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)

# Logic
builder.add_edge(START, "node_1")
builder.add_conditional_edges("node_1", decide_fruit)
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)

# Compile graph
graph = builder.compile()
