# GeoSpatial-RAG: An AI Framework For Analysis Of Remote Sensing Images

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)

A novel AI framework designed specifically for the analysis of remote sensing images, integrating large language models (LLMs) with specialized vision-language models to overcome challenges in Earth observation data analysis.

![GeoSpatial-RAG Demo](https://via.placeholder.com/800x400/1e3c72/ffffff?text=GeoSpatial-RAG+Framework)

## 🌍 Overview

GeoSpatial-RAG employs a retrieval-augmented generation (RAG) approach that creates a multi-modal knowledge vector database from remote sensing imagery and textual descriptions. The framework addresses the significant domain gap between natural images and remote sensing imagery by developing a specialized pipeline using CLIP (Contrastive Language-Image Pretraining).

### 🎯 Key Innovation
- **Domain-Specific RAG**: First RAG system specifically designed for remote sensing imagery
- **Multi-Modal Intelligence**: Seamlessly combines text and image understanding
- **High Accuracy**: Achieves 88%+ similarity matching for relevant queries
- **Production Ready**: Complete web interface with ChatGPT-like experience

## ✨ Key Features

- 🧠 **Multi-modal Knowledge Vector Database**: Unified encoding of remote sensing images and text descriptions
- 🔍 **Cross-modal Retrieval**: Semantic search using natural language queries or image inputs
- 🎯 **CLIP-based Embeddings**: Leverages CLIP for both visual and textual information encoding
- 🤖 **LangChain Integration**: Advanced text generation with vision-language model support
- 🗃️ **SQLite Database**: Efficient storage and retrieval of embeddings
- 🌐 **Web Interface**: Modern ChatGPT-like interface for easy interaction
- ⚡ **Real-time Processing**: GPU-accelerated processing for fast responses

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Input Query   │    │     Images      │    │  Text Captions  │
│   (Text/Image)  │    │                 │    │                 │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          ▼                      ▼                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CLIP Encoder                                 │
│                (Text + Vision)                                  │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                SQLite Vector Database                           │
│            (Text & Image Embeddings)                           │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│              Similarity Search & Retrieval                     │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│        LangChain RAG Pipeline + VLM Generation                 │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│              Generated Response                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- CUDA-compatible GPU (recommended)
- 8GB+ RAM

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/debanjan06/geospatial-rag.git
cd geospatial-rag
```

2. **Create virtual environment**
```bash
python -m venv geospatial_env

# Windows
geospatial_env\Scripts\activate

# Linux/MacOS
source geospatial_env/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
pip install -e .
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 🗃️ Database Setup

#### Option 1: Use Pre-built Database (Recommended for Testing)
```bash
# Download our pre-built database (10,975 documents)
# Place in: database/rsicd_embeddings.db
# Contact: bl.sc.p2dsc24032@bl.students.amrita.edu for access
```

#### Option 2: Create Your Own Database
```bash
# 1. Download RSICD dataset
wget [RSICD_DATASET_URL]

# 2. Generate embeddings
python scripts/generate_embeddings.py --dataset_path /path/to/RSICD --output_dir ./database

# 3. Create SQLite database
python scripts/create_database.py --embeddings_dir ./database --db_path ./database/rsicd_embeddings.db
```

#### Option 3: Demo Database (Quick Testing)
```bash
# Create a small demo database for testing
python scripts/create_demo_database.py
```

### 🧪 Test Your Setup

```bash
# Test database and imports
python test_database.py
```

Expected output:
```
🚀 GeoSpatial-RAG System Test
========================================
✅ Database connected successfully!
   📊 Descriptions: 10,975
   📝 Text embeddings: 10,975
   🖼️ Image embeddings: 10,975
✅ All tests passed!
```

## 🔧 Usage

### Command Line Interface

```bash
# Interactive demo
python demo/interactive_demo.py --db_path ./database/rsicd_embeddings.db
```

### Web Interface (Recommended)

```bash
# Start the web interface
streamlit run streamlit_app.py
```

Then open: http://localhost:8501

### Python API

```python
from geospatial_rag import GeoSpatialRAG
from PIL import Image

# Initialize the RAG system
rag = GeoSpatialRAG(db_path="./database/rsicd_embeddings.db")

# Text-only query
results = rag.query("Show me aerial views of storage tanks")

# Text + Image query
image = Image.open("satellite_image.jpg")
results = rag.query("What does this image show?", image=image)

# Display results
for doc in results['documents']:
    print(f"Description: {doc.page_content}")
    print(f"Similarity: {doc.metadata['similarity']:.4f}")
    print("---")

print(f"AI Response: {results['response']}")

# Close when done
rag.close()
```

## 📊 Performance Results

Our system has been tested and validated with impressive results:

- **📊 Database Size**: 10,975 remote sensing images with embeddings
- **🎯 Accuracy**: 88%+ similarity scores for relevant queries
- **⚡ Speed**: <2 seconds average query time on GPU
- **🔍 Precision**: High relevance in top-5 results for domain-specific queries

### Example Query Results

| Query | Top Similarity Score | Retrieved Documents | Response Quality |
|-------|---------------------|-------------------|------------------|
| "industrial complex with buildings" | 0.8818 | 5/5 relevant | Excellent |
| "aerial view of storage tanks" | 0.7631 | 5/5 relevant | Excellent |
| "satellite image of urban area" | 0.8203 | 4/5 relevant | Very Good |
| "remote sensing of forest" | 0.7892 | 5/5 relevant | Excellent |

## 📁 Project Structure

```
geospatial-rag/
├── src/
│   ├── __init__.py
│   └── geospatial_rag/           # Main package
│       ├── __init__.py
│       ├── embeddings.py         # CLIP embedding generation
│       ├── database.py           # SQLite database operations
│       ├── retriever.py          # Custom retriever class
│       ├── pipeline.py           # Main RAG pipeline
│       └── utils.py              # Utility functions
├── demo/
│   └── interactive_demo.py       # Command-line interface
├── tests/
│   └── test_*.py                 # Test modules
├── streamlit_app.py              # Web interface
├── setup_web_interface.py       # Web interface setup
├── quick_start.py                # Quick start script
├── test_database.py             # Database testing
├── requirements.txt              # Dependencies
├── setup.py                      # Package setup
├── LICENSE                       # MIT License
├── .gitignore                   # Git ignore rules
└── README.md                     # This file
```

## 🌐 Web Interface Features

The Streamlit web interface provides:

- 💬 **ChatGPT-like Interface**: Natural conversation flow
- 🖼️ **Image Upload**: Drag-and-drop satellite/aerial image analysis
- ⚙️ **Advanced Settings**: Configurable similarity thresholds and result counts
- 📊 **Real-time Stats**: Database statistics and system status
- 🔍 **Live Search**: Instant results with similarity scores
- 📱 **Responsive Design**: Works on desktop and mobile

## 🛠️ Configuration

### Environment Variables (.env)

```bash
# Model Configuration
CLIP_MODEL_NAME=openai/clip-vit-base-patch32
VLM_MODEL_NAME=Salesforce/blip-image-captioning-large
DEVICE=auto

# Database Configuration
DB_PATH=./database/rsicd_embeddings.db

# Processing Configuration
BATCH_SIZE=16
TEXT_WEIGHT=0.7
IMAGE_WEIGHT=0.3
TOP_K=5

# API Keys (optional)
HUGGINGFACE_API_KEY=your_hf_api_key_here
```

### Advanced Configuration

The system supports extensive configuration through:
- Environment variables
- Configuration files (JSON/YAML)
- Command-line arguments
- Python API parameters

## 📈 Dataset Information

### RSICD Dataset
- **Size**: 10,921 remote sensing images
- **Resolution**: 224×224 pixels
- **Sources**: Google Earth, Baidu Map, MapABC, Tianditu
- **Descriptions**: 5 sentences per image
- **Splits**: Train (8,734) / Valid (1,094) / Test (1,093)
- **Features**: High intra-class diversity and low inter-class dissimilarity

### Supported Image Types
- Satellite imagery
- Aerial photography
- Remote sensing data
- Multispectral images
- Urban planning imagery
- Agricultural monitoring
- Environmental surveillance

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test modules
pytest tests/test_embeddings.py
pytest tests/test_database.py
pytest tests/test_pipeline.py

# Run with coverage
pytest tests/ --cov=geospatial_rag --cov-report=html
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md).

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Install development dependencies: `pip install -e ".[dev]"`
4. Make your changes and add tests
5. Run tests: `pytest tests/`
6. Submit a pull request

### Areas for Contribution

- 🔬 **New Models**: Integration of additional vision-language models
- 📊 **Datasets**: Support for new remote sensing datasets
- 🌐 **Interfaces**: Mobile apps, desktop applications
- 🚀 **Performance**: Optimization and scaling improvements
- 📚 **Documentation**: Tutorials, examples, and guides

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📚 References

This work builds upon and is inspired by the following research:

[1] L. Fang et al., "Open-world recognition in remote sensing: Concepts, challenges, and opportunities," *IEEE Geosci. Remote Sens. Mag.*, vol. 12, no. 2, pp. 8–31, 2024.

[2] R. M. Haralick, K. Shanmugam, and I. Dinstein, "Textural features for image classification," *IEEE Trans. Syst., Man, Cybern.*, vol. SMC-3, no. 6, pp. 610–621, 1973.

[3] K. Kuckreja, M. S. Danish, M. Naseer, A. Das, S. Khan, and F. S. Khan, "Geochat: Grounded large vision-language model for remote sensing," *arXiv preprint arXiv:2311.15826*, 2023.

[4] R. Xu, C. Wang, J. Zhang, S. Xu, W. Meng, and X. Zhang, "Rssformer: Foreground saliency enhancement for remote sensing land-cover segmentation," *IEEE Trans. Image Process.*, vol. 32, pp. 1052–1064, 2023.

[5] J. Lin, Z. Yang, Q. Liu, Y. Yan, P. Ghamisi, W. Xie, and L. Fang, "Hslabeling: Toward efficient labeling for large-scale remote sensing image segmentation with hybrid sparse labeling," *IEEE Trans. Image Process.*, vol. 34, pp. 1864–1878, 2025.

[6] W. Zhang, M. Cai, T. Zhang, Y. Zhuang, and X. Mao, "Earthgpt: A universal multimodal large language model for multisensor image comprehension in remote sensing domain," *IEEE Trans. Geosci. Remote Sens.*, vol. 62, p. 5917820, 2024.

[7] Y. Hu, J. Yuan, C. Wen, X. Lu, and X. Li, "Rsgpt: A remote sensing vision language model and benchmark," *arXiv preprint arXiv:2307.15266*, 2023.

[8] L. Zhu, F. Wei, and Y. Lu, "Beyond text: Frozen large language models in visual signal comprehension," in *Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit.*, pp. 27047–27057, 2024.

[9] Z. Yuan, Z. Xiong, L. Mou, and X. X. Zhu, "Chatearthnet: A global-scale image–text dataset empowering vision–language geo-foundation models," *Earth Syst. Sci. Data*, vol. 17, pp. 1245–1263, 2025.

[10] X. Lu, B. Wang, X. Zheng, and X. Li, "Exploring models and data for remote sensing image caption generation," *IEEE Transactions on Geoscience and Remote Sensing*, vol. 56, no. 4, pp. 2183–2195, 2018.

## 🏆 Acknowledgments

- **Amrita Viswa Vidyapeetham** for research support and computational resources
- **OpenAI** for the CLIP model and vision-language research
- **Salesforce** for the BLIP model
- **RSICD dataset creators** for providing the remote sensing image captioning dataset
- **LangChain community** for the RAG framework
- **Streamlit team** for the excellent web app framework

## 📞 Contact & Support

- **Lead Researcher**: Debanjan Shil
- **Email**: [bl.sc.p2dsc24032@bl.students.amrita.edu](mailto:bl.sc.p2dsc24032@bl.students.amrita.edu)
- **Institution**: School of Computing, Amrita Viswa Vidyapeetham, Bengaluru
- **Project Repository**: [https://github.com/debanjan06/geospatial-rag](https://github.com/debanjan06/geospatial-rag)

### Getting Help

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/debanjan06/geospatial-rag/issues)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/debanjan06/geospatial-rag/discussions)
- 📧 **Direct Contact**: For database access or collaboration inquiries
- 📚 **Documentation**: Check our [docs/](docs/) directory for detailed guides

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=debanjan06/geospatial-rag&type=Date)](https://star-history.com/#debanjan06/geospatial-rag&Date)

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

**🚀 Ready to revolutionize remote sensing analysis with AI?**

[Get Started](https://github.com/debanjan06/geospatial-rag) • [Documentation](docs/) • [Examples](notebooks/) • [Web Demo](streamlit_app.py)

</div>
