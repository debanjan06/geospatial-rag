# GeoSpatial-RAG: An AI Framework For Analysis Of Remote Sensing Images

A novel AI framework designed specifically for the analysis of remote sensing images, integrating large language models (LLMs) with specialized vision-language models to overcome challenges in Earth observation data analysis.

## 🌍 Overview

GeoSpatial-RAG employs a retrieval-augmented generation (RAG) approach that creates a multi-modal knowledge vector database from remote sensing imagery and textual descriptions.

## ✨ Key Features

- **Multi-modal Knowledge Vector Database**: Unified encoding of remote sensing images and text descriptions
- **Cross-modal Retrieval**: Semantic search using natural language queries or image inputs
- **CLIP-based Embeddings**: Leverages CLIP for both visual and textual information encoding
- **LangChain Integration**: Advanced text generation with vision-language model support
- **SQLite Database**: Efficient storage and retrieval of embeddings

## 🚀 Installation

### Prerequisites
- Python 3.8+
- CUDA-compatible GPU (recommended)
- Git

### Setup
1. **Clone the repository**
```bash
git clone https://github.com/debanjan06/geospatial-rag.git
cd geospatial-rag
```

2. **Create virtual environment**
```bash
python -m venv geospatial_env
# On Windows: geospatial_env\Scripts\activate
# On Unix: source geospatial_env/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

## 🔧 Usage

### Quick Start

```python
from geospatial_rag import GeoSpatialRAG
from PIL import Image

# Initialize the RAG system
rag = GeoSpatialRAG(db_path="./database/rsicd_embeddings.db")

# Query with text
results = rag.query("Show me aerial views of storage tanks")

# Query with image
image = Image.open("path/to/satellite_image.jpg")
results = rag.query("What does this image show?", image=image)

# Print results
for doc in results['documents']:
    print(f"Description: {doc.page_content}")
    print(f"Similarity: {doc.metadata['similarity']:.4f}")
```

## 📞 Contact

- **Debanjan Shil** - [bl.sc.p2dsc24032@bl.students.amrita.edu](mailto:bl.sc.p2dsc24032@bl.students.amrita.edu)
- **Project Link** - [https://github.com/debanjan06/geospatial-rag](https://github.com/debanjan06/geospatial-rag)

---

⭐ **Star this repository if you find it helpful!**
