"""
Vercel serverless function handler for Flask app
"""
import sys
import os

# Add parent directory to path to import app
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

try:
    # Import the Flask app
    from app import app
    
    # Vercel automatically detects Flask apps when you export 'app'
    # This is the simplest approach that works with @vercel/python
except Exception as e:
    # If import fails, create a minimal error app
    from flask import Flask, jsonify
    app = Flask(__name__)
    
    @app.route('/')
    def error():
        return jsonify({'error': f'Failed to import app: {str(e)}'}), 500

