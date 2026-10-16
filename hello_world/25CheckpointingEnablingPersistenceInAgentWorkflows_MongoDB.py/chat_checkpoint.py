from pathlib import Path
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.mongodb import MongoDBSaver

env_path = Path(__file__).resolve().parents[1]/ ".env"
load_dotenv(env_path, override=True)

MONGODB_URI = os.getenv("MONGODB_URI")
print("URI loaded:", bool(MONGODB_URI))
print("URI starts with:", MONGODB_URI[:20] if MONGODB_URI else None)

llm = init_chat_model(
    model="qwen2.5:3b",
    model_provider= "ollama"
)

class State(TypedDict):
    messages: Annotated[list, add_messages]

def chatbot(state: State):
    response = llm.invoke(state.get("messages"))
    return {"messages": [response] }

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

# graph = graph_builder.compile()

#Create thread configuration
config = {
    "configurable": {
        "thread_id": "nancy" #If I change thread_id, like instead of nancy i use naina, then I will forget whatever it learned in nancy about me.
    }
}

#Method which I learned (but suitable for docker and for paid llm)
# def compile_graph_with_checkpointer():
#     DB_URL = "localhost:27017" #local MongoDB server.
#     with MongoDBSaver.from_conn_string(DB_URL) as checkpointer: 
#         graph = graph_builder.compile(checkpointer=checkpointer)
#     return graph 

# graph_with_checkpointer = compile_graph_with_checkpointer()

# config = {
#     "configurable":{
#         "thread_id": "nancy"
#     }
# }

def compile_graph_with_checkpointer():
    #Connect to MongoDB Atlas
    mongo_client = MongoClient(MONGODB_URI)
    mongo_client.admin.command("ping")
    print("MongoDB connection successful!")
    #Create MongoDB Checkpointer
    checkpointer = MongoDBSaver(
        mongo_client,
        "langgraph_db"
    )
    #Compile graph WITH checkpointer
    graph = graph_builder.compile(
        checkpointer=checkpointer
    )
    return graph

graph_with_checkpointer = compile_graph_with_checkpointer()

#As we get output like very messy, so to make that readable, we will use below code
# updated_state = graph_with_checkpointer.invoke(
#     State({"messages": [
#         ("user", "Hey, What is my name?")]}), # this msg will be stoered under nancy
#     config,) # When we invoke, we have to pass the initial state
# print("\n\nupdated_state", updated_state)

for chunk in graph_with_checkpointer.stream(
    State({"messages": ["In which company do I work?"]}),
    config,
    stream_mode="values"
):
    chunk["messages"][-1].pretty_print()

# we do configuration, because state is not global, state s actually scoped to the thread id.
