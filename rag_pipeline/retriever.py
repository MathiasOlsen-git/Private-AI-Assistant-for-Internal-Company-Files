from sentence_transformers import SentenceTransformer
import faiss
import pickle

# Indlæs FAISS index og metadata
index = faiss.read_index("vectorstore/index.faiss")
with open("vectorstore/metadata.pkl", "rb") as f:
    metadata = pickle.load(f)

# Indlæs den samme model som ved embedding
model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_relevant_chunks(question, top_k=3):
    question_embedding = model.encode([question])
    distances, indices = index.search(question_embedding, top_k)

    results = []
    for idx in indices[0]:
        results.append(metadata[idx])
    return results

# Test-funktion
if __name__ == "__main__":
    user_question = input("🔍 Stil et spørgsmål: ")
    top_chunks = retrieve_relevant_chunks(user_question)

    print("\n📄 Mest relevante tekstbidder:\n")
    for i, chunk in enumerate(top_chunks, 1):
        print(f"{i}. ({chunk['source']})\n{chunk['text']}\n")
