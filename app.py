from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os
import re
import json
import uuid
from werkzeug.utils import secure_filename
import PyPDF2
import docx
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

# Configure NLTK data path for Vercel serverless
if os.environ.get('VERCEL'):
    nltk.data.path.append('/tmp/nltk_data')

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Configuration
# Use /tmp for Vercel serverless, uploads for local
UPLOAD_FOLDER = '/tmp' if os.environ.get('VERCEL') else 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads directory (only for local, /tmp exists in Vercel)
if not os.environ.get('VERCEL'):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# FANG-specific keywords and requirements
FANG_KEYWORDS = {
    'technical': [
        'python', 'java', 'javascript', 'c++', 'c#', 'go', 'rust', 'scala', 'kotlin',
        'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'spring',
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'microservices', 'api', 'rest',
        'sql', 'nosql', 'mongodb', 'postgresql', 'mysql', 'redis', 'cassandra',
        'machine learning', 'deep learning', 'ai', 'neural networks', 'tensorflow', 'pytorch',
        'data structures', 'algorithms', 'system design', 'distributed systems',
        'agile', 'scrum', 'ci/cd', 'git', 'jenkins', 'terraform', 'ansible'
    ],
    'soft_skills': [
        'leadership', 'collaboration', 'communication', 'problem-solving', 'critical thinking',
        'mentoring', 'teamwork', 'adaptability', 'innovation', 'creativity'
    ],
    'quantitative': [
        'metrics', 'optimization', 'scalability', 'performance', 'efficiency',
        'throughput', 'latency', 'availability', 'reliability', 'analytics'
    ]
}

FANG_COMPANY_REQUIREMENTS = {
    'meta': {
        'keywords': ['react', 'graphql', 'php', 'hack', 'distributed systems', 'machine learning'],
        'focus': 'Social platforms, VR/AR, AI/ML'
    },
    'amazon': {
        'keywords': ['aws', 'java', 'distributed systems', 'scalability', 'customer obsession'],
        'focus': 'E-commerce, cloud services, scalability'
    },
    'netflix': {
        'keywords': ['java', 'python', 'microservices', 'streaming', 'recommendation systems'],
        'focus': 'Streaming, recommendation algorithms, content delivery'
    },
    'google': {
        'keywords': ['python', 'java', 'c++', 'machine learning', 'algorithms', 'distributed systems'],
        'focus': 'Search, AI/ML, cloud infrastructure, algorithms'
    }
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(file_path):
    """Extract text from PDF file"""
    try:
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def extract_text_from_docx(file_path):
    """Extract text from DOCX file"""
    try:
        doc = docx.Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except Exception as e:
        return f"Error reading DOCX: {str(e)}"

def extract_text_from_file(file_path, filename):
    """Extract text based on file type"""
    ext = filename.rsplit('.', 1)[1].lower()
    if ext == 'pdf':
        return extract_text_from_pdf(file_path)
    elif ext == 'docx':
        return extract_text_from_docx(file_path)
    elif ext == 'txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

def preprocess_text(text):
    """Clean and preprocess text"""
    text = text.lower()
    # Remove special characters but keep spaces
    text = re.sub(r'[^\w\s]', ' ', text)
    return text

def extract_keywords(text):
    """Extract keywords from text"""
    try:
        # Download required NLTK data (with better error handling for Vercel)
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            try:
                download_dir = '/tmp/nltk_data' if os.environ.get('VERCEL') else None
                nltk.download('punkt', quiet=True, download_dir=download_dir)
            except Exception:
                pass
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            try:
                download_dir = '/tmp/nltk_data' if os.environ.get('VERCEL') else None
                nltk.download('stopwords', quiet=True, download_dir=download_dir)
            except Exception:
                pass
        
        try:
            words = word_tokenize(preprocess_text(text))
            stop_words = set(stopwords.words('english'))
            keywords = [word for word in words if word.isalnum() and word not in stop_words and len(word) > 2]
            return keywords
        except Exception:
            # Fallback if NLTK fails
            words = preprocess_text(text).split()
            keywords = [w for w in words if len(w) > 2 and w.isalnum()]
            return keywords
    except Exception as e:
        # Final fallback: simple word extraction
        words = preprocess_text(text).split()
        keywords = [w for w in words if len(w) > 2 and w.isalnum()]
        return keywords

def calculate_ats_score(resume_text, keywords):
    """Calculate ATS compatibility score"""
    resume_text_lower = resume_text.lower()
    found_keywords = []
    missing_keywords = []
    
    all_keywords = []
    for category in FANG_KEYWORDS.values():
        all_keywords.extend(category)
    
    for keyword in all_keywords:
        if keyword.lower() in resume_text_lower:
            found_keywords.append(keyword)
        else:
            missing_keywords.append(keyword)
    
    score = (len(found_keywords) / len(all_keywords)) * 100 if all_keywords else 0
    return min(score, 100), found_keywords, missing_keywords[:20]  # Limit missing to 20

def analyze_skills_gap(resume_text, company='all'):
    """Analyze skills gap for specific FANG company"""
    resume_lower = resume_text.lower()
    gaps = {}
    
    if company == 'all':
        companies_to_check = FANG_COMPANY_REQUIREMENTS.keys()
    else:
        companies_to_check = [company] if company in FANG_COMPANY_REQUIREMENTS else []
    
    for comp in companies_to_check:
        req = FANG_COMPANY_REQUIREMENTS[comp]
        missing = [kw for kw in req['keywords'] if kw.lower() not in resume_lower]
        gaps[comp] = {
            'missing': missing,
            'matched': [kw for kw in req['keywords'] if kw.lower() in resume_lower],
            'focus': req['focus']
        }
    
    return gaps

def extract_sections(resume_text):
    """Extract sections from resume"""
    sections = {
        'experience': [],
        'education': [],
        'skills': [],
        'projects': []
    }
    
    lines = resume_text.split('\n')
    current_section = None
    
    for line in lines:
        line_lower = line.lower().strip()
        if any(keyword in line_lower for keyword in ['experience', 'work', 'employment', 'professional']):
            current_section = 'experience'
        elif any(keyword in line_lower for keyword in ['education', 'academic', 'university', 'degree']):
            current_section = 'education'
        elif any(keyword in line_lower for keyword in ['skills', 'technical', 'competencies']):
            current_section = 'skills'
        elif any(keyword in line_lower for keyword in ['projects', 'project', 'portfolio']):
            current_section = 'projects'
        
        if current_section and line.strip():
            sections[current_section].append(line.strip())
    
    return sections

def generate_suggestions(resume_text, ats_score, gaps, found_keywords):
    """Generate improvement suggestions"""
    suggestions = []
    
    # ATS Score suggestions
    if ats_score < 50:
        suggestions.append({
            'priority': 'high',
            'category': 'ATS Compatibility',
            'suggestion': 'Your resume has low ATS compatibility. Add more technical keywords relevant to FANG companies.',
            'action': f'Consider adding: {", ".join([kw for kw in FANG_KEYWORDS["technical"][:10] if kw not in found_keywords])}'
        })
    
    # Skills gap suggestions
    for company, gap_data in gaps.items():
        if len(gap_data['missing']) > 3:
            suggestions.append({
                'priority': 'medium',
                'category': f'{company.upper()} Optimization',
                'suggestion': f'Missing key skills for {company.upper()}: {", ".join(gap_data["missing"][:5])}',
                'action': f'Focus area: {gap_data["focus"]}'
            })
    
    # General suggestions
    if 'quantified achievements' not in resume_text.lower():
        suggestions.append({
            'priority': 'medium',
            'category': 'Impact Metrics',
            'suggestion': 'Add quantified achievements (metrics, percentages, numbers) to show impact.',
            'action': 'Example: "Improved system performance by 40%" or "Led team of 5 engineers"'
        })
    
    if len(extract_keywords(resume_text)) < 100:
        suggestions.append({
            'priority': 'low',
            'category': 'Content Depth',
            'suggestion': 'Resume content seems brief. Expand on technical details and achievements.',
            'action': 'Add more technical depth to your projects and experience sections.'
        })
    
    return suggestions

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_resume():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Please upload PDF, DOCX, or TXT'}), 400
        
        filename = secure_filename(file.filename)
        # Use unique filename for Vercel serverless to avoid conflicts
        unique_id = str(uuid.uuid4())
        file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else 'tmp'
        unique_filename = f"{unique_id}.{file_ext}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        
        # Extract text
        resume_text = extract_text_from_file(file_path, filename)
        
        if not resume_text or len(resume_text.strip()) < 50:
            return jsonify({'error': 'Could not extract sufficient text from resume'}), 400
        
        # Analyze
        keywords = extract_keywords(resume_text)
        ats_score, found_keywords, missing_keywords = calculate_ats_score(resume_text, keywords)
        gaps = analyze_skills_gap(resume_text, request.form.get('company', 'all'))
        sections = extract_sections(resume_text)
        suggestions = generate_suggestions(resume_text, ats_score, gaps, found_keywords)
        
        # Calculate overall score
        overall_score = (ats_score * 0.6) + (min(len(found_keywords) / 30 * 100, 100) * 0.4)
        
        result = {
            'success': True,
            'stats': {
                'word_count': len(resume_text.split()),
                'keyword_count': len(keywords),
                'ats_score': round(ats_score, 2),
                'overall_score': round(overall_score, 2)
            },
            'keywords': {
                'found': found_keywords[:30],
                'missing': missing_keywords
            },
            'skills_gaps': gaps,
            'sections': sections,
            'suggestions': suggestions,
            'resume_preview': resume_text[:500] + '...' if len(resume_text) > 500 else resume_text
        }
        
        # Cleanup
        try:
            os.remove(file_path)
        except:
            pass
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'message': 'Resume Enhancement API is running'})

# Export app for Vercel
# Vercel will automatically detect the Flask app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

