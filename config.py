import os
from dotenv import load_dotenv

load_dotenv()

# --- API Keys ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# --- Models ---
EMBEDDING_MODEL = "text-embedding-3-small"
MISTRAL_MODEL = os.getenv("MISTRAL_MODEL", "open-mistral-7b")

# --- Chunking ---
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150

# --- Storage ---
VECTOR_STORE_DIR = "vector_store_db"
DATA_DIR = "data"