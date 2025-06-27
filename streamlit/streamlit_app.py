"""
Streamlit application for the Math RAG Assistant.
This application allows users to ask math-related questions and get answers
using a Retrieval-Augmented Generation (RAG) model.

Author: Indira FABRE
"""

import streamlit as st
import requests
from utils import set_background, set_chat_css

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
# chat_css = """
# <style>
# .chat-container {
#     display: flex;
#     width: 100%;
#     margin-bottom: 1rem;
#     align-items: flex-start;
# }

# .chat-bubble {
#     background-color: rgba(255, 255, 255, 0.85);
#     border-radius: 12px;
#     padding: 0.75rem 1rem;
#     max-width: 80%;
#     box-shadow: 0 2px 6px rgba(0,0,0,0.1);
#     color: #333;
#     word-wrap: break-word;
# }

# .chat-left {
#     justify-content: flex-start;
#     flex-direction: row;
# }

# .chat-right {
#     justify-content: flex-end;
#     flex-direction: row-reverse;
# }

# .profile-icon {
#     font-size: 1.5rem;
#     margin: 0 0.5rem;
#     line-height: 1;
# }
# </style>
# """
# st.markdown(chat_css, unsafe_allow_html=True)


set_chat_css()

for role, msg in st.session_state.chat:
    align_class = "chat-left" if role == "assistant" else "chat-right"
    icon = "🤖" if role == "assistant" else "👩🏽"
    st.markdown(
        f'''
        <div class="chat-container {align_class}">
            <div class="profile-icon">{icon}</div>
            <div class="chat-bubble">{msg}</div>
        </div>
        ''',
        unsafe_allow_html=True
    )

