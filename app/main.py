from tests.eval_questions import EVAL_QUESTIONS
from app.chatbot import answer_question
from app.vectordb import load_vectorstore


def run_evaluation():
    vectorstore = load_vectorstore()

    print("\nRunning evaluation...\n")

    for item in EVAL_QUESTIONS:
        role = item["role"]
        question = item["question"]

        answer, docs = answer_question(vectorstore, question, role, k=3)

        print("=" * 60)
        print(f"ROLE: {role}")
        print(f"QUESTION: {question}")
        print(f"ANSWER: {answer}")
        print(f"SOURCES RETRIEVED: {len(docs)}")
        print("=" * 60)