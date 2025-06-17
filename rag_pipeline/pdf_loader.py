import fitz  # PyMuPDF
from pathlib import Path

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text.strip()

def load_all_pdfs(directory):
    pdf_texts = {}
    for pdf_file in Path(directory).glob("*.pdf"):
        text = extract_text_from_pdf(pdf_file)
        pdf_texts[pdf_file.name] = text
    return pdf_texts

# Test: Kør dette for at se resultatet
if __name__ == "__main__":
    docs = load_all_pdfs("data/")
    for name, content in docs.items():
        print(f"\n=== {name} ===\n{content[:300]}...\n")
