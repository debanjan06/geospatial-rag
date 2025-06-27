"""
Main pipeline for GeoSpatial-RAG system.
"""

import logging
from typing import Dict, List, Optional, Union, Any
from PIL import Image

from .embeddings import CLIPEmbedder
from .database import SQLiteVectorDB
from .retriever import SQLiteRetriever
from .models.vlm_models import VLMManager
from .utils import load_config, validate_image

logger = logging.getLogger(__name__)


class GeoSpatialRAG:
    """Main class for GeoSpatial-RAG system."""
    
    def __init__(
        self,
        db_path: str,
        config_path: Optional[str] = None,
        clip_model_name: str = "openai/clip-vit-base-patch32",
        vlm_model_name: str = "Salesforce/blip-image-captioning-large",
        device: str = "auto",
        **kwargs
    ):
        self.db_path = db_path
        self.config = load_config(config_path) if config_path else {}
        self.config.update(kwargs)
        
        logger.info("Initializing GeoSpatial-RAG system...")
        
        self.embedder = CLIPEmbedder(model_name=clip_model_name, device=device)
        self.db = SQLiteVectorDB(db_path)
        
        try:
            self.vlm_manager = VLMManager(model_name=vlm_model_name, device=device)
        except Exception as e:
            logger.warning(f"VLM manager initialization failed: {e}")
            self.vlm_manager = None
        
        self.text_weight = self.config.get('text_weight', 0.7)
        self.image_weight = self.config.get('image_weight', 0.3)
        self.top_k = self.config.get('top_k', 5)
        
        logger.info("GeoSpatial-RAG system initialized successfully")
    
    def query(
        self,
        text: str,
        image: Optional[Union[str, Image.Image]] = None,
        top_k: Optional[int] = None,
        filter_class: Optional[str] = None,
        generate_response: bool = True
    ) -> Dict[str, Any]:
        """Query the RAG system with text and/or image."""
        logger.info(f"Processing query: '{text[:50]}...'")
        
        if top_k is None:
            top_k = self.top_k
        
        if image is not None:
            if isinstance(image, str):
                image = Image.open(image).convert("RGB")
            image = validate_image(image)
        
        text_embedding = self.embedder.encode_text(text)
        image_embedding = None
        if image is not None:
            image_embedding = self.embedder.encode_image(image)
        
        retriever = SQLiteRetriever(
            db_path=self.db_path,
            query_embedding=text_embedding,
            image_embedding=image_embedding,
            combine_weights=(self.text_weight, self.image_weight)
        )
        
        documents = retriever.get_relevant_documents(top_k=top_k, filter_class=filter_class)
        
        logger.info(f"Retrieved {len(documents)} relevant documents")
        
        result = {
            'query': text,
            'documents': documents,
            'num_retrieved': len(documents)
        }
        
        if generate_response:
            try:
                image_caption = None
                if image is not None and self.vlm_manager:
                    image_caption = self.vlm_manager.generate_caption(image)
                    result['image_caption'] = image_caption
                
                context = self._build_context(documents)
                response = self._generate_response(text, context, image_caption)
                result['response'] = response
                
            except Exception as e:
                logger.error(f"Error generating response: {str(e)}")
                result['response'] = f"Error generating response: {str(e)}"
        
        return result
    
    def _build_context(self, documents: List) -> str:
        """Build context string from retrieved documents."""
        if not documents:
            return "No relevant context found."
        
        context_parts = []
        for i, doc in enumerate(documents[:5]):
            similarity = doc.metadata.get('similarity', 0)
            context_parts.append(f"{i+1}. {doc.page_content} (similarity: {similarity:.3f})")
        
        return "\n".join(context_parts)
    
    def _generate_response(self, query: str, context: str, image_caption: Optional[str] = None) -> str:
        """Generate response using retrieved context."""
        response_parts = [f"Query: {query}", ""]
        
        if image_caption:
            response_parts.extend([f"Image Description: {image_caption}", ""])
        
        response_parts.extend([
            "Based on similar remote sensing images in our database:",
            context,
            "",
            "This analysis is based on semantic similarity with existing remote sensing data."
        ])
        
        return "\n".join(response_parts)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics."""
        return self.db.get_stats()
    
    def close(self):
        """Close database connections and cleanup."""
        if hasattr(self, 'db'):
            self.db.close()
        logger.info("GeoSpatial-RAG system closed")
