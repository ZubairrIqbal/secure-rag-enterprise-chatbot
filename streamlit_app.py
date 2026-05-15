import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Secure RBAC RAG Chatbot", layout="wide")

st.title("Secure Role-Based Enterprise RAG Chatbot")

if "token" not in st.session_state:
    st.session_state.token = None

if "role" not in st.session_state:
    st.session_state.role = None

st.sidebar.header("Login")

username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

if st.sidebar.button("Login"):
    response = requests.post(
        f"{API_URL}/login",
        data={
            "username": username,
            "password": password
        }
    )

    if response.status_code == 200:
        data = response.json()
        st.session_state.token = data["access_token"]
        st.session_state.role = data["role"]
        st.sidebar.success(f"Logged in as {st.session_state.role}")
    else:
        st.sidebar.error("Invalid username or password")

if st.session_state.token:
    st.success(f"Current role: {st.session_state.role}")

    question = st.text_input("Ask a question")

    if st.button("Ask"):
        headers = {
            "Authorization": f"Bearer {st.session_state.token}"
        }

        response = requests.post(
            f"{API_URL}/ask",
            json={"question": question},
            headers=headers
        )

        if response.status_code == 200:
            data = response.json()

            st.subheader("Answer")
            st.write(data["answer"])

            st.caption(f"Sources retrieved: {data['sources_retrieved']}")
        else:
            st.error(response.text)
else:
    st.info("Please login to use the chatbot.")