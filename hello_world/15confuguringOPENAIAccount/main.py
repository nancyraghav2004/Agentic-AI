from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role": "user", "content": "Hello There!"}
    ]
)

print(response.choices[0].message.content)