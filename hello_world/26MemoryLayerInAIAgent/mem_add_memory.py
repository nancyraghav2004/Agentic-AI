# Now basically, we are adding few more like chatting and then storing it, so adding few lines of code in mem.py code
from pathlib import Path
from dotenv import load_dotenv
from mem0 import Memory
import os
from ollama import Client
import json

env_path = Path(__file__).resolve().parents[1]/ ".env"
load_dotenv(env_path, override=True)

client = Client(
    host="http://localhost:11434"
)


config = {
    "version": "v1.1",
    "llm": {
        "provider": "ollama",
        "config": { 
                   "model": "qwen2.5:3b",
                    "ollama_base_url": "http://localhost:11434",
                     "temperature": 0
            }
    },
    "embedder": {
        "provider": "ollama",
        "config": {
            "model": "embeddinggemma:latest", 
            "ollama_base_url": "http://localhost:11434"
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "url": "QDRANT_URL",
            "api_key": "QDRANT_API_KEY",
            "collection_name": "mem0_memories",
            "embedding_model_dims": 768
        }
    }
}

mem_client = Memory.from_config(config)


# for continue conversation 
while True:
    user_query = input("> ")

    # To retrieve saved memory
    search_memory = mem_client.search( # IT will find only relevant memory
        #user_id="nancy_raghav",
        filters={"user_id": "nancy_raghav"},
        query=user_query
    )

    memories = [
        f"ID: {mem.get("id")}\nMemory: {mem.get("memory")}" 
        for mem in search_memory.get("results", [])
    ]

    print("Found memories:", memories)

    SYSTEM_PROMPT = f"""
    Here is the context about the user:
    {json.dumps(memories)}
    """

    response = client.chat(model="qwen2.5:3b", messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_query}
    ])

    ai_response = response.message.content

    print("AI:", ai_response)

    result = mem_client.add(
        user_id="nancy_raghav",
        messages=[
            {"role": "user", "content": user_query},
            {"role": "assistant", "content": ai_response}
        ],
        prompt="Extract explicitly stated personal facts, including the user's facts and observations and other details, as concise memories.",
    )

    print("Mem0 result:", result)


