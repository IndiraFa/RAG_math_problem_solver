"""
Streamlit application for the Math RAG Assistant.
This application allows users to ask math-related questions and get answers
using a Retrieval-Augmented Generation (RAG) model.

Author: Indira FABRE
"""

import streamlit as st
import requests
from utils import set_background

FASTAPI_URL = "http://backend:8000" 

image_path = "images/background.png"

# Set background image
set_background(image_path)

# Title box using HTML
st.markdown("""
<div class="title-box">
    <h1>🧮 Math RAG Assistant</h1>
</div>
""", unsafe_allow_html=True)

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
