import os
from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient

env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(env_path, override=True)

print("URI EXISTS:", bool(os.getenv("MONGODB_URI")))
print("URI START:", os.getenv("MONGODB_URI", "")[:20])

uri = os.getenv("MONGODB_URI")

client = MongoClient(uri)

try:
    client.admin.command("ping")
    print("MongoDB connected successfully!")
finally:
    client.close()