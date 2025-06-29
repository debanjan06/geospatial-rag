#!/usr/bin/env python3
"""
Quick start script for GeoSpatial-RAG project.
"""

import os
import sys
import subprocess
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{description}...")
    print(f"Running: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"Error: {e.stderr}")
        return False


def main():
    """Main quick start function."""
    print("🚀 GeoSpatial-RAG Quick Start")
    print("=" * 30)
    
    # Check if virtual environment exists
    venv_path = Path("geospatial_env")
    if not venv_path.exists():
        print("Creating virtual environment...")
        if not run_command("python -m venv geospatial_env", "Virtual environment creation"):
            sys.exit(1)
    
    # Install dependencies
    if os.name == 'nt':  # Windows
        pip_cmd = "geospatial_env\\Scripts\\pip"
    else:  # Unix/Linux/MacOS
        pip_cmd = "geospatial_env/bin/pip"
    
    if not run_command(f"{pip_cmd} install -r requirements.txt", "Dependencies installation"):
        sys.exit(1)
    
    if not run_command(f"{pip_cmd} install -e .", "Package installation"):
        sys.exit(1)
    
    # Create .env file if it doesn't exist
    env_file = Path(".env")
    if not env_file.exists():
        import shutil
        shutil.copy(".env.example", ".env")
        print("✅ Created .env file from .env.example")
        print("📝 Please edit .env file with specific configuration")
    
    print("\n" + "="*60)
    print("🎉 GeoSpatial-RAG Quick Start Completed!")
    print("="*60)
    
    print("\n📋 Next Steps:")
    print("1. Edit .env file with dataset paths and API keys")
    print("2. Update existing notebook to use the new package structure")
    print("3. Test: python -c \"import sys; sys.path.append('./src'); from geospatial_rag import GeoSpatialRAG\"")
    print("4. Run interactive demo with existing database")


if __name__ == "__main__":
    main()
