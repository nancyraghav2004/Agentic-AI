from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(
    model="embeddinggemma"
)

vector = embeddings.embed_query("What is Python?")

print("Embedding created!")
print("Vector length:", len(vector))
print("First 5 values:", vector[:5])