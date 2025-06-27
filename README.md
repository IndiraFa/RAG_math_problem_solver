# Understanding retrieval-augmented generation 
Usecase: ability so solve math problems 

## 1. Context and objectives

## 2. Quick setup

Repo structure:  

```bash

RAG_math_problem_solver/    # Root project directory
│
├── backend                 # Backend logic (RAG system)
│    └──app.py              # FastAPI app with endpoints (e.g. /ask, /llm-only)
│    └──index_docs.py       # Script to load and embed math documents into PGVector
│    └──requirements.txt    # Python dependencies for backend
│    └──Dockerfile          # Dockerfile to contenerize the FastAPI backend
├── streamlit               # Streamlit-based frontend
│    └──streamlit_app.py    # Streamlit web interface for interacting with the RAG system 
│    └──requirements.txt    # Python dependencies for Streamlit
│    └──Dockerfile          # Dockerfile to contenerize the Streamlit frontend
├── .env                    # Environment variables (e.g., DATABASE_URL, OLLAMA_URL)
├── docker-compose.yml      # Compose file to orchestrate both backend and frontend services
├── Makefile                # Useful CLI commands (e.g., `make up`, `make index`, etc.)
└── README.md               # Project overview, setup instructions, usage

```

## 3. Project architecture

## 4. Environement setup

## 5. Parameters

## 6. Dataset choice

## 7. RAG Usage

## 8. Results analysis

## 9. Conclusion and next steps