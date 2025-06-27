"""
Embedding generation module using CLIP model.
"""

import logging
from typing import Union, List, Optional
import numpy as np
import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel, CLIPTokenizer

logger = logging.getLogger(__name__)


class CLIPEmbedder:
    """CLIP-based embedder for generating text and image embeddings."""
    
    def __init__(self, model_name: str = "openai/clip-vit-base-patch32", device: str = "auto"):
        self.model_name = model_name
        self.device = self._setup_device(device)
        self._load_model()
    
    def _setup_device(self, device: str) -> torch.device:
        """Setup and return the appropriate device."""
        if device == "auto":
            device = "cuda" if torch.cuda.is_available() else "cpu"
        return torch.device(device)
    
    def _load_model(self):
        """Load CLIP model, processor, and tokenizer."""
        try:
            logger.info(f"Loading CLIP model: {self.model_name}")
            self.model = CLIPModel.from_pretrained(self.model_name)
            self.processor = CLIPProcessor.from_pretrained(self.model_name)
            self.tokenizer = CLIPTokenizer.from_pretrained(self.model_name)
            
            self.model = self.model.to(self.device)
            self.model.eval()
            
            self.text_embedding_dim = self.model.config.text_config.hidden_size
            self.image_embedding_dim = self.model.config.vision_config.hidden_size
            
            logger.info(f"CLIP model loaded successfully on {self.device}")
        except Exception as e:
            logger.error(f"Error loading CLIP model: {str(e)}")
            raise RuntimeError(f"Failed to load CLIP model: {str(e)}")
    
    def encode_text(self, text: Union[str, List[str]], normalize: bool = True) -> np.ndarray:
        """Encode text into embeddings using CLIP."""
        try:
            if isinstance(text, str):
                text = [text]
                return_single = True
            else:
                return_single = False
            
            text_tokens = self.tokenizer(
                text,
                padding="max_length",
                max_length=77,
                truncation=True,
                return_tensors="pt"
            ).to(self.device)
            
            with torch.no_grad():
                text_features = self.model.get_text_features(
                    input_ids=text_tokens.input_ids,
                    attention_mask=text_tokens.attention_mask
                )
                
                if normalize:
                    text_features = text_features / text_features.norm(dim=1, keepdim=True)
            
            embeddings = text_features.cpu().numpy()
            
            if return_single:
                embeddings = embeddings[0]
            
            return embeddings
            
        except Exception as e:
            logger.error(f"Error encoding text: {str(e)}")
            dim = self.text_embedding_dim
            if isinstance(text, str):
                return np.zeros(dim, dtype=np.float32)
            else:
                return np.zeros((len(text), dim), dtype=np.float32)
    
    def encode_image(self, image: Union[Image.Image, str], normalize: bool = True) -> np.ndarray:
        """Encode image into embeddings using CLIP."""
        try:
            if isinstance(image, str):
                image = Image.open(image).convert("RGB")
            elif isinstance(image, Image.Image):
                image = image.convert("RGB")
            
            inputs = self.processor(images=image, return_tensors="pt").to(self.device)
            
            with torch.no_grad():
                image_features = self.model.get_image_features(**inputs)
                
                if normalize:
                    image_features = image_features / image_features.norm(dim=1, keepdim=True)
            
            embeddings = image_features.cpu().numpy()[0]
            return embeddings
            
        except Exception as e:
            logger.error(f"Error encoding image: {str(e)}")
            return np.zeros(self.image_embedding_dim, dtype=np.float32)
    
    def compute_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """Compute cosine similarity between two embeddings."""
        similarity = np.dot(embedding1, embedding2) / (
            np.linalg.norm(embedding1) * np.linalg.norm(embedding2)
        )
        return float(similarity)
