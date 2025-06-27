"""
SQLite database operations for storing and retrieving embeddings.
"""

import os
import sqlite3
import logging
import time
from typing import Dict, List, Optional, Any
import numpy as np
import json

logger = logging.getLogger(__name__)


class SQLiteVectorDB:
    """SQLite-based vector database for storing and retrieving embeddings."""
    
    def __init__(self, db_path: str, auto_create: bool = True):
        self.db_path = db_path
        self.connection = None
        
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._connect()
        
        if auto_create:
            self._create_tables()
        
        logger.info(f"SQLite vector database initialized: {db_path}")
    
    def _connect(self):
        """Establish connection to the SQLite database."""
        try:
            self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row
            logger.debug(f"Connected to database: {self.db_path}")
        except Exception as e:
            logger.error(f"Error connecting to database: {str(e)}")
            raise
    
    def _create_tables(self):
        """Create database tables if they don't exist."""
        cursor = self.connection.cursor()
        
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS descriptions (
                    id TEXT PRIMARY KEY,
                    class TEXT,
                    description TEXT,
                    path TEXT,
                    metadata TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS text_embeddings (
                    id TEXT PRIMARY KEY,
                    embedding BLOB,
                    embedding_dim INTEGER,
                    model_name TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (id) REFERENCES descriptions(id)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS image_embeddings (
                    id TEXT PRIMARY KEY,
                    embedding BLOB,
                    embedding_dim INTEGER,
                    model_name TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (id) REFERENCES descriptions(id)
                )
            """)
            
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_descriptions_class ON descriptions(class)')
            
            self.connection.commit()
            logger.debug("Database tables created successfully")
            
        except Exception as e:
            logger.error(f"Error creating tables: {str(e)}")
            self.connection.rollback()
            raise
        finally:
            cursor.close()
    
    def add_document(
        self,
        text: str,
        text_embedding: Optional[np.ndarray] = None,
        image_embedding: Optional[np.ndarray] = None,
        metadata: Optional[Dict] = None,
        doc_class: str = "document",
        image_path: str = "",
        model_name: str = "openai/clip-vit-base-patch32"
    ) -> str:
        """Add a document with embeddings to the database."""
        doc_id = f"{doc_class}_{int(time.time())}_{hash(text) % 10000}"
        
        cursor = self.connection.cursor()
        
        try:
            cursor.execute(
                """INSERT OR REPLACE INTO descriptions 
                   (id, class, description, path, metadata) 
                   VALUES (?, ?, ?, ?, ?)""",
                (doc_id, doc_class, text, image_path, json.dumps(metadata or {}))
            )
            
            if text_embedding is not None:
                embedding_bytes = text_embedding.astype(np.float32).tobytes()
                cursor.execute(
                    """INSERT OR REPLACE INTO text_embeddings 
                       (id, embedding, embedding_dim, model_name) 
                       VALUES (?, ?, ?, ?)""",
                    (doc_id, embedding_bytes, len(text_embedding), model_name)
                )
            
            if image_embedding is not None:
                embedding_bytes = image_embedding.astype(np.float32).tobytes()
                cursor.execute(
                    """INSERT OR REPLACE INTO image_embeddings 
                       (id, embedding, embedding_dim, model_name) 
                       VALUES (?, ?, ?, ?)""",
                    (doc_id, embedding_bytes, len(image_embedding), model_name)
                )
            
            self.connection.commit()
            logger.debug(f"Added document with ID: {doc_id}")
            return doc_id
            
        except Exception as e:
            logger.error(f"Error adding document: {str(e)}")
            self.connection.rollback()
            raise
        finally:
            cursor.close()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics."""
        cursor = self.connection.cursor()
        
        try:
            stats = {}
            
            cursor.execute("SELECT COUNT(*) FROM descriptions")
            stats['total_documents'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM text_embeddings")
            stats['total_text_embeddings'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM image_embeddings")
            stats['total_image_embeddings'] = cursor.fetchone()[0]
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting database stats: {str(e)}")
            raise
        finally:
            cursor.close()
    
    def close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
            logger.debug("Database connection closed")
