# pages/19_AI_Document_Search.py

import streamlit as st
import pickle
from sentence_transformers import SentenceTransformer, util

# Load vector store
with open("data/knowledge/embedded_knowledge.pkl", "rb") as f:
    embedded_knowledge = pickle.load(f)

model = SentenceTransformer("all-MiniLM-L6-v2")

st.set_page_config(page_title="AI Document Search", layout="centered")

st.markdown("""
    <style>
    .block-container {
        padding-top: 1.5rem;
    }
    label, textarea, input, select {
        font-size: 0.95rem !important;
    }
    @media screen and (max-width: 600px) {
        h1, h2, h3 {
            font-size: 1.4rem !important;
        }
        button[kind="primary"] {
            font-size: 1rem !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

st.title("📚 Ask TARGA: GC PDF Knowledge Search")

query = st.text_input("🔍 Ask a question about GC methods, service, or theory:")

if query:
    query_embedding = model.encode(query, convert_to_tensor=True)
    scores = util.cos_sim(query_embedding, embedded_knowledge["embeddings"])[0]
    
    top_k = min(3, len(scores))
    best_indices = scores.argsort(descending=True)[:top_k]

    for idx in best_indices:
        chunk = embedded_knowledge["chunks"][idx]
        score = scores[idx].item()
        st.markdown(f"**Score: {score:.2f}**")
        st.write(chunk)
        st.markdown("---")