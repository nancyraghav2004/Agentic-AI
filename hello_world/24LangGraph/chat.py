from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END

# First we create a state
class State(TypedDict):
    # In state we can literally have anything, x as a key, input anything
    messages: Annotated[list, add_messages]
    #add_message is like always keep adding something to the annotation

def chatbot(state: State):
    print("\n\nInside chatbot node", state)
    return {"messages": ["Hi, This is the message from ChatBot Node"] }

def samplenode(state: State):
    print("\n\nInside samplenode node", state)
    return {"messages": ["Sample Message Appended"] }

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("samplenode", samplenode)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "samplenode")
graph_builder.add_edge("samplenode", END)
# START -> chatbot -> samplenode -> END

graph = graph_builder.compile()

updated_state = graph.invoke(State({"messages": "Hi, My name is Nancy Raghav"})) # When we invoke, we have to pass the initial state
print("\n\nupdated_state", updated_state)

# State = { messages: ["Hey, there"]}
# node runs: chatbot(state: ["Hey there"]) -> ["Hi, This is the message from chatbot"]
# state = { "messages": ["Hey Ther (original one)", "Hi, This is the message from chatbot Node (appended one)"]}