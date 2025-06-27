"""
Utility functions for the GeoSpatial-RAG system.
"""

import os
import json
import logging
import logging.config
from typing import Dict, Any, Optional
from PIL import Image


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """Load configuration from file or environment variables."""
    config = {}
    
    if config_path and os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
        except Exception as e:
            logging.warning(f"Error loading config file {config_path}: {str(e)}")
    
    # Environment variables
    env_config = {
        'clip_model_name': os.getenv('CLIP_MODEL_NAME', 'openai/clip-vit-base-patch32'),
        'vlm_model_name': os.getenv('VLM_MODEL_NAME', 'Salesforce/blip-image-captioning-large'),
        'device': os.getenv('DEVICE', 'auto'),
        'dataset_path': os.getenv('DATASET_PATH', './data/RSICD'),
        'db_path': os.getenv('DB_PATH', './database/rsicd_embeddings.db'),
        'batch_size': int(os.getenv('BATCH_SIZE', '16')),
        'text_weight': float(os.getenv('TEXT_WEIGHT', '0.7')),
        'image_weight': float(os.getenv('IMAGE_WEIGHT', '0.3')),
        'top_k': int(os.getenv('TOP_K', '5')),
        'log_level': os.getenv('LOG_LEVEL', 'INFO'),
    }
    
    env_config = {k: v for k, v in env_config.items() if v is not None}
    config.update(env_config)
    
    return config


def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None) -> None:
    """Setup logging configuration."""
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {'format': log_format},
        },
        'handlers': {
            'console': {
                'level': log_level,
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
            },
        },
        'loggers': {
            '': {
                'handlers': ['console'],
                'level': log_level,
                'propagate': False
            }
        }
    }
    
    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        logging_config['handlers']['file'] = {
            'level': log_level,
            'class': 'logging.FileHandler',
            'filename': log_file,
            'formatter': 'standard',
            'mode': 'a',
        }
        logging_config['loggers']['']['handlers'].append('file')
    
    logging.config.dictConfig(logging_config)


def validate_image(image: Image.Image, max_size: tuple = (1024, 1024)) -> Image.Image:
    """Validate and preprocess an image."""
    if not isinstance(image, Image.Image):
        raise ValueError("Input must be a PIL Image object")
    
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
    
    return image
