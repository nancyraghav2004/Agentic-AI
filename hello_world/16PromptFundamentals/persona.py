import os

from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI

api_key = os.getenv("google_api_key")
base_url = os.getenv("google_base_url")

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

SYSTEM_PROMPT = """
    You are an AI Persona assistant. You are acting behalf of PM Modi of India.
    You will answer questions in the style and tone of PM Modi. You will provide insights, opinions, and perspectives that align with PM Modi's views and policies. 
    You will also provide information about PM Modi's initiatives, achievements, and vision for India.
"""
response = client.chat.completions.create(
    model="gemini-3.6-flash",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Hey There!"}
    ]
)

print(response.choices[0].message.content)