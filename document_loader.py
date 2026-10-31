import os
from langchain_community.document_loaders import (PyPDFLoader,TextLoader,Docx2txtLoader,)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import CHUNK_SIZE, CHUNK_OVERLAP

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}
def load_document(file_path: str):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Document not found: {file_path}")

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        loader = PyPDFLoader(file_path)

    elif extension == ".docx":
        loader = Docx2txtLoader(file_path)

    elif extension == ".txt":
        loader = TextLoader(file_path, encoding = "utf-8", autodetect_encoding = True)

    else:
        raise ValueError(f"Unsupported file type: {extension or 'no extension'}")

    return loader.load()


def split_documents(documents):
    if CHUNK_SIZE <= 0:
        raise ValueError("CHUNK_SIZE must be greater than zero.")
    
    if CHUNK_OVERLAP < 0 or CHUNK_OVERLAP >= CHUNK_SIZE:
        raise ValueError("CHUNK_OVERLAP must be non-negative and smaller than CHUNK_SIZE.")

    splitter = RecursiveCharacterTextSplitter(chunk_size = CHUNK_SIZE, chunk_overlap = CHUNK_OVERLAP)
    return splitter.split_documents(documents)

def load_and_split(file_path: str):
    documents = load_document(file_path)
    return split_documents(documents)
