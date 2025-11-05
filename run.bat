@echo off
echo Starting FANG Resume Enhancer...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

REM Check if requirements are installed
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Create uploads directory
if not exist "uploads" mkdir uploads

REM Run the application
echo Starting Flask application...
echo Open your browser to: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python app.py

