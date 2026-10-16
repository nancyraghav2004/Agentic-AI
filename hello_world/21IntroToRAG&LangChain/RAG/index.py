from dotenv import load_dotenv

# This File is responsible for indexing the data
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
# from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_qdrant import QdrantVectorStore
import os 


load_dotenv()

pdf_path = Path(__file__).parent / "Eric-Matthes - Python-Crash Course.pdf"

# Load this file in the python program
loader =  PyPDFLoader(file_path=pdf_path)
docs = loader.load()
# print(docs[45])

# Split the doc into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 400 #Overlap is like taking a little/few part from prev chunk with current chunk to understand the background, it's like recap from prev chunk
)

chunks = text_splitter.split_documents(documents=docs)

#As we are using ollama, so we will add this code too, as my system is not that powerful enough
# print("Number of chunks:", len(chunks))
chunks = chunks[:10]
print("Testing with:", len(chunks), "chunks..")
#These lines are to make limited, not whole book chunks


# Vector Embeddings
embeddings = OllamaEmbeddings(
    model="embeddinggemma"
)
# vector_store = embeddings.embed_query(chunks) 
""" (This would directly call the embedding model and turn the text into vectors.But there is a problem: 
embed_query() is meant for one piece of text/query, not your whole list of document chunks.Also, this only 
creates the embeddings in memory. It doesn't create a Qdrant collection or store them in Qdrant."""

# That is why we need this method (using qdrant) , below is the actual RAG approach
#It's like storing vectors into database
# vector_store = QdrantVectorStore.from_documents(
vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embeddings,
    # url="http://localhost:6333",  #this one is if i use server but i am using qdrant cloud
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
    collection_name='learning-rag'
)

print("Indexing of documents done...")