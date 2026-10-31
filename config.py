import os
from dotenv import load_dotenv

load_dotenv()

# API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# Models
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
MISTRAL_MODEL = os.getenv("MISTRAL_MODEL", "open-mistral-7b")

# Document chunking
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150

# Local storage
VECTOR_STORE_DIR = os.getenv("VECTOR_STORE_DIR", "vector_store_db")
DATA_DIR = os.getenv("DATA_DIR", "data")