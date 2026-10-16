from fastapi import FastAPI, Body
from ollama import Client

app = FastAPI()
client = Client(
    host="http://localhost:11434"
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/contact-us")
def read_item():
    return {"email": "example@gmail.com"}

@app.post("/chat")
def chat(message: str=Body(..., description="The Message")):
    response = client.chat(model="tinyllama", messages=[
        {"role": "user", "content":message}
    ])
    return { "response": response.message.content }