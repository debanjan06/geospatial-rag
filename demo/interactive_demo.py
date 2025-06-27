#!/usr/bin/env python3
"""
Interactive demo for GeoSpatial-RAG system.
"""

import argparse
import sys
from pathlib import Path
from PIL import Image

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from geospatial_rag import GeoSpatialRAG
from geospatial_rag.utils import setup_logging


def main():
    parser = argparse.ArgumentParser(description="Interactive GeoSpatial-RAG demo")
    parser.add_argument("--db_path", type=str, required=True, help="Path to SQLite database")
    parser.add_argument("--image", type=str, default=None, help="Path to input image")
    
    args = parser.parse_args()
    
    setup_logging(log_level="INFO")
    
    print("Initializing GeoSpatial-RAG system...")
    rag = GeoSpatialRAG(db_path=args.db_path)
    
    image = None
    if args.image:
        image = Image.open(args.image).convert("RGB")
        print(f"Loaded image: {args.image}")
    
    print("\nGeoSpatial-RAG Interactive Demo")
    print("=" * 40)
    print("Enter your query (or 'quit' to exit):")
    
    while True:
        try:
            query = input("\n> ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                break
            
            if not query:
                continue
            
            print("\nProcessing query...")
            results = rag.query(query, image=image)
            
            print(f"\nQuery: {results['query']}")
            print(f"Retrieved {results['num_retrieved']} documents")
            
            if 'image_caption' in results:
                print(f"Image caption: {results['image_caption']}")
            
            print("\nTop documents:")
            for i, doc in enumerate(results['documents'][:3]):
                print(f"{i+1}. {doc.page_content}")
                print(f"   Similarity: {doc.metadata.get('similarity', 0):.4f}")
            
            if 'response' in results:
                print(f"\nGenerated response:")
                print(results['response'])
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {str(e)}")
    
    print("\nGoodbye!")


if __name__ == "__main__":
    main()
