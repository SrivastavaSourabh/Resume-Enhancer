"""
Setup script for FANG Resume Enhancer
Run this script to install all dependencies and set up the application
"""

import subprocess
import sys
import os

def install_requirements():
    """Install requirements from requirements.txt"""
    try:
        print("Installing Python dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing dependencies: {e}")
        return False

def setup_nltk_data():
    """Download required NLTK data"""
    try:
        print("Setting up NLTK data...")
        import nltk
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        print("✓ NLTK data downloaded successfully!")
        return True
    except Exception as e:
        print(f"⚠ Warning: Could not download NLTK data: {e}")
        print("The app will use fallback methods.")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ['uploads', 'static', 'templates']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    print("✓ Directories created!")

def main():
    print("=" * 50)
    print("FANG Resume Enhancer - Setup")
    print("=" * 50)
    print()
    
    create_directories()
    
    if install_requirements():
        setup_nltk_data()
        print()
        print("=" * 50)
        print("Setup completed successfully!")
        print("=" * 50)
        print()
        print("To run the application:")
        print("  python app.py")
        print()
        print("Then open your browser to:")
        print("  http://localhost:5000")
        print()
    else:
        print()
        print("Setup failed. Please install dependencies manually:")
        print("  pip install -r requirements.txt")
        print()

if __name__ == "__main__":
    main()

