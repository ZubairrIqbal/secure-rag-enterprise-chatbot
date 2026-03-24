# Secure Company RAG Chatbot

A secure internal company chatbot built with Retrieval-Augmented Generation (RAG), role-based access control (RBAC), and guardrails for safe document-based question answering.

## Features
- Multi-document RAG pipeline
- ChromaDB vector store
- Groq LLM integration
- Streamlit web interface
- Role-based access control (RBAC)
- Guardrails for sensitive query blocking
- Logging and basic evaluation support

## Tech Stack
- Python
- LangChain
- ChromaDB
- Groq
- Streamlit
- Pandas
- Sentence Transformers

## Supported Departments
- Engineering
- Finance
- HR
- Marketing
- General

## Roles
- Admin
- HR
- Finance
- Marketing
- Engineering
- Guest

## Security Features
- Department-level retrieval filtering
- Sensitive keyword blocking
- Out-of-scope question rejection
- Optional masking of emails and numeric confidential data

## How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt

# Note: 
Data Used in this project collect from: https://github.com/codebasics/ds-rpc-01
