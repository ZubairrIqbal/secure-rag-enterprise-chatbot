from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

from app.auth import authenticate_user, create_access_token, get_current_user
from app.chatbot import answer_question
from app.vectordb import load_vectorstore
from fastapi.security import OAuth2PasswordRequestForm


app = FastAPI(title="Role-Based Enterprise RAG API")

vectorstore = load_vectorstore()


class LoginRequest(BaseModel):
    username: str
    password: str


class AskRequest(BaseModel):
    question: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/login")
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token({
        "sub": user["username"],
        "role": user["role"]
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user["role"]
    }


@app.post("/ask")
def ask(request: AskRequest, current_user: dict = Depends(get_current_user)):
    role = current_user["role"]

    answer, docs = answer_question(
        vectorstore=vectorstore,
        question=request.question,
        role=role,
        k=3
    )

    return {
        "user": current_user["username"],
        "role": role,
        "question": request.question,
        "answer": answer,
        "sources_retrieved": len(docs)
    }