import streamlit as st
import sys
import os

# Tillad import af rag_pipeline
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from rag_pipeline.retriever import retrieve_relevant_chunks
from rag_pipeline.llm_interface import generate_answer_with_ollama

st.set_page_config(page_title="Intern Local AI Assistant")

st.title("🔐 Intern Local AI Assistant")
st.markdown("Stil et spørgsmål baseret på interne dokumenter (lokalt og privat).")

# Brugerinput
user_question = st.text_input("📝 Dit spørgsmål", placeholder="Fx: Hvad skal jeg vide om cybersecurity her i firmaet?")

if user_question:
    with st.spinner("🔍 Finder relevante dokumenter..."):
        chunks = retrieve_relevant_chunks(user_question)
        context = "\n\n".join([chunk["text"] for chunk in chunks])

        prompt = f"""Du er en hjælpsom AI-assistent. Besvar følgende spørgsmål baseret på konteksten nedenfor.

Kontekst:
{context}

Spørgsmål:
{user_question}

Svar:"""

        answer = generate_answer_with_ollama(prompt)

    st.markdown("### 🤖 Svar")
    st.write(answer)

    with st.expander("📄 Se anvendt kontekst"):
        for i, chunk in enumerate(chunks, 1):
            st.markdown(f"**{i}. ({chunk['source']})**")
            st.write(chunk["text"])
