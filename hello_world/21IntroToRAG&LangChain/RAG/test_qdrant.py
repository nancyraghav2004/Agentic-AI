# from qdrant_client import QdrantClient

# client = QdrantClient(path="./qdrant_data") # This is for ocally only, docker-compose.yml will start an actual Qdrant server, but as we are not using docker

# print("Qdrant is working!")

# client.close()


# Local is store Qdrant on my computer.
# What we are doing is - connect my Python program to my Qdrant Cloud database.


#Means your Python app is talking to Qdrant Cloud successfully. But still it is not connected to server, it is qdrant cloud
import os
from qdrant_client import QdrantClient
from dotenv import load_dotenv

load_dotenv()

client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

print(client.get_collections())

# The normal Qdrant development setup is Docker. Qdrant officially recommends Docker for local 
# development/testing, and localhost:6333/dashboard is the Web UI for that setup.


# There are two different things:
# QdrantClient(path="./qdrant_data") → embedded/local storage, not a Qdrant server
# Qdrant Server → actual service listening on port 6333, with REST API + dashboard.
