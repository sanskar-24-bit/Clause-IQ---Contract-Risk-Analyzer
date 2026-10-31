import os
from pathlib import Path
from config import DATA_DIR, VECTOR_STORE_DIR
from document_loader import load_and_split
from vector_store import build_vector_store

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}

def ingest():
    data_path = Path(DATA_DIR)
    data_path.mkdir(parents = True, exist_ok = True)

    all_chunks = []

    for file_path in sorted(data_path.iterdir()):
        if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
            print(f"Loading {file_path.name}...")
            all_chunks.extend(load_and_split(str(file_path)))

    if not all_chunks:
        print(f"No supported contract files found in {DATA_DIR}/")
        return

    print(f"Total chunks: {len(all_chunks)}")
    build_vector_store(all_chunks, persist_dir = VECTOR_STORE_DIR)
    print(f"Vector store built and saved to {VECTOR_STORE_DIR}/")


if __name__ == "__main__":
    ingest()
