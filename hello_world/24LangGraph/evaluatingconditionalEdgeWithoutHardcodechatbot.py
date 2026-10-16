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
            {"role": "user", "content": state.get("user_query")} 
        ]
    )

    state["llm_output"] = response.message.content 
    return state

# We were using hard coded here using True and False, in conditionalEdgeChatbot.py file, now we will see how to make it real evaluator
# def evaluate_response(state: State)-> Literal["chatbot_tinyllama", "endnode"]: 
#     print("Evaluate_response Node", state)
#     if True:
#         return "endnode" 

#     return "chatbot_tinyllama" 

def evaluate_response(state: State)-> Literal["chatbot_tinyllama", "endnode"]: 
    print("Evaluating response...")
    evaluation_prompt = f"""
        You are an evaluator.
        User question: {state["user_query"]}
        AI answer: {state["llm_output"]}
        Evaluate whether the AI answer correctly and adequetely answers the user's question.
         Reply with ONLY:
         GOOD or BAD
"""
    response = client.chat(
        model = "qwen2.5:3b",
        messages=[
            {"role": "user", "content": evaluation_prompt}
        ]
    )
    evaluation = response.message.content.strip().upper()

    print("Evaluation:", evaluation)

    if evaluation == "GOOD":
        return "endnode"
    return "chatbot_tinyllama"

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