#!/usr/bin/env python3
"""
Streamlit Web Interface for GeoSpatial-RAG System

A ChatGPT-like interface for querying remote sensing images with text and image inputs.
"""

import streamlit as st
import sys
from pathlib import Path
import os
from PIL import Image
import time
import io
import base64

# Add src to path
current_dir = Path(__file__).parent
src_path = current_dir / "src"
sys.path.insert(0, str(src_path))

try:
    from geospatial_rag import GeoSpatialRAG
    from geospatial_rag.utils import setup_logging
except ImportError as e:
    st.error(f"❌ Failed to import GeoSpatial-RAG modules: {e}")
    st.info("Please ensure you're running this from the project root directory.")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="GeoSpatial-RAG ChatBot",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for chat-like interface
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .chat-container {
        max-height: 600px;
        overflow-y: auto;
        padding: 1rem;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        background-color: #f9f9f9;
    }
    
    .user-message {
        background-color: #007acc;
        color: white;
        padding: 10px 15px;
        border-radius: 15px 15px 5px 15px;
        margin: 10px 0;
        margin-left: 20%;
        text-align: right;
    }
    
    .bot-message {
        background-color: #e9ecef;
        color: #333;
        padding: 10px 15px;
        border-radius: 15px 15px 15px 5px;
        margin: 10px 0;
        margin-right: 20%;
    }
    
    .similarity-score {
        background-color: #28a745;
        color: white;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.8em;
        margin-left: 10px;
    }
    
    .document-result {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 10px;
        margin: 5px 0;
    }
    
    .stats-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables."""
    if 'rag_system' not in st.session_state:
        st.session_state.rag_system = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'system_initialized' not in st.session_state:
        st.session_state.system_initialized = False

def load_rag_system():
    """Load the RAG system with caching."""
    if st.session_state.rag_system is None:
        try:
            # Get database path from environment or default
            db_path = os.getenv('DB_PATH', 'C:/Users/DEBANJAN SHIL/Documents/geospatial-rag/SQLiteDB/rsicd_clip_embeddings.db')
            
            with st.spinner('🚀 Initializing GeoSpatial-RAG system...'):
                setup_logging(log_level="INFO")
                st.session_state.rag_system = GeoSpatialRAG(db_path=db_path)
                st.session_state.system_initialized = True
            
            return True
        except Exception as e:
            st.error(f"❌ Failed to initialize RAG system: {str(e)}")
            return False
    return True

def display_results(results):
    """Display query results in a formatted way."""
    st.markdown("### 📊 Search Results")
    
    # Summary
    st.info(f"🔍 Found **{results['num_retrieved']} relevant documents** for your query")
    
    # Image caption if available
    if 'image_caption' in results:
        st.markdown(f"**🖼️ Image Caption:** {results['image_caption']}")
    
    # Top documents
    if results['documents']:
        st.markdown("#### 📄 Most Relevant Documents:")
        
        for i, doc in enumerate(results['documents'][:3]):  # Show top 3
            similarity = doc.metadata.get('similarity', 0)
            
            with st.expander(f"📑 Document {i+1} (Similarity: {similarity:.3f})", expanded=i==0):
                st.markdown(f"**Content:** {doc.page_content}")
                st.markdown(f"**Class:** {doc.metadata.get('class', 'N/A')}")
                
                # Progress bar for similarity
                st.progress(similarity)
    
    # Generated response
    if 'response' in results:
        st.markdown("#### 🤖 AI Analysis:")
        st.markdown(results['response'])

def main():
    """Main application function."""
    initialize_session_state()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🛰️ GeoSpatial-RAG ChatBot</h1>
        <p>Intelligent Remote Sensing Image Analysis with AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("## ⚙️ System Configuration")
        
        # System status
        if st.session_state.system_initialized:
            st.success("✅ System Ready")
            
            # Get system stats
            if st.session_state.rag_system:
                try:
                    stats = st.session_state.rag_system.get_stats()
                    st.markdown("### 📊 Database Stats")
                    st.metric("Total Documents", stats.get('total_documents', 0))
                    st.metric("Text Embeddings", stats.get('total_text_embeddings', 0))
                    st.metric("Image Embeddings", stats.get('total_image_embeddings', 0))
                except:
                    pass
        else:
            st.warning("⚠️ System Not Initialized")
        
        st.markdown("---")
        
        # Query settings
        st.markdown("### 🔧 Query Settings")
        top_k = st.slider("Number of results", 1, 10, 5)
        text_weight = st.slider("Text weight", 0.0, 1.0, 0.7, 0.1)
        image_weight = 1.0 - text_weight
        st.write(f"Image weight: {image_weight:.1f}")
        
        # Filter options
        filter_class = st.selectbox(
            "Filter by class",
            ["All", "train", "valid", "test"],
            index=0
        )
        if filter_class == "All":
            filter_class = None
        
        st.markdown("---")
        
        # Clear chat
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
        
        # System info
        st.markdown("### ℹ️ About")
        st.info("""
        This system uses:
        - 🧠 CLIP for embeddings
        - 🗃️ SQLite vector database
        - 🔍 Semantic similarity search
        - 🤖 RAG for intelligent responses
        """)
    
    # Initialize system
    if not st.session_state.system_initialized:
        if st.button("🚀 Initialize System", use_container_width=True):
            if load_rag_system():
                st.success("✅ System initialized successfully!")
                st.rerun()
        else:
            st.warning("👆 Click 'Initialize System' to start using the chatbot")
            return
    
    # Main interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("## 💬 Chat Interface")
        
        # Display chat history
        for i, (query, image, response) in enumerate(st.session_state.chat_history):
            # User message
            with st.chat_message("user"):
                st.write(f"**You:** {query}")
                if image is not None:
                    st.image(image, width=200, caption="Uploaded Image")
            
            # Bot response
            with st.chat_message("assistant"):
                st.write(f"**🤖 GeoSpatial-RAG:** {response}")
        
        # Input form
        st.markdown("### 📝 Ask a Question")
        
        # Text input
        user_query = st.text_area(
            "Enter your query:",
            placeholder="e.g., 'Show me aerial views of storage tanks' or 'What does this satellite image show?'",
            height=100,
            key="query_input"
        )
        
        # Image upload
        uploaded_image = st.file_uploader(
            "Upload an image (optional):",
            type=['png', 'jpg', 'jpeg', 'tiff', 'tif'],
            help="Upload a satellite or aerial image to analyze",
            key="image_upload"
        )
        
        # Submit button
        if st.button("🔍 Search", use_container_width=True):
            if user_query.strip():
                if not st.session_state.system_initialized:
                    st.error("Please initialize the system first!")
                else:
                    # Process the query
                    with st.spinner('🔍 Searching database...'):
                        try:
                            # Process uploaded image
                            image_input = None
                            if uploaded_image is not None:
                                image_input = Image.open(uploaded_image).convert("RGB")
                            
                            # Query the RAG system
                            results = st.session_state.rag_system.query(
                                text=user_query,
                                image=image_input,
                                top_k=top_k,
                                filter_class=filter_class
                            )
                            
                            # Generate summary response
                            if results['documents']:
                                top_doc = results['documents'][0]
                                similarity = top_doc.metadata.get('similarity', 0)
                                summary = f"Found {results['num_retrieved']} relevant documents. Top match: '{top_doc.page_content[:100]}...' (similarity: {similarity:.3f})"
                                
                                if 'image_caption' in results:
                                    summary = f"Image shows: {results['image_caption']}. " + summary
                            else:
                                summary = "No relevant documents found for your query."
                            
                            # Add to chat history
                            st.session_state.chat_history.append((user_query, image_input, summary))
                            
                            # Display results in col2
                            with col2:
                                display_results(results)
                            
                            # Clear inputs
                            st.session_state.query_input = ""
                            st.rerun()
                            
                        except Exception as e:
                            st.error(f"❌ Error processing query: {str(e)}")
            else:
                st.warning("Please enter a query!")
    
    with col2:
        st.markdown("## 📊 Latest Results")
        
        if not st.session_state.chat_history:
            st.info("💡 Ask a question to see results here!")
        else:
            st.markdown("Results will appear here after your query.")
    
    # Example queries
    st.markdown("---")
    st.markdown("### 💡 Example Queries")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🏭 Industrial complex"):
            st.session_state.query_input = "industrial complex with buildings"
            st.rerun()
        if st.button("🛢️ Storage tanks"):
            st.session_state.query_input = "aerial view of storage tanks"
            st.rerun()
    
    with col2:
        if st.button("🏙️ Urban area"):
            st.session_state.query_input = "satellite image of urban area"
            st.rerun()
        if st.button("🌲 Forest area"):
            st.session_state.query_input = "remote sensing of forest"
            st.rerun()
    
    with col3:
        if st.button("🌊 Coastal area"):
            st.session_state.query_input = "coastal area with water"
            st.rerun()
        if st.button("✈️ Airport runway"):
            st.session_state.query_input = "airport runway aerial view"
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        🛰️ GeoSpatial-RAG System | Powered by CLIP + BLIP + RAG
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()