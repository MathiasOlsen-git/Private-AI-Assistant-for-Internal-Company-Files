from sentence_transformers import SentenceTransformer
import faiss
import pickle
from pathlib import Path
from pdf_loader import load_all_pdfs

#  Split tekst op i bidder
def chunk_text(text, chunk_size=500):
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

#  Indlæs PDF'er
data_dir = "data/"
documents = load_all_pdfs(data_dir)

chunks = []
metadata = []

for filename, content in documents.items():
    for chunk in chunk_text(content):
        chunks.append(chunk)
        metadata.append({"source": filename, "text": chunk})

#  Lav embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(chunks)

#  Opret FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

#  Gem index og metadata
Path("vectorstore/").mkdir(exist_ok=True)
faiss.write_index(index, "vectorstore/index.faiss")

with open("vectorstore/metadata.pkl", "wb") as f:
    pickle.dump(metadata, f)

print("✅ Embed og vektor-index gemt!")

