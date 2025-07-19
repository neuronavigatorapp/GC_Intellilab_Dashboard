# utils/rag_embed_text.py

import os
import json
import pickle
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from tqdm import tqdm

RAW_TEXT_PATH = "data/knowledge/raw_extracted_text.txt"
VECTOR_STORE_PATH = "data/knowledge/embedded_knowledge.pkl"
CHUNK_SIZE = 600  # characters
OVERLAP = 100

os.makedirs("data/knowledge", exist_ok=True)

# Load and chunk the OCR text
def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

# Main RAG embedding pipeline
def embed_chunks():
    if not os.path.exists(RAW_TEXT_PATH):
        print(f"❌ No text found at {RAW_TEXT_PATH}. Please run rag_ocr_ingest.py first.")
        return

    print("📖 Loading text...")
    with open(RAW_TEXT_PATH, "r", encoding="utf-8") as f:
        text = f.read()

    chunks = chunk_text(text)
    print(f"🔹 Split into {len(chunks)} chunks.")

    print("⚙️ Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")  # Lightweight model, good for local use

    print("🧠 Embedding...")
    embeddings = model.encode(chunks, show_progress_bar=True)

    print("💾 Saving vector store...")
    with open(VECTOR_STORE_PATH, "wb") as out:
        pickle.dump({"chunks": chunks, "embeddings": embeddings}, out)

    print(f"✅ Vector store saved to {VECTOR_STORE_PATH}")

if __name__ == "__main__":
    embed_chunks()
