from fastapi import FastAPI
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores.pgvector import PGVector
from langchain.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader
from sqlalchemy import create_engine,text
import os

app = FastAPI()

# Set up environment
db_url = os.environ["DATABASE_URL"]
ollama_url = os.environ.get("OLLAMA_URL", "http://localhost:11434")
collection_name = "math_qa"
db_url = os.environ.get("DATABASE_URL")
engine = create_engine(db_url)
llm_model_name = "llama3"  # tried: "llama3", "gemma:2b"

# Initialize Embeddings and Vector DB
embedding = OllamaEmbeddings(model="nomic-embed-text", base_url=ollama_url)

vectorstore = PGVector(
    connection_string=db_url,
    collection_name=collection_name,
    embedding_function=embedding,
)

#llm = Ollama(model="llama3", base_url=ollama_url)
llm = Ollama(model=llm_model_name, base_url=ollama_url)

qa = RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore.as_retriever())

@app.get("/ask")
def ask(q: str):
    """Answer a question using the vectorstore."""
    return {"answer": qa.run(q)}

@app.get("/llm-only")
def llm_only(q: str):
    """Use LLM directly without vectorstore, to see the impact of retrieval."""
    return {"answer": llm.invoke(q)}


@app.get("/debug/vector_count")
def count_docs():
    """
    Count the number of documents in the vectorstore collection.
    Returns a JSON object with the count.
    """
    with engine.connect() as conn:
        # Step 1: Get collection ID
        collection_result = conn.execute(
            text("SELECT uuid FROM langchain_pg_collection WHERE name = :name"),
            {"name": collection_name}
        ).fetchone()

        if collection_result is None:
            return {"error": f"Collection '{collection_name}' not found."}

        collection_id = collection_result[0]

        # Step 2: Count embeddings for this collection
        count_result = conn.execute(
            text("SELECT COUNT(*) FROM langchain_pg_embedding WHERE collection_id = :cid"),
            {"cid": collection_id}
        ).scalar()

        return {"count": count_result}