import os
import shutil
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from app.config import VECTORSTORE_DIR, EMBEDDING_MODEL


def get_embedding_function():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


def create_vectorstore(chunks):
    if os.path.exists(VECTORSTORE_DIR):
        shutil.rmtree(VECTORSTORE_DIR)

    embedding_function = get_embedding_function()

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_function,
        persist_directory=VECTORSTORE_DIR
    )

    return vectorstore


def load_vectorstore():
    embedding_function = get_embedding_function()

    return Chroma(
        persist_directory=VECTORSTORE_DIR,
        embedding_function=embedding_function
    )