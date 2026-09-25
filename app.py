import os
import tempfile

import streamlit as st

from document_loader import load_and_split
from vector_store import build_vector_store
from risk_analyzer import build_qa_chain, analyze

st.set_page_config(
    page_title = "Clause IQ - Contract Risk Analyzer",
    page_icon = "⚖️",
    layout = "wide")

# Custom CSS
st.markdown("""
<style>
.main {
    background-color: #0E1117;
}

.metric-card {
    background: #1E1E2F;
    padding: 15px;
    border-radius: 15px;
    text-align:center;
    color:white;
}

.answer-box {
    background:#1A2333;
    padding:20px;
    border-radius:15px;
    border-left:5px solid #4CAF50;
}

.risk-box {
    background:#2A1A1A;
    padding:15px;
    border-radius:12px;
    border-left:5px solid red;
}

.stButton>button {
    width:100%;
    border-radius:10px;
    height:50px;
    font-size:16px;
}
</style>
""", unsafe_allow_html = True)

st.title("⚖️ Clause IQ - Contract Risk Analyzer")  
st.caption("AI-Powered Contract Review using RAG + Mistral AI")

with st.sidebar:
    st.header("⚙️ Settings")

    top_k = st.slider(
        "Retrieved Chunks",
        min_value = 1,
        max_value = 10,
        value = 5)

    risk_level = st.selectbox(
        "Risk Sensitivity",
        ["Low", "Medium", "High"])

    st.divider()
    st.markdown("Example Questions")
    examples = ["What are the termination clauses?",
        "Is there any indemnity risk?",
        "What penalties are mentioned?",
        "Are there auto-renewal clauses?",
        "What liabilities exist?"]

    for q in examples:
        st.write("•", q)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("LLM", "Mistral")

with col2:
    st.metric("Retriever", f"Top-{top_k}")

with col3:
    st.metric("Sensitivity", risk_level)

st.divider()

uploaded_file = st.file_uploader("Upload Contract",
    type=["pdf", "docx", "txt"])

question = st.text_area("Ask a Contract Question",
    placeholder="Example: What risks exist in this agreement?")

if st.button("🔍 Analyze Contract"):

    if not question:
        st.warning("Please enter a question.")
    elif not uploaded_file:
        st.warning("Please upload a contract file.")
    else:

        with st.spinner("Analyzing contract..."):

            try:
                suffix = os.path.splitext(uploaded_file.name)[1]
                with tempfile.NamedTemporaryFile(delete = False, suffix = suffix) as tmp:
                    tmp.write(uploaded_file.getvalue())
                    tmp_path = tmp.name

                try:
                    chunks = load_and_split(tmp_path)
                    vector_store = build_vector_store(chunks, persist_dir = None)

                    retriever = vector_store.as_retriever(search_kwargs = {"k": top_k})
                    chain = build_qa_chain(retriever)
                    result = analyze(question, chain)

                finally:
                    os.remove(tmp_path)

                answer = result["answer"]
                sources = result["sources"]

                st.success("Analysis Complete")

                st.subheader("📋 Analysis")

                st.markdown(
                    f"""
                    <div class = 'answer-box'>
                    {answer}
                    </div>
                    """,
                    unsafe_allow_html = True)

                st.subheader("⚠️ Potential Risk Areas")

                risk_keywords = ["liability",
                    "termination",
                    "indemnity",
                    "penalty",
                    "renewal"]

                detected = []

                for word in risk_keywords:
                    if word.lower() in answer.lower():
                        detected.append(word)

                if detected:
                    for risk in detected:
                        st.markdown(
                            f"""
                            <div class = 'risk-box'>
                            🚨 {risk.upper()}
                            </div>
                            """,
                            unsafe_allow_html = True)
                else:
                    st.info("No major risk keywords detected.")

                st.subheader("📂 Sources")

                for src in set(sources):
                    st.write("📄", src)

                report = f"""
CONTRACT RISK ANALYSIS REPORT

Question:
{question}

Answer:
{answer}

Sources:
{sources}
"""

                st.download_button(
                    "⬇ Download Report",
                    report,
                    file_name="risk_report.txt")

            except Exception as e:
                st.error(str(e))


st.divider()
st.caption("Built with LangChain • ChromaDB • Mistral AI • Streamlit")