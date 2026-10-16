from typing_extensions import TypedDict
from typing import Optional, Literal
from langgraph.graph import StateGraph, START, END
from ollama import Client

client = Client(host="http://localhost:11434")

class State(TypedDict):
    user_query: str
    llm_output: Optional[str]
    is_good: Optional[bool]

def chatbot(state: State):
    print("Chatbot Node", state)
    response = client.chat(
        model="qwen2.5:3b",
        messages=[
            {"role": "user", "content": state.get("user_query")} #2.Read that state
        ]
    )

    state["llm_output"] = response.message.content #4.Update your state
    return state #5.Return the state

def evaluate_response(state: State)-> Literal["chatbot_tinyllama", "endnode"]: # Literal is we are telling that if response is good then go to end node otherwise go to chatbot_tinyllama
    #For now, let's assume evaluation is good (i.e., response is good)
    print("Evaluate_response Node", state)
    #if False:
    if True:
        return "endnode" # we return the node id where we want to redirect

    return "chatbot_tinyllama" # else, return where do we want to redirect

def chatbot_tinyllama(state: State):
    print("Chatbot_tinyllama Node", state)
    response = client.chat(
            model="tinyllama:latest",
            messages=[
                {"role": "user", "content": state.get("user_query")}
            ]
        )
    
    state["llm_output"] = response.message.content
    return state

def endnode(state: State):
    print("Endnode Node", state)
    return state

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("chatbot_tinyllama", chatbot_tinyllama)
graph_builder.add_node("endnode", endnode)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", evaluate_response)

graph_builder.add_edge("chatbot_tinyllama", "endnode")
graph_builder.add_edge("endnode", END)

graph = graph_builder.compile()

updated_state = graph.invoke(State({"user_query": "Hey, what is 2+2?"}))
print(updated_state)