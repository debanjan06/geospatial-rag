#!/usr/bin/env python3
"""
Test script to verify database connection and package functionality.
"""

import sqlite3
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, './src')

def test_database_connection():
    """Test database connection and get stats."""
    print("🔍 Testing Database Connection...")
    
    db_path = 'C:/Users/DEBANJAN SHIL/Documents/geospatial-rag/SQLiteDB/rsicd_clip_embeddings.db'
    
    # Check if file exists
    if not os.path.exists(db_path):
        print(f"❌ Database file not found at: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Test descriptions table
        cursor.execute('SELECT COUNT(*) FROM descriptions')
        desc_count = cursor.fetchone()[0]
        
        # Test text embeddings table
        cursor.execute('SELECT COUNT(*) FROM text_embeddings')
        text_emb_count = cursor.fetchone()[0]
        
        # Test image embeddings table
        cursor.execute('SELECT COUNT(*) FROM image_embeddings')
        img_emb_count = cursor.fetchone()[0]
        
        print(f"✅ Database connected successfully!")
        print(f"   📊 Descriptions: {desc_count}")
        print(f"   📝 Text embeddings: {text_emb_count}")
        print(f"   🖼️  Image embeddings: {img_emb_count}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False


def test_package_import():
    """Test package imports."""
    print("\n📦 Testing Package Imports...")
    
    try:
        # Test basic imports
        import numpy
        print("✅ NumPy available")
        
        import torch
        print(f"✅ PyTorch available (version: {torch.__version__})")
        
        import transformers
        print(f"✅ Transformers available (version: {transformers.__version__})")
        
        from PIL import Image
        print("✅ Pillow available")
        
        # Test our package
        from geospatial_rag import GeoSpatialRAG
        print("✅ GeoSpatial-RAG package imported successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False


def test_rag_system():
    """Test RAG system initialization."""
    print("\n🤖 Testing RAG System...")
    
    try:
        from geospatial_rag import GeoSpatialRAG
        
        db_path = 'C:/Users/DEBANJAN SHIL/Documents/geospatial-rag/SQLiteDB/rsicd_clip_embeddings.db'
        
        # Initialize RAG system
        print("   Initializing RAG system...")
        rag = GeoSpatialRAG(db_path=db_path)
        
        # Get stats
        stats = rag.get_stats()
        print(f"✅ RAG system initialized!")
        print(f"   📊 Database stats: {stats}")
        
        rag.close()
        return True
        
    except Exception as e:
        print(f"❌ RAG system error: {e}")
        return False


def test_query():
    """Test a simple query."""
    print("\n🔍 Testing Query Functionality...")
    
    try:
        from geospatial_rag import GeoSpatialRAG
        
        db_path = 'C:/Users/DEBANJAN SHIL/Documents/geospatial-rag/SQLiteDB/rsicd_clip_embeddings.db'
        
        rag = GeoSpatialRAG(db_path=db_path)
        
        # Test query
        print("   Running test query...")
        results = rag.query('aerial view of storage tanks', top_k=3)
        
        print(f"✅ Query successful!")
        print(f"   Query: {results['query']}")
        print(f"   Retrieved: {results['num_retrieved']} documents")
        
        if results['documents']:
            print("   Top result:")
            doc = results['documents'][0]
            print(f"   📄 {doc.page_content[:100]}...")
            print(f"   🔍 Similarity: {doc.metadata.get('similarity', 0):.4f}")
        
        rag.close()
        return True
        
    except Exception as e:
        print(f"❌ Query error: {e}")
        return False


def main():
    """Run all tests."""
    print("🚀 GeoSpatial-RAG System Test")
    print("=" * 40)
    
    # Run tests
    db_ok = test_database_connection()
    import_ok = test_package_import()
    
    if db_ok and import_ok:
        rag_ok = test_rag_system()
        if rag_ok:
            query_ok = test_query()
    
    print("\n" + "=" * 40)
    print("🎯 Test Summary:")
    print(f"   Database Connection: {'✅' if db_ok else '❌'}")
    print(f"   Package Imports: {'✅' if import_ok else '❌'}")
    if db_ok and import_ok:
        print(f"   RAG System: {'✅' if rag_ok else '❌'}")
        if rag_ok:
            print(f"   Query Test: {'✅' if query_ok else '❌'}")
    
    if db_ok and import_ok:
        print("\n🎉 Your system is ready to use!")
        print("\n📋 Next steps:")
        print("1. Try the interactive demo:")
        print("   python demo/interactive_demo.py --db_path 'C:/Users/DEBANJAN SHIL/Documents/geospatial-rag/SQLiteDB/rsicd_clip_embeddings.db'")
        print("2. Update your notebook to use the new package structure")
    else:
        print("\n⚠️  Some issues need to be resolved first.")


if __name__ == "__main__":
    main()