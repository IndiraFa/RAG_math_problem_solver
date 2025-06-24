import streamlit as st
import requests

FASTAPI_URL = "http://backend:8000" 

st.title("🧮 Math RAG Assistant")

if "chat" not in st.session_state:
    st.session_state.chat = []

query = st.chat_input("Ask your question...")

if query:
    st.session_state.chat.append(("user", query))
    with st.spinner("Thinking..."):
        response = requests.get(f"{FASTAPI_URL}/ask", params={"q": query})
        answer = response.json().get("answer", "Error")
        st.session_state.chat.append(("assistant", answer))

# Display chat
for role, msg in st.session_state.chat:
    st.chat_message(role).write(msg)
