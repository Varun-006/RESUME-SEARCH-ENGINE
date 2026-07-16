import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from models.embedding import EmbeddingModel
from database.chroma_db import ResumeDatabase


def print_results(results):
    """
    Pretty-print the top matching resumes from ChromaDB query results.
    """
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    print("\n" + "=" * 70)
    print("  Top Matching Resumes")
    print("=" * 70)

    if not documents:
        print("  No results found. Try ingesting resumes first (python ingest.py)")
        return

    for i in range(len(documents)):
        print(f"\n  Rank #{i + 1}")
        print(f"  Filename : {metadatas[i]['filename']}")
        print(f"  Distance : {round(distances[i], 4)}")
        print("\n  Resume Preview:")
        print("  " + documents[i][:400].replace("\n", "\n  "))
        print("-" * 70)


def main():
    model = EmbeddingModel()
    database = ResumeDatabase()

    print("=" * 60)
    print("  Resume Search Engine - CLI")
    print("=" * 60)
    print(f"  Resumes indexed: {database.count()}")
    print("\n  Type a job description to search for matching resumes.")
    print("  Type 'exit' to quit.\n")

    while True:
        query = input("Enter Job Description (or 'exit'): ").strip()

        if query.lower() == "exit":
            print("Goodbye!")
            break

        if not query:
            print("Please enter a search query.\n")
            continue

        embedding = model.create_embedding(query)
        results = database.search(embedding, top_k=5)
        print_results(results)
        print()


if __name__ == "__main__":
    main()
