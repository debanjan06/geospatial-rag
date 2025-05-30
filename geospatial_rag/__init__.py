"""
GeoSpatial-RAG: AI-Powered Remote Sensing Analysis System

A production-ready system for semantic search and analysis of satellite imagery
using state-of-the-art vision-language models and vector databases.

Author: Debanjan Shil
Email: bl.sc.p2dsc24032@bl.students.amrita.edu
Institution: Amrita Vishwa Vidyapeetham, Bengaluru
"""

__version__ = "1.0.0"
__author__ = "Debanjan Shil"
__email__ = "bl.sc.p2dsc24032@bl.students.amrita.edu"

# System information
SYSTEM_INFO = {
    "name": "GeoSpatial-RAG",
    "version": __version__,
    "description": "AI-Powered Remote Sensing Analysis System",
    "author": __author__,
    "email": __email__,
    "features": [
        "Multi-modal semantic search",
        "CLIP vision-language embeddings", 
        "Vector database integration",
        "Production-ready API",
        "Interactive web interface"
    ],
    "supported_databases": ["ChromaDB", "Pinecone", "Weaviate"],
    "supported_models": ["CLIP ViT-B/32", "CLIP ViT-L/14"],
    "datasets": ["RSICD", "Custom satellite imagery"]
}

def get_system_info():
    """Get system information and capabilities"""
    return SYSTEM_INFO

def print_banner():
    """Print system banner"""
    print("🛰️" + "="*60)
    print("   GeoSpatial-RAG: AI-Powered Remote Sensing Analysis")
    print("   Version:", __version__)
    print("   Author:", __author__)
    print("="*62) 
