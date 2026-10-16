from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
#instead of init_chat_model we can also uuse openai's openai.chat.completion (if we are using openai key)

#We just made a little change here for llm and in chatbot node code (as compare to chatbot)
llm = init_chat_model(
    model="qwen2.5:3b ",
    model_provider= "ollama"
)

# First we create a state
class State(TypedDict):
    # In state we can literally have anything, x as a key, input anything
    messages: Annotated[list, add_messages]
    #add_message is like always keep adding something to the annotation

def chatbot(state: State):
    response = llm.invoke(state.get("messages"))
    return {"messages": [response] }

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

updated_state = graph.invoke(State({"messages": "Hi, My name is Nancy Raghav"}))
print("\n\nupdated_state", updated_state)
