# GeoSpatial-RAG:An AI Framework For Analysis Of Remote Sensing Images

A novel AI framework designed for analyzing remote sensing images using retrieval-augmented generation (RAG) with multimodal large language models.

## Overview

This project implements a comprehensive pipeline that bridges the domain gap between natural images and remote sensing imagery by creating a specialized RAG system. The framework combines CLIP embeddings, vector databases, and LangChain integration to enable semantic search and context-aware generation for Earth observation data.

## Key Features

- **Multi-Modal Knowledge Vector Database**: Stores both image and text embeddings using CLIP model in SQLite
- **Cross-Modal Retrieval**: Semantic search across remote sensing imagery using natural language queries
- **LangChain Integration**: Combines retrieval with vision-language models for comprehensive analysis
- **RSICD Dataset Support**: Processes over 10,000 remote sensing images with textual descriptions
- **Flexible Architecture**: Supports both local and API-based vision-language models

## Architecture

### 1. Multi-Modal Knowledge Vector Database Construction
- **Image & Caption Embeddings**: Uses CLIP (openai/clip-vit-base-patch32) to encode both visual and textual information
- **Automated Annotation**: Generates descriptions for remote sensing images using predefined candidate descriptions
- **SQLite Storage**: Efficient storage and retrieval of embeddings with proper indexing

### 2. Retrieval System
- **Semantic Search**: Cosine similarity-based retrieval using normalized embeddings
- **Combined Scoring**: Weighted combination of text (0.7) and image (0.3) similarities
- **Flexible Filtering**: Support for class-based filtering and top-k retrieval

### 3. LangChain Integration
- **Vision-Language Models**: Integration with BLIP for image captioning
- **Structured Prompting**: Context-aware prompt generation using retrieved documents
- **Response Generation**: Coherent natural language responses based on retrieved context

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/GeoSpatial-RAG.git
cd GeoSpatial-RAG

# Install required packages
pip install torch torchvision transformers
pip install langchain sqlite3 pillow numpy pandas tqdm
pip install huggingface-hub
```

## Dataset Setup

1. Download the RSICD dataset containing 10,921 remote sensing images
2. Organize the dataset structure:
```
RSCID/
├── train/
├── valid/
├── test/
├── train.csv
├── valid.csv
└── test.csv
```

## Usage

### 1. Generate Annotations and Embeddings

```python
# Run the embedding generation pipeline
python GeoSpatial-RAG.ipynb  # Cell 1: Multi-Modal Knowledge Vector Database Construction
```

### 2. Create SQLite Database

```python
# Ingest data into SQLite database
python GeoSpatial-RAG.ipynb  # Cell 2: Ingestion Of Data in SQLiteDB
```

### 3. Query the System

```python
from PIL import Image
import sqlite3

# Load your query image
image = Image.open("path/to/your/remote_sensing_image.jpg")

# Run the RAG pipeline
docs, response = rs_rag_langchain_pipeline(
    query="What does this aerial image show?",
    image=image,
    top_k=5
)

print("Retrieved Documents:")
for doc in docs:
    print(f"- {doc.page_content}")
    print(f"  Similarity: {doc.metadata['similarity']:.4f}")

print(f"\nGenerated Response:\n{response}")
```

### 4. Basic Similarity Search

```python
# Simple text-based retrieval
def find_similar_images(query_text, top_k=5):
    conn = sqlite3.connect("path/to/rsicd_clip_embeddings.db")
    
    # Create query embedding and search
    results = find_similar_by_text(query_text, top_k)
    
    for result in results:
        print(f"ID: {result['id']}")
        print(f"Description: {result['description']}")
        print(f"Similarity: {result['similarity']:.4f}\n")
```

## Configuration

Update the configuration paths in the notebook:

```python
# Configuration
base_path = "path/to/your/RSCID/dataset"
db_path = "path/to/your/SQLite/database"
model_name = "openai/clip-vit-base-patch32"
vlm_model_name = "Salesforce/blip-image-captioning-large"
```

## Database Schema

The SQLite database contains three main tables:

- **descriptions**: Stores image metadata (ID, class, description, path)
- **text_embeddings**: Stores CLIP text embeddings as BLOBs
- **image_embeddings**: Stores CLIP image embeddings as BLOBs

## Results

The system demonstrates:
- Effective cross-modal retrieval with high similarity scores
- Successful integration of text and image embeddings
- Context-aware generation using retrieved documents
- Bridging the domain gap between natural and remote sensing imagery

## Technical Details

- **Embedding Dimension**: 512 (CLIP-ViT-B/32)
- **Database Size**: 10,921 images with corresponding embeddings
- **Processing**: GPU-accelerated with CUDA support
- **Similarity Metric**: Cosine similarity with L2 normalization

## Applications

- Environmental monitoring and analysis
- Urban planning and development assessment
- Disaster response and damage assessment
- Agricultural land use classification
- Infrastructure and transportation analysis

## Acknowledgments

- RSICD dataset for remote sensing image captioning
- OpenAI CLIP for multimodal embeddings
- Salesforce BLIP for image captioning
- LangChain for framework integration
