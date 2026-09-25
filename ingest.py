import os

from config import DATA_DIR, VECTOR_STORE_DIR
from document_loader import load_and_split                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             # type: ignore
from vector_store import build_vector_store                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            # type: ignore

def ingest():
    all_chunks = []

    for fname in os.listdir(DATA_DIR):
        path = os.path.join(DATA_DIR, fname)

        if os.path.isfile(path):
            print(f"Loading {fname}....")
            all_chunks.extend(load_and_split(path))


    if not all_chunks:
        print(f"No contract files found in {DATA_DIR}/")
        return

    print(f"Total chunks:{len(all_chunks)}")
    build_vector_store(all_chunks, VECTOR_STORE_DIR)
    print(f"Vector store built and saved to {VECTOR_STORE_DIR}/")


if __name__ == "__main__":
    ingest()