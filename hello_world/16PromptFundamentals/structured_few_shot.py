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

Rule:
- Strictly follow the output in JSON format.

Output format:
{{
"Code": "string" or None,
"isCodingQuestion": boolean
}}

Examples:
- User: "What is the capital of France?"
  Assistant: {{"code": null, "isCodingQuestion": false}}
- User: "How do I write a for loop in Python?"
  Assistant: {{"code": "for i in range(10):\n    print(i)", "isCodingQuestion": true}}
"""
response = client.chat.completions.create(
    model="gemini-3.6-flash",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Hey There!"}
    ]
)

print(response.choices[0].message.content)