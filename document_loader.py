import os
from langchain_community.document_loaders import PyPDFLoader,TextLoader,Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import CHUNK_SIZE, CHUNK_OVERLAP

def load_document(file_path: str):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        loader = PyPDFLoader(file_path)

    elif ext == ".docx":
        loader = Docx2txtLoader(file_path)

    elif ext == ".txt":
        loader = TextLoader(file_path)

    else:
        raise ValueError(f"Unsupported file types: {ext}")

    return loader.load()

def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = CHUNK_SIZE,
        chunk_overlap = CHUNK_OVERLAP)

    return splitter.split_documents(documents)

def load_and_split(file_path: str):
    documents = load_document(file_path)
    return split_documents(documents)


