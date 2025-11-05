#!/bin/bash

echo "Starting FANG Resume Enhancer..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check if requirements are installed
if ! python3 -c "import flask" &> /dev/null; then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies"
        exit 1
    fi
fi

# Create uploads directory
mkdir -p uploads

# Run the application
echo "Starting Flask application..."
echo "Open your browser to: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""
python3 app.py

