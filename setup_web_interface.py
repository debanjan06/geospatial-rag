#!/usr/bin/env python3
"""
Setup script for web interfaces.
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    print("🌐 Setting up Web Interface for GeoSpatial-RAG")
    print("=" * 50)
    
    # Web interface packages
    web_packages = [
        "streamlit>=1.28.0",
        "gradio>=3.0.0"
    ]
    
    print("📦 Installing web interface packages...")
    
    for package in web_packages:
        print(f"Installing {package}...")
        if install_package(package):
            print(f"✅ {package} installed successfully")
        else:
            print(f"❌ Failed to install {package}")
    
    print("\n🎉 Web interface setup completed!")
    print("\n🚀 You can now run:")
    print("1. Streamlit interface: streamlit run streamlit_app.py")
    print("2. Gradio interface: python gradio_app.py")
    
    # Create launch scripts
    print("\n📝 Creating launch scripts...")
    
    # Streamlit launcher
    streamlit_launcher = '''@echo off
echo 🚀 Starting GeoSpatial-RAG Streamlit Interface...
streamlit run streamlit_app.py
pause
'''
    with open("launch_streamlit.bat", "w") as f:
        f.write(streamlit_launcher)
    print("✅ Created launch_streamlit.bat")
    
    # Gradio launcher  
    gradio_launcher = '''@echo off
echo 🚀 Starting GeoSpatial-RAG Gradio Interface...
python gradio_app.py
pause
'''
    with open("launch_gradio.bat", "w") as f:
        f.write(gradio_launcher)
    print("✅ Created launch_gradio.bat")
    
    print("\n💡 Quick start:")
    print("- Double-click 'launch_streamlit.bat' for Streamlit interface")
    print("- Double-click 'launch_gradio.bat' for Gradio interface")

if __name__ == "__main__":
    main()