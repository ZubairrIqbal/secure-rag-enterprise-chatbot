import os
import pandas as pd
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_markdown_file(file_path: str, department: str):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    return Document(
        page_content=text,
        metadata={
            "source": file_path,
            "department": department,
            "file_type": "markdown"
        }
    )


def load_csv_file(file_path: str, department: str):
    df = pd.read_csv(file_path)

    docs = []
    for idx, row in df.iterrows():
        row_text = ", ".join([f"{col}: {row[col]}" for col in df.columns])

        docs.append(
            Document(
                page_content=row_text,
                metadata={
                    "source": file_path,
                    "department": department,
                    "file_type": "csv",
                    "row_index": idx
                }
            )
        )
    return docs


def load_all_documents(data_dir: str):
    all_docs = []

    for department in os.listdir(data_dir):
        dept_path = os.path.join(data_dir, department)

        if not os.path.isdir(dept_path):
            continue

        for file_name in os.listdir(dept_path):
            file_path = os.path.join(dept_path, file_name)

            if file_name.endswith(".md"):
                all_docs.append(load_markdown_file(file_path, department))

            elif file_name.endswith(".csv"):
                all_docs.extend(load_csv_file(file_path, department))

    return all_docs


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    return splitter.split_documents(documents)