import streamlit as st
from ai_modules.diagnostic_llm import ask_diagnostic, build_gc_context

st.set_page_config(page_title="🧠 GC AI Assistant", layout="wide")
st.title("🧠 GC Diagnostic Assistant (LLM)")

# 1️⃣ Input Serial + Context
serial_input = st.text_input("Enter Instrument Serial Number (optional for auto context)")
custom_context = st.text_area("Add additional notes or symptoms (optional)", height=100)
question = st.text_input("What do you want help with?")
submit = st.button("Ask AI")

# 2️⃣ Generate Combined Context
if submit and question:
    with st.spinner("Thinking..."):
        auto_context = build_gc_context(serial_input) if serial_input else ""
        full_context = f"{auto_context}\n\n{custom_context}".strip()
        response = ask_diagnostic(question, full_context)

    st.subheader("💬 AI Response")
    st.markdown(f"```markdown\n{response}\n```")
