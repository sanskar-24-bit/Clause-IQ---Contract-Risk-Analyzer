import shutil
from pathlib import Path
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from config import OPENAI_API_KEY, EMBEDDING_MODEL, VECTOR_STORE_DIR

def get_embeddings():
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is missing. Check your .env file.")

    return OpenAIEmbeddings(model = EMBEDDING_MODEL, api_key = OPENAI_API_KEY)

def build_vector_store(chunks, persist_dir: str | None = VECTOR_STORE_DIR):
    if not chunks:
        raise ValueError("No document chunks provided.")

    embeddings = get_embeddings()
    kwargs = {"documents": chunks, "embedding": embeddings}

    if persist_dir:
        store_path = Path(persist_dir)

        if store_path.exists():
            if not store_path.is_dir():
                raise NotADirectoryError(
                    f"Vector store path exists but is not a directory: {persist_dir}")
            shutil.rmtree(store_path)

        store_path.mkdir(parents = True, exist_ok = True)
        kwargs["persist_directory"] = str(store_path)

    return Chroma.from_documents(**kwargs)


def load_vector_store(persist_dir: str = VECTOR_STORE_DIR):
    if not persist_dir:
        raise ValueError("A persistent vector store directory must be provided.")

    store_path = Path(persist_dir)
    if not store_path.is_dir():
        raise FileNotFoundError(
            f"Vector store not found at '{persist_dir}'. Process contracts first.")

    embeddings = get_embeddings()
    return Chroma(persist_directory = str(store_path), embedding_function = embeddings)
