# Chain of Thought (CoT) prompting is a technique in natural language processing where a model is guided to generate intermediate reasoning steps before arriving at a final answer. This approach helps the model break down complex problems into smaller, manageable parts, allowing for more accurate and coherent responses. By explicitly prompting the model to think through the problem step-by-step, CoT prompting can improve performance on tasks that require logical reasoning, multi-step calculations, or understanding of intricate relationships between concepts.
# Basically to get human like accuracy, models thinks before responding.

import os

from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
import json

api_key = os.getenv("api_key")
base_url = os.getenv("base_url")

client = OpenAI(
    api_key=api_key,
    base_url=base_url

)

# ZERO SHOT PROMPTING
SYSTEM_PROMPT = """
 You are an expert AI Assitant solving user queries using chain of thought.
 You work on START, PLAN and OUTPUT Steps.
 You need to first PLAN what need to be done. The PLAN can be multiple steps.
 Once you think enough PLAN has been done, finally you will OUTPUT the answer to the user query.

 Rules:
 -Strctly follow the given JSON output format:
 -Only run one step at a time.
 -The dequence of steps is START (where user gives an input), a PLAN( that can be of multiple steps) and finally OUTPUT (where you give the final answer to the user query)

 Output JSON format:
{"step": "START"|"PLAN"|"OUTPUT", "content": "string"}

Example:
 START: "Can you solve 2+3*4+2"
 PLAN: {"step": "PLAN"" "content": "Seems like user is interested in maths problem."}
 PLAN : {"step": "PLAN", "content": "I will first using BODMAS rule"}
 PLAN: {"step": "PLAN", "content": "I will first solve 3*4 = 12"}
 PLAN: {"step": "PLAN", "content": "Then I will add 2+12 = 14"}
 PLAN: {"step": "PLAN", "content": "Finally I will add 14+2 = 16"}
 OUTPUT: {"step": "OUTPUT", "content": "The final answer is 16"}
"""

print("\n\n\n\n")

message_history = [
    {"role": "system", "content": SYSTEM_PROMPT},
]

user_input = input("Enter your query: ")

message_history.append({"role": "assistant", "content": user_input})

while True:
    response = client.chat.completions.create(
        model="gemini-3.6-flash",
        response_format={"type": "json_object"},
        messages=message_history
    )

    raw_result = response.choices[0].message.content
    message_history.append({"role": "assistant", "content": raw_result})
    result = json.loads(raw_result)

    if result.get("step") == "START":
        print("Started", result.get("content"))
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