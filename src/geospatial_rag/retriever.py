"""
Custom retriever implementation for SQLite vector database.
"""

import sqlite3
import numpy as np
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

# Simple Document class for compatibility
class Document:
    def __init__(self, page_content: str, metadata: dict = None):
        self.page_content = page_content
        self.metadata = metadata or {}


class SQLiteRetriever:
    """Custom retriever class that works with SQLite vector database."""
    
    def __init__(self, db_path: str, query_embedding=None, image_embedding=None, 
                 combine_weights=(0.7, 0.3)):
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self.query_embedding = query_embedding
        self.image_embedding = image_embedding
        self.combine_weights = combine_weights
    
    def _compute_similarity(self, embedding_a, embedding_b):
        """Compute cosine similarity between two embeddings."""
        return np.dot(embedding_a, embedding_b) / (
            np.linalg.norm(embedding_a) * np.linalg.norm(embedding_b)
        )
    
    def get_relevant_documents(self, top_k=10, filter_class=None):
        """Retrieve relevant documents based on embedding similarity."""
        cursor = self.connection.cursor()
        
        if self.query_embedding is None:
            logger.warning("No query embedding provided")
            return []
        
        if filter_class:
            cursor.execute("""
                SELECT d.id, te.embedding, ie.embedding, d.description, d.class 
                FROM descriptions d
                JOIN text_embeddings te ON d.id = te.id
                LEFT JOIN image_embeddings ie ON d.id = ie.id
                WHERE d.class = ? AND d.id NOT LIKE 'query_%'
            """, (filter_class,))
        else:
            cursor.execute("""
                SELECT d.id, te.embedding, ie.embedding, d.description, d.class 
                FROM descriptions d
                JOIN text_embeddings te ON d.id = te.id
                LEFT JOIN image_embeddings ie ON d.id = ie.id
                WHERE d.id NOT LIKE 'query_%'
            """)
        
        results = cursor.fetchall()
        similarities = []
        
        for id, text_emb_bytes, img_emb_bytes, description, item_class in results:
            text_emb = np.frombuffer(text_emb_bytes, dtype=np.float32)
            
            text_similarity = self._compute_similarity(self.query_embedding, text_emb)
            combined_similarity = text_similarity
            
            if self.image_embedding is not None and img_emb_bytes is not None:
                img_emb = np.frombuffer(img_emb_bytes, dtype=np.float32)
                img_similarity = self._compute_similarity(self.image_embedding, img_emb)
                
                combined_similarity = (
                    self.combine_weights[0] * text_similarity + 
                    self.combine_weights[1] * img_similarity
                )
            
            doc = Document(
                page_content=description,
                metadata={
                    "id": id,
                    "class": item_class,
                    "similarity": float(combined_similarity)
                }
            )
            
            similarities.append((doc, combined_similarity))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        return [doc for doc, _ in similarities[:top_k]]
    
    def close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
