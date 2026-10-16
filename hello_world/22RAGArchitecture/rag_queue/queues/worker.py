from openai import OpenAI
from pathlib import Path
from ollama import Client
from langchain_qdrant import QdrantVectorStore
from langchain_ollama import OllamaEmbeddings
import os
from dotenv import load_dotenv


env_path = Path(__file__).resolve().parents[3] / ".env"
load_dotenv(env_path)

client = Client(
    host="http://localhost:11434"
)

# Vector Embeddings
embeddings = OllamaEmbeddings(
    model="embeddinggemma"
)

print("QDRANT URL:", os.getenv("QDRANT_URL"))
print("QDRANT KEY EXISTS:", bool(os.getenv("QDRANT_API_KEY")))

vector_db = QdrantVectorStore.from_existing_collection(
    url=os.getenv("QDRANT_URL"),
    port=443,
    api_key=os.getenv("QDRANT_API_KEY"),
    collection_name='learning-rag',
    embedding=embeddings,
    check_compatibility=False
)

def process_query(query:str):
    print("Searching Chunks", query)
    search_results = vector_db.similarity_search(query=query)

    context = "\n\n\n".join([f"Page Content: {result.page_content}\nPage Number: {result.metadata['page_label']}\nFile Location: {result.metadata['source']}" for result in search_results])    

    SYSTEM_PROMPT = f"""
    You are an helpful AI assistant who answers user query based on the available context retreived from a 
    pdf file along with page_contents and page number.

    You should only anser the user based on the following context and navigate the user to open the right 
    page number to know more.

    Context:
    {context}
    """

    response = client.chat(
            model="qwen2.5:3b",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": query}
            ]
    )

    print(f"🤖: {response.message.content}")
    return response.message.content