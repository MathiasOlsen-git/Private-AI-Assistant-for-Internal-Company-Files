import sys
import os

# Tilføj projektmappen til sys.path, så vi kan importere rag_pipeline
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from rag_pipeline.retriever import retrieve_relevant_chunks
from rag_pipeline.llm_interface import generate_answer_with_ollama

# Brugerens spørgsmål
question = "Hvordan kalibrerer man X12 radar?"

# Hent relevante tekstuddrag fra PDF'erne
chunks = retrieve_relevant_chunks(question)
context = "\n\n".join([chunk["text"] for chunk in chunks])

# Prompt til modellen
prompt = f"""Du er en hjælpsom AI-assistent. Besvar følgende spørgsmål baseret på konteksten nedenfor.

Kontekst:
{context}

Spørgsmål:
{question}

Svar:"""

# Generér svar via lokal Mistral-model
answer = generate_answer_with_ollama(prompt)

# Udskriv svar
print("\n🤖 Svar fra modellen:\n")
print(answer)
