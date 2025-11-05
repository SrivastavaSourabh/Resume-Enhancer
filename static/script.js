let currentData = null;

// File input handling
document.getElementById('fileInput').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        document.getElementById('fileName').textContent = `Selected: ${file.name}`;
        document.getElementById('analyzeBtn').disabled = false;
    }
});

// Drag and drop
const uploadBox = document.getElementById('uploadBox');
const fileInput = document.getElementById('fileInput');

uploadBox.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadBox.classList.add('dragover');
});

uploadBox.addEventListener('dragleave', () => {
    uploadBox.classList.remove('dragover');
});

uploadBox.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadBox.classList.remove('dragover');
    const file = e.dataTransfer.files[0];
    if (file && (file.type === 'application/pdf' || file.type.includes('word') || file.type === 'text/plain')) {
        fileInput.files = e.dataTransfer.files;
        document.getElementById('fileName').textContent = `Selected: ${file.name}`;
        document.getElementById('analyzeBtn').disabled = false;
    }
});

// Analyze resume
async function analyzeResume() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    const company = document.getElementById('companySelect').value;
    
    if (!file) {
        showError('Please select a file first');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', file);
    formData.append('company', company);
    
    // Show loading
    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('results').classList.add('hidden');
    document.getElementById('error').classList.add('hidden');
    
    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Analysis failed');
        }
        
        currentData = data;
        displayResults(data);
        
    } catch (error) {
        showError(error.message);
    } finally {
        document.getElementById('loading').classList.add('hidden');
    }
}

function displayResults(data) {
    // Update scores
    updateScore(data.stats.overall_score, data.stats.ats_score);
    document.getElementById('atsScore').textContent = Math.round(data.stats.ats_score);
    document.getElementById('keywordCount').textContent = data.keywords.found.length;
    
    // Display keywords
    displayKeywords(data.keywords.found, 'foundKeywords');
    displayKeywords(data.keywords.missing, 'missingKeywords');
    
    // Display gaps
    displayGaps(data.skills_gaps);
    
    // Display suggestions
    displaySuggestions(data.suggestions);
    
    // Display stats
    displayStats(data.stats, data.sections);
    
    // Show results
    document.getElementById('results').classList.remove('hidden');
}

function updateScore(overallScore, atsScore) {
    const scoreText = document.getElementById('overallScore');
    const scoreCircle = document.getElementById('scoreCircle');
    
    scoreText.textContent = Math.round(overallScore);
    
    const circumference = 2 * Math.PI * 45;
    const offset = circumference - (overallScore / 100) * circumference;
    scoreCircle.style.strokeDashoffset = offset;
    
    // Update color based on score
    let color = '#ef4444'; // red
    if (overallScore >= 70) color = '#10b981'; // green
    else if (overallScore >= 50) color = '#f59e0b'; // yellow
    
    scoreCircle.style.stroke = color;
}

function displayKeywords(keywords, containerId) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';
    
    keywords.forEach(keyword => {
        const tag = document.createElement('span');
        tag.className = 'keyword-tag';
        tag.textContent = keyword;
        container.appendChild(tag);
    });
    
    if (keywords.length === 0) {
        container.innerHTML = '<p style="color: var(--text-muted);">None found</p>';
    }
}

function displayGaps(gaps) {
    const container = document.getElementById('gapsContent');
    container.innerHTML = '';
    
    if (Object.keys(gaps).length === 0) {
        container.innerHTML = '<p style="color: var(--text-muted);">No gaps found. Great job!</p>';
        return;
    }
    
    Object.entries(gaps).forEach(([company, gapData]) => {
        const card = document.createElement('div');
        card.className = 'gap-card';
        
        const matchedPct = Math.round((gapData.matched.length / (gapData.matched.length + gapData.missing.length)) * 100);
        
        card.innerHTML = `
            <h4>${company.toUpperCase()}</h4>
            <p><strong>Focus:</strong> ${gapData.focus}</p>
            <p><strong>Match Rate:</strong> ${matchedPct}%</p>
            <div style="margin-top: 15px;">
                <strong style="color: var(--success);">Matched (${gapData.matched.length}):</strong>
                <div class="keyword-tags" style="margin-top: 10px;">
                    ${gapData.matched.map(kw => `<span class="keyword-tag" style="background: var(--success);">${kw}</span>`).join('')}
                </div>
            </div>
            ${gapData.missing.length > 0 ? `
                <div style="margin-top: 15px;">
                    <strong style="color: var(--danger);">Missing (${gapData.missing.length}):</strong>
                    <div class="keyword-tags" style="margin-top: 10px;">
                        ${gapData.missing.slice(0, 10).map(kw => `<span class="keyword-tag" style="background: var(--danger);">${kw}</span>`).join('')}
                    </div>
                </div>
            ` : ''}
        `;
        
        container.appendChild(card);
    });
}

function displaySuggestions(suggestions) {
    const container = document.getElementById('suggestionsContent');
    container.innerHTML = '';
    
    if (suggestions.length === 0) {
        container.innerHTML = '<p style="color: var(--success);">Your resume looks great! No major suggestions at this time.</p>';
        return;
    }
    
    suggestions.forEach(suggestion => {
        const card = document.createElement('div');
        card.className = `suggestion-card ${suggestion.priority}`;
        
        card.innerHTML = `
            <div class="category">${suggestion.category} • ${suggestion.priority.toUpperCase()} Priority</div>
            <h4>${suggestion.suggestion}</h4>
            <div class="action">
                <strong>Action:</strong> ${suggestion.action}
            </div>
        `;
        
        container.appendChild(card);
    });
}

function displayStats(stats, sections) {
    const container = document.getElementById('statsContent');
    
    container.innerHTML = `
        <div class="stats-grid">
            <div class="stat-card">
                <div class="value">${stats.word_count}</div>
                <div class="label">Total Words</div>
            </div>
            <div class="stat-card">
                <div class="value">${stats.keyword_count}</div>
                <div class="label">Keywords Extracted</div>
            </div>
            <div class="stat-card">
                <div class="value">${Object.keys(sections).length}</div>
                <div class="label">Sections Detected</div>
            </div>
            <div class="stat-card">
                <div class="value">${Math.round(stats.ats_score)}%</div>
                <div class="label">ATS Compatibility</div>
            </div>
        </div>
        <div style="margin-top: 30px;">
            <h4 style="margin-bottom: 15px;">Section Breakdown</h4>
            ${Object.entries(sections).map(([section, content]) => `
                <div style="background: var(--bg); padding: 15px; border-radius: 8px; margin-bottom: 10px;">
                    <strong style="text-transform: capitalize; color: var(--primary);">${section}:</strong>
                    <p style="color: var(--text-muted); margin-top: 5px;">
                        ${content.length > 0 ? content.slice(0, 3).join('<br>') + (content.length > 3 ? '...' : '') : 'No content detected'}
                    </p>
                </div>
            `).join('')}
        </div>
    `;
}

function showTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab
    document.getElementById(tabName + 'Tab').classList.add('active');
    event.target.classList.add('active');
}

function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
    
    setTimeout(() => {
        errorDiv.classList.add('hidden');
    }, 5000);
}

// Add gradient definition for SVG
document.addEventListener('DOMContentLoaded', () => {
    const svg = document.querySelector('.score-svg');
    if (svg) {
        const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
        const gradient = document.createElementNS('http://www.w3.org/2000/svg', 'linearGradient');
        gradient.setAttribute('id', 'gradient');
        gradient.setAttribute('x1', '0%');
        gradient.setAttribute('y1', '0%');
        gradient.setAttribute('x2', '100%');
        gradient.setAttribute('y2', '100%');
        
        const stop1 = document.createElementNS('http://www.w3.org/2000/svg', 'stop');
        stop1.setAttribute('offset', '0%');
        stop1.setAttribute('stop-color', '#6366f1');
        const stop2 = document.createElementNS('http://www.w3.org/2000/svg', 'stop');
        stop2.setAttribute('offset', '100%');
        stop2.setAttribute('stop-color', '#8b5cf6');
        
        gradient.appendChild(stop1);
        gradient.appendChild(stop2);
        defs.appendChild(gradient);
        svg.appendChild(defs);
    }
});

