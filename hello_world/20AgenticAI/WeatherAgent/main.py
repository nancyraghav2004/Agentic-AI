# from openai import OpenAI
from ollama import Client
# from dotenv import load_dotenv
import requests

# load_dotenv()

client = Client(
    host="http://localhost:11434"
)


# Code for OpenAI
# def main():
#     user_query = input("> ")
#     response = client.chat.completions.create(
#         model="llama3.2",
#         messages=[
#             {"role": "user", "content": user_query}
#         ]
#     )

#     print(f"🤖: {response.choices[0].message.content}")

#main()


# Code for OpenSource
# client = Client(
#     host="http://localhost:11434"
# )

def get_city(city:str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return(f"The weather in {city} is {response.text}")

    return "Something went wrong"


def main():
    user_query = input("> ")
    response = client.chat(model="tinyllama", messages=[
        {"role": "user", "content": user_query}
    ])

    print(f"🤖: {response.message.content}")

# main()

print(get_city("Delhi"))

# Pre-trained data can not give you current weather, so for that, we need weather api
# FOr that the url is - https://wttr.in/{city}?format=%C+%t
