"""
Vercel serverless function handler for Flask app
This version has comprehensive error handling to identify import issues
"""
import sys
import os

# Add parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Set VERCEL environment before any imports
os.environ['VERCEL'] = '1'

# Try importing with detailed error reporting
try:
    from app import app
    print("✓ Successfully imported Flask app")
except ImportError as e:
    print(f"✗ ImportError: {e}")
    import traceback
    traceback.print_exc()
    # Create minimal error app
    from flask import Flask, jsonify
    app = Flask(__name__)
    
    @app.route('/')
    @app.route('/<path:path>')
    def error(path=''):
        return jsonify({
            'error': 'Import failed',
            'message': str(e),
            'type': 'ImportError'
        }), 500
except Exception as e:
    print(f"✗ Unexpected error: {e}")
    import traceback
    traceback.print_exc()
    # Create minimal error app
    from flask import Flask, jsonify
    app = Flask(__name__)
    
    @app.route('/')
    @app.route('/<path:path>')
    def error(path=''):
        import traceback
        return jsonify({
            'error': 'Initialization failed',
            'message': str(e),
            'type': type(e).__name__,
            'traceback': traceback.format_exc()
        }), 500

# Export app for Vercel
print("✓ Handler initialized successfully")
