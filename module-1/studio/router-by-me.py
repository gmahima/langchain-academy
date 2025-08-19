import os
import getpass
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState, StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition

def multiply(a: int, b: int) -> int:
    """Multiply two integers and return the result."""
    return a * b

def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")

# Setup OpenAI
_set_env("OPENAI_API_KEY")
chat_model = ChatOpenAI(model="gpt-4o-mini")
chat_model_with_tools = chat_model.bind_tools([multiply])

# LLM Node
def tool_calling_llm(state: MessagesState): 
    return {"messages": chat_model_with_tools.invoke(state["messages"])}

# Build the graph
builder = StateGraph(MessagesState)
builder.add_node("tool_calling_llm", tool_calling_llm)
builder.add_node("tools", ToolNode([multiply]))
builder.add_edge(START, "tool_calling_llm")
builder.add_conditional_edges("tool_calling_llm", tools_condition)
builder.add_edge("tool_calling_llm", END)
builder.add_edge("tools", END)

# Compile the graph
graph = builder.compile()
