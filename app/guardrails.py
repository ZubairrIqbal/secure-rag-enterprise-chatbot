import re
SENSITIVE_KEYWORDS = [
    "salary",
    "email",
    "phone",
    "address",
    "ssn",
    "personal",
    "employee id",
    "contact",
    "bank",
    "account"
]
OUT_OF_SCOPE = [
    "weather",
    "cricket",
    "football",
    "news",
    "movie",
    "song",
    "capital",
    "history"
]


def check_sensitive_query(question: str):
    q = question.lower()

    for word in SENSITIVE_KEYWORDS:
        if word in q:
            return True, "This query involves sensitive personal or confidential data."

    return False, ""


def check_out_of_scope(question: str):
    q = question.lower()

    for word in OUT_OF_SCOPE:
        if word in q:
            return True, "This question is outside the scope of company knowledge."

    return False, ""