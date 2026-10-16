from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
import os

api_key = os.getenv("api_key")
base_url = os.getenv("base_url")


client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

SYSTEM_PROMPT = """
You should only and only ans the coding related questions. Do not ns anything else. Your name is 
Kia. If user asks something other than coding related questions, you should just say "Sorry" and nothing else.
Examples:
- User: "What is the capital of France?"
  Assistant: "Sorry, I can only answer coding related questions."
- User: "How do I write a for loop in Python?"
  Assistant: "Here's how you write a for loop in Python..."
"""
response = client.chat.completions.create(
    model="gemini-3.6-flash",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Hey There!"}
    ]
)

print(response.choices[0].message.content)

# Few shot prompting is a technique in natural language processing where a model is given a task or question along with a few examples of how to perform that task. The model uses these examples to understand the desired behavior and generate responses accordingly. This approach helps the model learn from limited data and adapt to new tasks more effectively.