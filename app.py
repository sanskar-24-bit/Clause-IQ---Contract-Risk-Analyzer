import uuid
from datetime import datetime
from pathlib import Path
import streamlit as st

from config import DATA_DIR, VECTOR_STORE_DIR
from document_loader import load_and_split
from vector_store import build_vector_store
from risk_analyzer import analyze, build_qa_chain


st.set_page_config(page_title = "Clause IQ", page_icon = "⚖️")
st.title("⚖️ Clause IQ - Contract Risk Analyzer")
st.caption("Upload a contract and ask questions about its clauses and potential risks.")

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}
Path(DATA_DIR).mkdir(parents = True, exist_ok = True)

# Keep the latest result so it survives reruns (a download click reruns the script).
st.session_state.setdefault("last_result", None)


def save_uploaded_file(uploaded_file) -> str:
    original_name = Path(uploaded_file.name.replace("\\", "/")).name
    extension = Path(original_name).suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {extension or 'no extension'}")

    safe_stem = Path(original_name).stem.replace(" ", "_")
    destination = Path(DATA_DIR) / f"{safe_stem}_{uuid.uuid4().hex[:8]}{extension}"

    with destination.open("wb") as output_file:
        output_file.write(uploaded_file.getbuffer())

    return str(destination)


def build_report(entry: dict) -> str:
    sources = "\n".join(f"- {name}" for name in entry["sources"]) \
        or "- No source information was returned."
    return (
        "# Clause IQ - Contract Risk Analysis Report\n"
        f"_Generated: {datetime.now().strftime('%d %b %Y, %H:%M')}_\n\n"
        f"## Question\n{entry['question']}\n\n"
        f"## Answer\n{entry['answer']}\n\n"
        f"## Sources\n{sources}\n"
    )


# ---------- Sidebar: upload and index ----------

with st.sidebar:
    st.header("Upload contracts")

    uploaded_files = st.file_uploader(
        "Choose PDF, DOCX or TXT files",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True)

    if st.button("Process documents", use_container_width=True):

        if not uploaded_files:
            st.warning("Please upload at least one contract.")

        else:
            try:
                with st.spinner("Reading and indexing contracts..."):
                    all_chunks = []

                    for uploaded_file in uploaded_files:
                        saved_path = save_uploaded_file(uploaded_file)
                        all_chunks.extend(load_and_split(saved_path))

                    if not all_chunks:
                        raise ValueError(
                            "No text chunks were extracted. Check that the files "
                            "contain readable text.")

                    # Discard the old chain before replacing the persistent index.
                    st.session_state.pop("chain", None)
                    build_vector_store(all_chunks, persist_dir=VECTOR_STORE_DIR)
                    st.session_state.chain = build_qa_chain()

                    # Old answers belong to the old documents.
                    st.session_state.last_result = None

                st.success(f"Indexed {len(all_chunks)} document chunks successfully.")

            except Exception as error:
                st.error(f"Could not process the documents: {error}")

    if Path(VECTOR_STORE_DIR).is_dir():
        st.info("A saved vector store is available. You can ask questions.")


# ---------- Main: ask and answer ----------

st.header("Ask a question")
question = st.text_input(
    "Your question",
    placeholder="e.g. What are the termination and penalty clauses?")

if st.button("Analyze", type="primary"):

    if not question.strip():
        st.warning("Please enter a question.")

    elif not Path(VECTOR_STORE_DIR).is_dir():
        st.warning("Upload and process a contract first.")

    else:
        try:
            with st.spinner("Analyzing the contract..."):
                if "chain" not in st.session_state:
                    st.session_state.chain = build_qa_chain()

                result = analyze(question, st.session_state.chain)

            st.session_state.last_result = {
                "question": question.strip(),
                "answer": result["answer"],
                "sources": sorted({Path(s).name for s in result["sources"]}),
            }

        except Exception as error:
            st.error(f"Something went wrong: {error}")

entry = st.session_state.last_result

if entry:
    st.subheader("Answer")
    st.write(entry["answer"])

    st.subheader("Sources")
    if entry["sources"]:
        for source in entry["sources"]:
            st.markdown(f"- `{source}`")
    else:
        st.write("No source information was returned.")

    st.download_button(
        "⬇️ Download report",
        data=build_report(entry),
        file_name = f"clause_iq_report_{datetime.now():%Y%m%d_%H%M%S}.md",
        mime = "text/markdown")
