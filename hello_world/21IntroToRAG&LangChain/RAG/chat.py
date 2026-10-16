# Retrieval Phase
from dotenv import load_dotenv
from langchain_ollama import OllamaEmbeddings
from langchain_qdrant import QdrantVectorStore
from ollama import Client
import os

load_dotenv()

# Vector Embeddings
embeddings = OllamaEmbeddings(
    model="embeddinggemma"
)

vector_db = QdrantVectorStore.from_existing_collection(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
    collection_name='learning-rag',
    embedding=embeddings
)

#Take the user input
user_query = input("Ask something: ")

#Relevant chunks (search_result will return those relevant chunks)
search_results = vector_db.similarity_search(query=user_query)

context = "\n\n\n".join([f"Page Content: {result.page_content}\nPage Number: {result.metadata['page_label']}\nFile Location: {result.metadata['source']}" for result in search_results])

SYSTEM_PROMPT = f"""
 You are an helpful AI assistant who answers user query based on the available context retreived from a 
 pdf file along with page_contents and page number.

 You should only anser the user based on the following context and navigate the user to open the right 
 page number to know more.

 Context:
 {context}
"""
client = Client(
    host="http://localhost:11434"
)

response = client.chat(
            model="qwen2.5:3b",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": SYSTEM_PROMPT}
            ]
        )

print(f"🤖: {response.message.content}")