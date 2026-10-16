from mem0 import Memory

# for open ai
#OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

config = {
    "version": "v1.1",
    #THIS ONE IS FOR OPENAI ONLY
    # "embedder": { 
    #     "provider": "openai",
    #     "config": { "api_key": "localhost//..", "model": "text-embedding.."} #"config": { "api_key": OPENAI_API_KEY}"}
    # },
    "llm": {
        "provider": "ollama", #"provider": "openai" #Use Ollama to generate the reasoning/response
        "config": { #"api_key": OPENAI_API_KEY, 
                   "model": "qwen2.5:3b",
                    "ollama_base_url": "http://localhost:11434",
                     "temperature": 0
            } #"config": { "api_key": OPENAI_API_KEY, "model": "any model" }
    },
    "embedder": {
        "provider": "ollama",
        "config": {
            "model": "embeddinggemma:latest", #Use Ollama's embeddinggemma to convert memories into vectors.
            "ollama_base_url": "http://localhost:11434"
        }
    },
    "vector_store": { #Store those vectors in Qdrant.
        "provider": "qdrant",
        "config": {
            "url": "QDRANT_URL",
            "api_key": "QDRANT_API_KEY",
            "collection_name": "mem0_memories",
            "embedding_model_dims": 768
        }
        # "provider": "qdrant",
        # "config": { 
        #     "host": "localhost",
        #     "port": 6333, 
        #     }
    }
}

mem_client = Memory.from_config(config)