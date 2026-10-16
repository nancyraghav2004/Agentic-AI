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

response = client.chat.completions.create(
    model="gemini-3.6-flash",
    messages=[
        {"role": "system", "content": "You are a mathematician that only answers if question is related to maths otherwise you will say 'Sorry'"},
        {"role": "user", "content": "Hey There!"}
    ]
)

print(response.choices[0].message.content)

# Zero shot prompting is a technique in natural language processing where a model is given a task or question without any prior examples or training on that specific task. The model is expected to generate a response based solely on its pre-existing knowledge and understanding of language. This approach tests the model's ability to generalize and apply its knowledge to new, unseen situations.
#{"role": "system", "content": "You are a mathematician that only answers if question is related to maths otherwise you will say 'Sorry'"},


