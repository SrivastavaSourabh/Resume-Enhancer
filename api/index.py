"""
Vercel serverless function handler for Flask app
"""
import sys
import os

# Add parent directory to path to import app
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Set VERCEL environment variable before importing app
os.environ['VERCEL'] = '1'

try:
    # Import the Flask app
    from app import app
    
    # Vercel's @vercel/python automatically detects Flask apps
    # The app variable is exported and Vercel will use it
except ImportError as e:
    # If import fails, create a minimal error app
    from flask import Flask, jsonify
    app = Flask(__name__)
    
    @app.route('/')
    @app.route('/<path:path>')
    def error(path=''):
        import traceback
        error_msg = f'Failed to import app: {str(e)}\n\nTraceback:\n{traceback.format_exc()}'
        return jsonify({'error': error_msg, 'type': 'ImportError'}), 500
except Exception as e:
    # Catch any other errors during import
    from flask import Flask, jsonify
    app = Flask(__name__)
    
    @app.route('/')
    @app.route('/<path:path>')
    def error(path=''):
        import traceback
        error_msg = f'Error initializing app: {str(e)}\n\nTraceback:\n{traceback.format_exc()}'
        return jsonify({'error': error_msg, 'type': type(e).__name__}), 500

