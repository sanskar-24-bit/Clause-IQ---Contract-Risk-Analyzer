from vector_store import load_vector_store
from config import VECTOR_STORE_DIR

def get_retriever( k : int = 4, persist_dir : str = VECTOR_STORE_DIR):
    vector_store = load_vector_store(persist_dir)
    return vector_store.as_retriever(search_kwargs = {"k":k})