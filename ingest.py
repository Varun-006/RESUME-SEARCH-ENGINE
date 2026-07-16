import os
import sys

# Support running from project root
sys.path.insert(0, os.path.dirname(__file__))

from utils.pdf_reader import PDFReader
from utils.docx_reader import read_docx
from utils.txt_reader import read_txt
from utils.text_splitter import split_text
from models.embedding import EmbeddingModel
from database.chroma_db import ResumeDatabase


RESUMES_FOLDER = "data/resumes"


def load_all_resumes(folder_path):
    """
    Load all resumes from folder supporting PDF, DOCX, and TXT formats.
    Returns list of dicts with 'filename' and 'text'.
    """
    resumes = []

    if not os.path.exists(folder_path):
        print(f"Folder not found: {folder_path}")
        return resumes

    for filename in os.listdir(folder_path):
        full_path = os.path.join(folder_path, filename)
        ext = filename.lower().split(".")[-1]
        text = ""

        try:
            if ext == "pdf":
                reader = PDFReader(folder_path)
                text = reader.extract_text_from_pdf(full_path)
            elif ext == "docx":
                text = read_docx(full_path)
            elif ext == "txt":
                text = read_txt(full_path)
            else:
                continue  # skip unsupported types
        except Exception as e:
            print(f"  Error reading {filename}: {e}")
            continue

        if text.strip():
            resumes.append({"filename": filename, "text": text.strip()})

    return resumes


def main():
    print("=" * 60)
    print("  Resume Search Engine - Data Ingestion")
    print("=" * 60)

    # Initialize components
    model = EmbeddingModel()
    database = ResumeDatabase()

    # Clear previous data for a clean re-index
    print("\nClearing previous index...")
    database.delete_all()

    # Load all resumes
    print(f"\nReading resume files from '{RESUMES_FOLDER}'...")
    documents = load_all_resumes(RESUMES_FOLDER)
    print(f"Found {len(documents)} resume(s)")

    if len(documents) == 0:
        print("\nNo resumes found. Please add PDF, DOCX, or TXT files to:")
        print(f"  {RESUMES_FOLDER}/")
        return

    # Process and embed each resume
    resumes_to_store = []
    chunk_id = 0

    for doc in documents:
        print(f"\n  Processing: {doc['filename']}")

        # Split text into chunks for better embedding coverage
        chunks = split_text(doc["text"])
        print(f"    → {len(chunks)} chunk(s)")

        for chunk in chunks:
            embedding = model.create_embedding(chunk)
            resumes_to_store.append({
                "id": str(chunk_id),
                "filename": doc["filename"],
                "text": chunk,
                "embedding": embedding
            })
            chunk_id += 1

    # Store everything in ChromaDB
    print(f"\nSaving {len(resumes_to_store)} chunk(s) to ChromaDB...")
    database.add_multiple_resumes(resumes_to_store)

    print("\n" + "=" * 60)
    print(f"  Done! Total indexed chunks: {database.count()}")
    print("=" * 60)


if __name__ == "__main__":
    main()
