from config import VECTOR_STORE_DIR
from vector_store import load_vector_store

def get_retriever(k: int = 4, persist_dir: str = VECTOR_STORE_DIR):
    if k < 1:
        raise ValueError("k must be at least 1.")

    vector_store = load_vector_store(persist_dir)
    return vector_store.as_retriever(search_kwargs = {"k": k})
