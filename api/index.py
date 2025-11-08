"""
Vercel serverless function handler for Flask app
Using Vercel's recommended pattern for Flask applications
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

# Import Flask app - this must succeed for Vercel
from app import app

# Vercel automatically detects Flask apps exported as 'app'
# No additional handler function needed
