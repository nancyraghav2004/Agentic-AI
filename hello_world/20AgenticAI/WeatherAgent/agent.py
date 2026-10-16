# Chain of Thought (CoT) prompting is a technique in natural language processing where a model is guided to generate intermediate reasoning steps before arriving at a final answer. This approach helps the model break down complex problems into smaller, manageable parts, allowing for more accurate and coherent responses. By explicitly prompting the model to think through the problem step-by-step, CoT prompting can improve performance on tasks that require logical reasoning, multi-step calculations, or understanding of intricate relationships between concepts.
# Basically to get human like accuracy, models thinks before responding.

# from dotenv import load_dotenv
# load_dotenv()
# from openai import OpenAI
from ollama import Client
import json
import requests

client = Client(
    host="http://localhost:11434"
)


def get_city(city:str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return(f"The weather in {city} is {response.text}")

    return "Something went wrong"

available_tools = {
     "get_city": get_city
}

# ZERO SHOT PROMPTING
SYSTEM_PROMPT = """
 You are an expert AI Assitant solving user queries using chain of thought.
 You work on START, PLAN and OUTPUT Steps.
 You need to first PLAN what need to be done. The PLAN can be multiple steps.
 Once you think enough PLAN has been done, finally you will OUTPUT the answer to the user query.
 You can also call a tool if required from the list of available tools.
 For every tool call wait for the observe step which is the output from the tool.

 Rules:
 -Strctly follow the given JSON output format:
 -Only run one step at a time.
 -The dequence of steps is START (where user gives an input), a PLAN( that can be of multiple steps) and finally OUTPUT (where you give the final answer to the user query)

 Output JSON format:
{"step": "START"|"PLAN"|"OUTPUT"|"TOOL", "content": "string", "tool": "string", "input": "string"}

Available Tools:
-get_city: Takes city name as an input string and returns the weather information about the city.

Example 1:
 START: "Can you solve 2+3*4+2"
 PLAN: {"step": "PLAN"" "content": "Seems like user is interested in maths problem."}
 PLAN : {"step": "PLAN", "content": "I will first using BODMAS rule"}
 PLAN: {"step": "PLAN", "content": "I will first solve 3*4 = 12"}
 PLAN: {"step": "PLAN", "content": "Then I will add 2+12 = 14"}
 PLAN: {"step": "PLAN", "content": "Finally I will add 14+2 = 16"}
 OUTPUT: {"step": "OUTPUT", "content": "The final answer is 16"}

Example 2:
 START: "What is the weather of Delhi?"
 PLAN: {"step": "PLAN"" "content": "Seems like user is interested in getting weather od Delhi in India"}
 PLAN : {"step": "PLAN", "content": "Let's see if we have any available tool from the list of available tools"}
 PLAN: {"step": "PLAN", "content": "Great, we have get_city tool available for this query."}
 PLAN: {"step": "PLAN", "content": "I need to call get_city tool for Delhi as input for city."}
 PLAN: {"step": "TOOL", "tool": "get_city", "input": "delhi"}
 PLAN: {"step": "OBSERVE", "tool": "get_city", "output": "THe temperature of delhi is cloudy with 20 C"}
 PLAN: {"step": "TOOL", "content": "I got the weather information about Delhi."}
 OUTPUT: {"step": "OUTPUT", "content": "The current weatehr in delhi is 20 C with some cloudy sky"}

"""

print("\n\n\n\n")

message_history = [
    {"role": "system", "content": SYSTEM_PROMPT},
]

# while true, to make things continuous.
while True:
    user_input = input("Enter your query: ")
    message_history.append({"role": "user", "content": user_input})

    while True:
        response = client.chat(
            model="qwen2.5:3b",
            format="json",
            messages=message_history
        )

        raw_result = response.message.content
        message_history.append({"role": "assistant", "content": raw_result})
        try:
            result = json.loads(raw_result)
        except json.JSONDecodeError:
            print("Model returned invalid JSON:", raw_result)
            message_history.append({
                "role": "user",
                "content": "Return only one valid JSON object with step, content, tool, and input fields."
            })
            continue

        if result is None:
            print("Model returned an invalid JSON response:", raw_result)
            message_history.append({
                "role": "user",
                "content": "Return only one valid JSON object using the required format."
            })
            continue

        if result.get("step") == "START":
            print("Started", result.get("content"))
            continue

        if result.get("step") == "TOOL":
            tool_to_call = result.get("tool")
            tool_input = result.get("input")
            print(f"🔧: {tool_to_call} ({tool_input})")

            tool_response = available_tools[tool_to_call](tool_input)
            print(f"🔧: {tool_to_call} ({tool_input}) = {tool_response}")
            message_history.append({"role": "user", "content": json.dumps({
                "step": "OBSERVE", "tool": tool_to_call, "input": tool_input, "output": tool_response
            })})
            continue

        if result.get("step") == "PLAN":
                print("Planning", result.get("content"))
                continue

        if result.get("step") == "OUTPUT":
                print("Output ", result.get("content"))
                break

        message_history.append({
            "role": "user",
            "content": "Continue to the next step and return only the required JSON object."
        })

    print ("\n\n\n\n")