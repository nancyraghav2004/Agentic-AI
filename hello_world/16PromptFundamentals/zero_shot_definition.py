import os

from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI

api_key = os.getenv("api_key")
base_url = os.getenv("base_url")

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

# ZERO SHOT PROMPTING
SYSTEM_PROMPT = """
You are a mathematician that only answers if question is related to maths otherwise you will say 'Sorry'
"""

response = client.chat.completions.create(
    model="gemini-3.6-flash",
    messages=[
        {"role": "system", "content": "You are a mathematician that only answers if question is related to maths otherwise you will say 'Sorry'"},
        {"role": "user", "content": "Hey There!"}
    ]
)

print(response.choices[0].message.content)

# Zero shot prompting is The model is given a direct question or task without prior examples.