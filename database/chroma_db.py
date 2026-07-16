import chromadb


class ResumeDatabase:
    """
    Handles all ChromaDB operations for storing and searching resumes.
    """

    def __init__(self, db_path="./chroma_db"):
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(
            name="resumes"
        )

    def add_resume(self, resume_id, text, embedding, filename):
        """
        Add a single resume to the vector database.
        """
        self.collection.add(
            ids=[resume_id],
            documents=[text],
            embeddings=[embedding],
            metadatas=[{"filename": filename}]
        )

    def add_multiple_resumes(self, resumes):
        """
        Add multiple resumes at once.
        Each resume dict must have: id, text, embedding, filename
        """
        ids = []
        documents = []
        embeddings = []
        metadatas = []

        for resume in resumes:
            ids.append(resume["id"])
            documents.append(resume["text"])
            embeddings.append(resume["embedding"])
            metadatas.append({"filename": resume["filename"]})

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

    def search(self, query_embedding, top_k=5):
        """
        Search for the most similar resumes to a query embedding.
        Returns ChromaDB results dict with documents, metadatas, distances.
        """
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        return results

    def count(self):
        """
        Return the number of resumes stored in the database.
        """
        return self.collection.count()

    def delete_all(self):
        """
        Remove all resumes and recreate the collection.
        """
        try:
            self.client.delete_collection("resumes")
        except Exception:
            pass
        self.collection = self.client.get_or_create_collection("resumes")
