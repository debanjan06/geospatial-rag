"""
GeoSpatial-RAG: An AI Framework For Analysis Of Remote Sensing Images

This package provides a comprehensive framework for analyzing remote sensing images
using retrieval-augmented generation (RAG) with vision-language models.
"""

__version__ = "0.1.0"
__author__ = "Debanjan Shil"
__email__ = "bl.sc.p2dsc24032@bl.students.amrita.edu"

# Core imports
try:
    from .pipeline import GeoSpatialRAG
    from .embeddings import CLIPEmbedder
    from .database import SQLiteVectorDB
    from .retriever import SQLiteRetriever
    from .utils import load_config, setup_logging
    
    __all__ = [
        "GeoSpatialRAG",
        "CLIPEmbedder", 
        "SQLiteVectorDB",
        "SQLiteRetriever",
        "load_config",
        "setup_logging",
    ]
except ImportError as e:
    print(f"Warning: Some imports failed: {e}")
    print("Please install all dependencies with: pip install -r requirements.txt")
