# from google import genai

# client = genai.Client(
#     api_key="YOUR_API_KEY"  # Replace with your actual API key

# )

# response = client.models.generate_content(
#     model="gemini-2.5-flash", contents="Explain how AI works in a few words"
# )

# print(response.text)

from dotenv import load_dotenv
 
from google import genai
 
load_dotenv()  # Load environment variables from .env file
 
client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash", contents= "How many wonders are there in the world?"
)
 
print(response.text)