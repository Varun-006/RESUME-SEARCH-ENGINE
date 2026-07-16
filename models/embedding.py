# pyrefly: ignore [missing-import]
from sentence_transformers import SentenceTransformer


class EmbeddingModel:
    """
    Handles loading the embedding model and generating embeddings.
    """

    def __init__(self):
        print("Loading embedding model...")
        # Downloads the model the first time (~90MB)
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        print("Model loaded successfully!")

    def create_embedding(self, text):
        """
        Create an embedding for a single piece of text.
        Returns a list of floats.
        """
        embedding = self.model.encode(text)
        return embedding.tolist()

    def create_embeddings(self, texts):
        """
        Create embeddings for multiple texts at once.
        Returns a list of lists of floats.
        """
        embeddings = self.model.encode(texts)
        return embeddings.tolist()
