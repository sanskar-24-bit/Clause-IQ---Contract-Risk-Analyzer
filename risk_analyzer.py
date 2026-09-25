from langchain_mistralai import ChatMistralAI
from langchain_classic.chains import RetrievalQA
from langchain_classic.prompts import PromptTemplate

from config import MISTRAL_API_KEY, MISTRAL_MODEL
from retriever import get_retriever                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   # type: ignore

RISK_PROMPT = PromptTemplate(
    input_variables = ["context", "question"],
    template = """You are a contract risk analysis assistant.
Use the contract excerpts below to answer the question.
Flag risky clauses when relevant (liability, termination, penalties, indemnity, auto - renewal).
If the excerpts don't contain the answer, say so clearly instead of guessing.

Contract excerpts:
{context}

Question: {question}

Answer:"""
)

def get_llm():
    return ChatMistralAI(
        model = MISTRAL_MODEL,
        mistral_api_key = MISTRAL_API_KEY,
        temperature = 0.2
    )

def build_qa_chain(retriever = None):
    retriever = retriever or get_retriever()

    llm = get_llm()
    return RetrievalQA.from_chain_type(
        llm = llm,
        retriever = retriever,
        chain_type = "stuff",
        chain_type_kwargs = {"prompt":RISK_PROMPT},
        return_source_documents = True,
    )

def analyze(question: str, chain = None):
    chain = chain or build_qa_chain()
    result = chain.invoke({"query":question})

    return {
        "answer":result["result"],
        "sources":[doc.metadata.get("source","unknown") for doc in result["source_documents"]],
    }




