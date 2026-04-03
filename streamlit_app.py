import os
import streamlit as st
from app.ingest import load_all_documents, split_documents
from app.vectordb import create_vectorstore, load_vectorstore
from app.chatbot import answer_question
from app.config import DATA_DIR, VECTORSTORE_DIR
from app.logger import log_interaction


st.set_page_config(
    page_title="Secure RAG Chatbot",
    page_icon="🔐",
    layout="wide"
)


@st.cache_resource
def prepare_vectorstore():
    if not os.path.exists(VECTORSTORE_DIR) or not os.listdir(VECTORSTORE_DIR):
        docs = load_all_documents(DATA_DIR)
        chunks = split_documents(docs)
        create_vectorstore(chunks)

    return load_vectorstore()


vectorstore = prepare_vectorstore()

st.sidebar.title("Access Control")
role = st.sidebar.selectbox(
    "Select your role",
    ["admin", "hr", "finance", "marketing", "engineering", "guest"]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "This chatbot uses retrieval-augmented generation with RBAC and guardrails."
)

st.title("Secure Internal Chatbot")
st.write("Ask questions from company documents based on your role and permissions.")

question = st.text_input("Enter your question")

if st.button("Ask") and question.strip():
    with st.spinner("Searching and generating answer..."):
        answer, retrieved_docs = answer_question(vectorstore, question, role, k=3)

    log_interaction(role, question, answer, len(retrieved_docs))

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Answer")
        st.write(answer)

    with col2:
        st.subheader("Session Info")
        st.write(f"**Role:** {role}")
        st.write(f"**Sources retrieved:** {len(retrieved_docs)}")

    st.subheader("Retrieved Sources")

    if retrieved_docs:
        for i, doc in enumerate(retrieved_docs, start=1):
            with st.expander(f"Source {i} - {doc.metadata.get('source', 'unknown')}"):
                st.write("**Metadata:**")
                st.json(doc.metadata)

                st.write("**Content Preview:**")
                st.write(doc.page_content[:1200])
    else:
        st.info("No source documents were retrieved.")