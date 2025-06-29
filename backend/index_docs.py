"""
This script indexes the Microsoft Orca Math Word Problems dataset into a 
PGVector database using Ollama embeddings.

Author: Indira FABRE
"""
from datasets import load_dataset
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores.pgvector import PGVector
from langchain_core.documents import Document
import os
import time

# === Config ===
dataset_name = "microsoft/orca-math-word-problems-200k"
split = "train"
collection_name = "math_qa"
db_url = os.environ.get("DATABASE_URL")
ollama_url = os.environ.get("OLLAMA_URL", "http://localhost:11434")

if not db_url:
    raise ValueError("DATABASE_URL environment variable is missing.")

# === Load Dataset ===
print(f"Loading dataset: {dataset_name}...")
dataset = load_dataset(dataset_name, split=split).select(range(500)) # Limit to 200 samples for testing

print(f"Loaded {len(dataset)} samples.")

# === Set up Embeddings and PGVector ===
print("Connecting to embedding model and vector database...")

try:
    embedding = OllamaEmbeddings(model="nomic-embed-text", base_url=ollama_url)
except Exception as e:
    raise RuntimeError(f"Failed to connect to Ollama embeddings: {e}")


# === Temp instance to delete collection ===
print(f"Deleting collection {collection_name} (if it exists)...")
try:
    temp_vs = PGVector(
        connection_string=db_url,
        collection_name=collection_name,
        embedding_function=embedding,
    )
    temp_vs.delete_collection()
    print("Deleted.")
except Exception as e:
    print(f"Failed to delete collection {collection_name}: {e}")
    print("Continuing with reinitialization...")

# === Reinitialize vectorstore ===
print("Reinitializing collection...")
try:
    vectorstore = PGVector(
        connection_string=db_url,
        collection_name=collection_name,
        embedding_function=embedding,
    )
except Exception as e:
    raise RuntimeError(f"Failed to initialize PGVector: {e}")
print(f"Collection {collection_name} initialized successfully.")

# === Format and index data ===
docs = []
failed = 0


for i, item in enumerate(dataset):
    question = item.get("question", "").strip()
    # Handle possible variations in answer format
    answer_raw = item.get("answer", "")
    print(f"Processing item {i + 1}/{len(dataset)}: {question} -> {answer_raw}")
    if isinstance(answer_raw, dict):
        answer = answer_raw.get("text", [""])[0]
    elif isinstance(answer_raw, str):
        answer = answer_raw
    else:
        answer = ""

    if question and answer:
        text = f"Q: {question}\nA: {answer.strip()}"
        docs.append(Document(page_content=text, metadata={"id": i}))
    else:
        failed += 1

print(f"Prepared {len(docs)} documents. Skipped {failed} invalid entries.")

# === Index in chunks ===
print("Indexing documents in batches...")
BATCH_SIZE = 100

for i in range(0, len(docs), BATCH_SIZE):
    batch = docs[i:i+BATCH_SIZE]
    print(f"Processing batch {i // BATCH_SIZE + 1}...")
    try:
        vectorstore.add_documents(batch)
        print(f"Indexed batch {i // BATCH_SIZE + 1}")
    except Exception as e:
        print(f"Failed to index batch {i // BATCH_SIZE + 1}: {e}")
        time.sleep(1)

print("Finished indexing.")
