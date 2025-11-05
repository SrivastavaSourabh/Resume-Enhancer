# 🚀 FANG Resume Enhancer

A powerful web application to optimize your resume for FANG companies (Meta, Amazon, Netflix, Google) and other top tech companies. Get personalized suggestions, ATS compatibility scores, and skills gap analysis.

## Features

- 📊 **ATS Compatibility Scoring**: Get your resume's compatibility score with Applicant Tracking Systems
- 🎯 **FANG-Specific Analysis**: Targeted optimization for Meta, Amazon, Netflix, and Google
- 🔍 **Keyword Analysis**: Identify missing and present keywords relevant to tech companies
- 💡 **Smart Suggestions**: Get actionable recommendations to improve your resume
- 📈 **Skills Gap Analysis**: See what skills you're missing for specific companies
- 📄 **Multi-Format Support**: Upload PDF, DOCX, or TXT files
- 🎨 **Modern UI**: Beautiful, responsive interface

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Clone or navigate to the project directory**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:5000`

## Usage

1. **Upload Your Resume**: Click "Choose File" or drag and drop your resume (PDF, DOCX, or TXT)
2. **Select Target Company** (Optional): Choose a specific FANG company or analyze for all
3. **Click "Analyze Resume"**: Get instant analysis and recommendations
4. **Review Results**:
   - Check your overall resume score
   - Review found and missing keywords
   - See company-specific skills gaps
   - Follow improvement suggestions
   - View detailed statistics

## API Endpoints

- `GET /` - Main application page
- `POST /api/analyze` - Analyze uploaded resume
  - Form data: `file` (required), `company` (optional: 'all', 'meta', 'amazon', 'netflix', 'google')
- `GET /api/health` - Health check endpoint

## Deployment

### Local Development
```bash
python app.py
```

### Production Deployment

#### Option 1: Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

#### Option 2: Using Waitress (Windows compatible)
```bash
pip install waitress
waitress-serve --host=0.0.0.0 --port=5000 app:app
```

#### Option 3: Deploy to Heroku
1. Create a `Procfile`:
   ```
   web: gunicorn -w 4 -b 0.0.0.0:$PORT app:app
   ```
2. Deploy using Heroku CLI

#### Option 4: Deploy to PythonAnywhere
1. Upload files to PythonAnywhere
2. Create a web app
3. Point to `app.py`

## Project Structure

```
Resume Enhancement app/
├── app.py                 # Flask backend application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/
│   └── index.html        # Frontend HTML
├── static/
│   ├── style.css         # Styling
│   └── script.js         # Frontend JavaScript
└── uploads/              # Temporary file storage (auto-created)
```

## Features Explained

### ATS Score
Measures how well your resume will pass through Applicant Tracking Systems used by most companies. Based on keyword density and relevance.

### Keyword Analysis
- **Found Keywords**: Technical terms and skills already present in your resume
- **Missing Keywords**: Important keywords you should consider adding

### Skills Gap Analysis
Company-specific analysis showing:
- Which required skills you have
- Which skills you're missing
- Focus areas for each company

### Improvement Suggestions
Prioritized recommendations:
- **High Priority**: Critical issues affecting your resume
- **Medium Priority**: Important improvements
- **Low Priority**: Nice-to-have enhancements

## Troubleshooting

### Issue: "NLTK data not found"
The app will automatically download required NLTK data on first run. If issues persist:
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

### Issue: "Cannot read PDF"
- Ensure the PDF is not password-protected
- Try converting to DOCX or TXT format

### Issue: Port already in use
Change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Use different port
```

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **PDF Processing**: PyPDF2
- **DOCX Processing**: python-docx
- **NLP**: NLTK
- **Styling**: Custom CSS with modern gradients and animations

## Contributing

Feel free to fork, improve, and submit pull requests!

## License

MIT License - Feel free to use this project for your own purposes.

## Support

For issues or questions, please open an issue on the repository.

---

**Built with ❤️ for FANG aspirants**

