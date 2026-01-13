import uuid
import os
from chromadb import Client
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import streamlit as st

class ChromaVectorDB:
    def __init__(self, persist_directory="chroma_db"):
        """
        Initialize Chroma client and collection.
        """
        self.client = Client(
            Settings(
                persist_directory=persist_directory,
                anonymized_telemetry=False
            )
        )
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="universities"
        )
        # Load embedding model
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")

    def add_documents(self, documents):
        """
        Each document gets a unique UUID.
        """
        if not documents:
            return

        # Generate embeddings
        embeddings = self.embedder.encode(documents, show_progress_bar=True)

        # Prepare IDs
        ids = [str(uuid.uuid4()) for _ in documents]
        

        # Add to collection
        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings.tolist() 
        )


    def query(self, query_text, top_k=5):
        """
        Query the vector database to find top_k similar documents.
        """
        query_embedding = self.embedder.encode([query_text])
        results = self.collection.query(
            query_embeddings=query_embedding.tolist(),
            n_results=top_k
        )
        # Return documents only
        return results.get("documents", [])

    def clear(self):
        """
        Clears all documents from the collection.
        """
        self.collection.delete()
    
    def peek(self,limit=50):
        data=self.collection.get(limit=limit)
        return data["documents"]