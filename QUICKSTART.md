# 🚀 Quick Start Guide

## Windows (PowerShell/CMD)

### Option 1: Using run.bat (Easiest)
1. Double-click `run.bat`
2. Wait for dependencies to install (first time only)
3. Open browser to `http://localhost:5000`

### Option 2: Manual Setup
```powershell
# Navigate to project folder
cd "C:\Users\ASUS\OneDrive\Desktop\Resume Enhancement app"

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

## Linux/Mac

### Option 1: Using run.sh
```bash
chmod +x run.sh
./run.sh
```

### Option 2: Manual Setup
```bash
# Install dependencies
pip3 install -r requirements.txt

# Run the app
python3 app.py
```

## Troubleshooting

### Port Already in Use
If port 5000 is busy, edit `app.py` and change:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Use different port
```

### Missing Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### NLTK Data Issues
The app will auto-download NLTK data. If issues persist:
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

## Features to Test

1. ✅ Upload a resume (PDF/DOCX/TXT)
2. ✅ Select target company
3. ✅ View ATS score
4. ✅ Check keyword analysis
5. ✅ Review skills gaps
6. ✅ Get improvement suggestions

## Production Deployment

For production, use:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Or on Windows:
```bash
pip install waitress
waitress-serve --host=0.0.0.0 --port=5000 app:app
```

