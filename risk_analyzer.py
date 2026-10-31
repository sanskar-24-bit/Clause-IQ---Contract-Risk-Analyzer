from langchain_mistralai import ChatMistralAI
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from config import MISTRAL_API_KEY, MISTRAL_MODEL
from retriever import get_retriever

RISK_PROMPT = PromptTemplate(
    input_variables = ["context", "question"],
    template = """You are a contract risk analysis assistant.

Use the contract excerpts below to answer the question.
Flag risky clauses when relevant, including liability, termination,
penalties, indemnity, and auto-renewal.

If the excerpts do not contain the answer, say so clearly
instead of guessing.

Contract excerpts:
{context}

Question: {question}

Answer:""")


def get_llm():
    if not MISTRAL_API_KEY:
        raise ValueError("MISTRAL_API_KEY is missing. Check your .env file.")

    return ChatMistralAI(model = MISTRAL_MODEL, mistral_api_key = MISTRAL_API_KEY, temperature = 0.2)

def build_qa_chain(retriever = None):
    if retriever is None:
        retriever = get_retriever()

    llm = get_llm()
    return RetrievalQA.from_chain_type(llm = llm, retriever = retriever, chain_type = "stuff",chain_type_kwargs = {"prompt": RISK_PROMPT}, return_source_documents = True)

def analyze(question: str, chain = None):
    if not question or not question.strip():
        raise ValueError("Please enter a valid question.")

    if chain is None:
        chain = build_qa_chain()

    result = chain.invoke({"query": question})

    source_documents = result.get("source_documents", [])
    sources = [
        document.metadata.get("source", "unknown")
        for document in source_documents]

    return {
        "answer": result.get("result", ""),
        "sources": sources}
