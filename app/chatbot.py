import app.guardrails
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from app.config import GROQ_API_KEY, MODEL_NAME
from app.retriver import retrieve_documents


def format_context(documents):
    context_parts = []

    for i, doc in enumerate(documents, start=1):
        source = doc.metadata.get("source", "unknown")
        department = doc.metadata.get("department", "unknown")

        context_parts.append(
            f"[Document {i}] "
            f"(Department: {department}, Source: {source})\n"
            f"{doc.page_content}"
        )

    return "\n\n".join(context_parts)


def create_chat_model():
    return ChatGroq(
        api_key=GROQ_API_KEY,
        model=MODEL_NAME,
        temperature=0
    )


def answer_question(vectorstore, question, role, k=3):

    is_sensitive, msg = app.guardrails.check_sensitive_query(question)
    if is_sensitive:
        return f"Access Denied: {msg}", []

    is_out, msg = app.guardrails.check_out_of_scope(question)
    if is_out:
        return f"{msg}", []

    retrieved_docs = retrieve_documents(vectorstore, question, role, k=k)

    if not retrieved_docs:
        return "You are not authorized to access this information.", []

    context = format_context(retrieved_docs)

    prompt = ChatPromptTemplate.from_template(
        """
You are a secure internal company assistant.

STRICT RULES:
- Answer ONLY from given context
- Do NOT reveal personal or sensitive data
- If information is sensitive, refuse
- If not found, say not available

Context:
{context}

Question:
{question}
"""
    )

    model = create_chat_model()
    chain = prompt | model

    response = chain.invoke({
        "context": context,
        "question": question
    })

    return response.content, retrieved_docs