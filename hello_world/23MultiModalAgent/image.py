import requests
from ollama import Client

client = Client(host="http://localhost:11434")
# AS ollama directly can not use/pick link, so we tried another way to work this code.
image_url = "https://images.pexels.com/photos/39320552/pexels-photo-39320552.jpeg"
image_data = requests.get(image_url, timeout=30)
image_data.raise_for_status()

response = client.chat(
    model="minicpm-v4.6:1b",
    messages=[
        {
            "role": "user",
            "content": "Generate a caption for this image in about 50 words.",
            "images": [image_data.content]
        }
    ]
)

print(response.message.content)