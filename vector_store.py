from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from config import OPENAI_API_KEY, EMBEDDING_MODEL, VECTOR_STORE_DIR

def get_embeddings():
    return OpenAIEmbeddings(model = EMBEDDING_MODEL, api_key = OPENAI_API_KEY)

def build_vector_store(chunks, persist_dir: str = VECTOR_STORE_DIR):
    embeddings = get_embeddings()

    kwargs = {"documents": chunks, "embedding": embeddings} 
    if persist_dir:
        kwargs["persist_directory"] = persist_dir

def load_vector_store(persist_dir: str = VECTOR_STORE_DIR):
    embeddings =  get_embeddings()
    return Chroma(persist_directory = persist_dir, embedding_function = embeddings)