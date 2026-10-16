import os

from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI

google_api_key = os.getenv("google_api_key")
google_base_url = os.getenv("google_base_url")

client = OpenAI(
    api_key=google_api_key,
    base_url=google_base_url
)

response = client.chat.completions.create(
    model="gemini-3.6-flash",
    messages=[
        {"role": "user", "content": "Hey There!"}
    ]
)

print(response.choices[0].message.content)