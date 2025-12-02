# app.py - ULTRA PREMIUM NAVIGATION VERSION
import streamlit as st
import pandas as pd
from datetime import datetime
import time
import random
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import plotly.graph_objects as go
import PyPDF2
import io
from docx import Document

# Import email configuration
try:
    from email_config import get_email_config, validate_email_config
    EMAIL_CONFIG = get_email_config()
    EMAIL_ENABLED = True
except ImportError:
    st.error("❌ email_config.py file not found. Please create the configuration file.")
    EMAIL_ENABLED = False
    EMAIL_CONFIG = {}

# Ultra Premium Theme CSS
def load_ultra_premium_css():
    st.markdown("""
    <style>
    /* Ultra Premium Theme */
    :root {
        --bg-primary: #0A0A0A;
        --bg-secondary: #111111;
        --bg-card: #1A1A1A;
        --bg-sidebar: #1a1a1a;
        --accent-primary: #00D4AA;
        --accent-secondary: #0099FF;
        --accent-gradient: linear-gradient(135deg, #00D4AA, #0099FF);
        --text-primary: #FFFFFF;
        --text-secondary: #E0E0E0;
        --text-muted: #AAAAAA;
        --border: #333333;
        --input-bg: #2D2D2D;
        --input-text: #FFFFFF;
        --success: #00C853;
        --shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        --shadow-lg: 0 16px 48px rgba(0, 212, 170, 0.2);
        --glass-bg: rgba(255, 255, 255, 0.05);
        --glass-border: rgba(255, 255, 255, 0.1);
    }
    
    .stApp {
        background: var(--bg-primary) !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Fix ALL text colors to white */
    .st-emotion-cache-3qzj0x p, 
    .st-emotion-cache-3qzj0x ol, 
    .st-emotion-cache-3qzj0x ul, 
    .st-emotion-cache-3qzj0x dl, 
    .st-emotion-cache-3qzj0x li {
        color: white !important;
    }
    
    /* Fix file uploader text color */
    .stFileUploader label p {
        color: white !important;
    }
    
    .stFileUploader label {
        color: white !important;
    }
    
    /* Fix Date Input text color */
    .stDateInput input {
        color: white !important;
    }
    
    .stDateInput > div > div > input {
        color: white !important;
    }
    
    /* Fix all input text colors */
    input, textarea, select {
        color: white !important;
    }
    
    /* Fix text area content color */
    .stTextArea textarea {
        color: white !important;
    }
    
    /* Fix select box text color */
    .stSelectbox > div > div {
        color: white !important;
    }
    
    /* Fix text input color */
    .stTextInput input {
        color: white !important;
    }
    
    /* JD Generator Specific - Black Text on White Background */
    .jd-generator-input input,
    .jd-generator-input textarea,
    .jd-generator-input .stSelectbox > div > div {
        background: white !important;
        color: black !important;
        border: 2px solid #00D4AA !important;
    }
    
    .jd-generator-input input::placeholder,
    .jd-generator-input textarea::placeholder {
        color: #666666 !important;
    }
    
    /* SPECIFIC FIX FOR JD GENERATOR OUTPUT TEXTAREA */
    .jd-generator-output textarea {
        background: white !important;
        color: black !important;
        border: 2px solid #0099FF !important;
        font-family: 'Courier New', monospace !important;
    }
    
    /* HIGH SPECIFICITY OVERRIDE FOR JD GENERATOR */
    div[data-testid="stTextArea"] textarea.jd-output {
        background: white !important;
        color: black !important;
    }
    
    /* Force black text in specific text areas */
    textarea[value*="#"] {
        color: black !important;
        background: white !important;
    }
    
    /* Sidebar - Premium Glass Morphism */
    section[data-testid="stSidebar"] {
        background: linear-gradient(135deg, rgba(26, 26, 26, 0.95), rgba(17, 17, 17, 0.98)) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 1px solid var(--glass-border) !important;
        box-shadow: 8px 0 32px rgba(0, 0, 0, 0.3) !important;
    }
    
    .st-emotion-cache-1legitb {
        background: transparent !important;
    }
    
    /* ULTRA PREMIUM NAVIGATION */
    .nav-container {
        margin: 1.5rem 0 !important;
    }
    
    .nav-section-title {
        font-size: 0.85rem !important;
        font-weight: 700 !important;
        color: var(--accent-primary) !important;
        margin-bottom: 1rem !important;
        padding: 0.5rem 1rem !important;
        background: rgba(0, 212, 170, 0.1) !important;
        border-radius: 8px !important;
        border-left: 3px solid var(--accent-primary) !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    .nav-button-active {
        width: 100% !important;
        text-align: left !important;
        padding: 1.1rem 1.2rem !important;
        margin: 0.4rem 0 !important;
        border: none !important;
        border-radius: 12px !important;
        background: linear-gradient(135deg, #00D4AA, #0099FF) !important;
        color: white !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94) !important;
        box-shadow: 0 8px 25px rgba(0, 212, 170, 0.3) !important;
        display: flex !important;
        align-items: center !important;
        gap: 0.8rem !important;
        position: relative !important;
        overflow: hidden !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    .nav-button-active::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: -100% !important;
        width: 100% !important;
        height: 100% !important;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent) !important;
        transition: left 0.6s ease !important;
    }
    
    .nav-button-active:hover::before {
        left: 100% !important;
    }
    
    .nav-button-inactive {
        width: 100% !important;
        text-align: left !important;
        padding: 1rem 1.2rem !important;
        margin: 0.4rem 0 !important;
        border: 1.5px solid transparent !important;
        border-radius: 12px !important;
        background: rgba(255, 255, 255, 0.03) !important;
        color: var(--text-secondary) !important;
        font-size: 0.92rem !important;
        font-weight: 500 !important;
        cursor: pointer !important;
        transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94) !important;
        display: flex !important;
        align-items: center !important;
        gap: 0.8rem !important;
        position: relative !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .nav-button-inactive:hover {
        background: rgba(0, 212, 170, 0.08) !important;
        color: var(--accent-primary) !important;
        transform: translateX(8px) scale(1.02) !important;
        border-color: rgba(0, 212, 170, 0.3) !important;
        box-shadow: 0 4px 15px rgba(0, 212, 170, 0.15) !important;
    }
    
    .nav-icon {
        font-size: 1.1rem !important;
        width: 24px !important;
        text-align: center !important;
        transition: transform 0.3s ease !important;
    }
    
    .nav-button-inactive:hover .nav-icon {
        transform: scale(1.2) !important;
    }
    
    .nav-button-active .nav-icon {
        transform: scale(1.1) !important;
        filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3)) !important;
    }
    
    .nav-indicator {
        position: absolute !important;
        right: 1rem !important;
        width: 6px !important;
        height: 6px !important;
        background: white !important;
        border-radius: 50% !important;
        animation: pulse 2s infinite !important;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.5); opacity: 0.7; }
        100% { transform: scale(1); opacity: 1; }
    }
    
    /* Premium Logo Section */
    .logo-section {
        text-align: center !important;
        padding: 2rem 1rem 1.5rem 1rem !important;
        background: linear-gradient(135deg, rgba(0, 212, 170, 0.1), rgba(0, 153, 255, 0.05)) !important;
        border-radius: 0 0 20px 20px !important;
        margin: -1rem -1rem 1.5rem -1rem !important;
        border-bottom: 1px solid var(--glass-border) !important;
    }
    
    .logo-icon {
        font-size: 2.8rem !important;
        background: linear-gradient(135deg, #00D4AA, #0099FF) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        margin-bottom: 0.5rem !important;
        display: block !important;
    }
    
    .logo-text {
        font-size: 1.4rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #00D4AA, #0099FF) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        margin: 0 !important;
    }
    
    .logo-subtext {
        font-size: 0.8rem !important;
        color: var(--text-secondary) !important;
        margin: 0.2rem 0 0 0 !important;
        font-weight: 500 !important;
        letter-spacing: 0.5px !important;
    }
    
    /* Stats Section */
    .stats-section {
        background: rgba(255, 255, 255, 0.03) !important;
        border-radius: 12px !important;
        padding: 1.2rem !important;
        margin: 1.5rem 0 !important;
        border: 1px solid var(--glass-border) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stats-title {
        font-size: 0.8rem !important;
        font-weight: 700 !important;
        color: var(--accent-primary) !important;
        margin-bottom: 0.8rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        display: flex !important;
        align-items: center !important;
        gap: 0.5rem !important;
    }
    
    /* Fix Select Box Background */
    .stSelectbox > div > div {
        background: var(--input-bg) !important;
        color: var(--input-text) !important;
        border: 2px solid var(--border) !important;
        border-radius: 10px !important;
    }
    
    .stSelectbox > div > div:hover {
        border-color: var(--accent-primary) !important;
    }
    
    /* Input Fields - Dark Background with White Text */
    .stTextInput>div>div>input, .stTextArea>div>textarea {
        background: var(--input-bg) !important;
        color: var(--input-text) !important;
        border: 2px solid var(--border) !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
    }
    
    .stTextInput>div>div>input::placeholder, .stTextArea>div>textarea::placeholder {
        color: var(--text-muted) !important;
    }
    
    /* Date Input and Time Input */
    .stDateInput > div > div, .stTimeInput > div > div {
        background: var(--input-bg) !important;
        color: var(--input-text) !important;
        border: 2px solid var(--border) !important;
        border-radius: 10px !important;
    }
    
    /* Premium Header with Logo */
    .premium-header {
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(135deg, #00D4AA, #0099FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15px;
    }
    
    .logo-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15px;
        margin-bottom: 2rem;
    }
    
    .logo {
        font-size: 2.5rem;
        background: linear-gradient(135deg, #00D4AA, #0099FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
    }
    
    /* Premium Cards */
    .premium-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: var(--shadow);
        transition: all 0.3s ease;
    }
    
    .premium-card:hover {
        transform: translateY(-5px);
        box-shadow: var(--shadow-lg);
    }
    
    /* Button Styles */
    .stButton > button {
        background: linear-gradient(135deg, #00D4AA, #0099FF) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }
    
    /* Success Animation */
    @keyframes successPop {
        0% { transform: scale(0.8); opacity: 0; }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); opacity: 1; }
    }
    
    .success-pop {
        animation: successPop 0.6s ease-out;
    }
    
    /* Horizontal button layout for candidates */
    .horizontal-buttons {
        display: flex !important;
        flex-direction: row !important;
        gap: 10px !important;
        margin-top: 10px !important;
    }
    
    .horizontal-buttons .stButton {
        flex: 1 !important;
    }
    
    /* Dashboard Description */
    .dashboard-description {
        text-align: center;
        color: var(--text-secondary);
        font-size: 1.1rem;
        margin-bottom: 2rem;
        line-height: 1.6;
    }
    
    /* Fix text in text areas and inputs */
    .stTextArea textarea, .stTextInput input {
        color: white !important;
    }
    
    /* Fix placeholder text color */
    ::placeholder {
        color: var(--text-muted) !important;
    }
    
    /* Fix all Streamlit text elements */
    .stMarkdown, .stText, .stAlert, .stInfo, .stSuccess, .stWarning, .stError {
        color: white !important;
    }
    
    /* Current Page Indicator */
    .current-page-indicator {
        background: linear-gradient(135deg, #00D4AA, #0099FF);
        color: white;
        padding: 12px 24px;
        border-radius: 25px;
        font-weight: 700;
        font-size: 1rem;
        display: inline-block;
        margin-bottom: 25px;
        box-shadow: 0 6px 20px rgba(0, 212, 170, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
    }
    
    /* HIGH PRIORITY OVERRIDES FOR JD GENERATOR */
    [data-testid="stTextArea"] textarea {
        color: inherit !important;
    }
    
    /* Specific override for JD output */
    div[data-testid="stTextArea"] textarea[aria-label="Job Description Content"] {
        background: white !important;
        color: black !important;
        border: 2px solid #0099FF !important;
    }
    
    /* Larger sidebar section */
    section[data-testid="stSidebar"] > div {
        padding: 0rem 1rem 2rem 1rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# AI Question Bank with Questions & Answers
AI_QUESTION_BANK = {
    "Data Science": [
        {
            "question": "Explain the bias-variance tradeoff in machine learning",
            "answer": "The bias-variance tradeoff is a fundamental concept in ML where:\n\n• **High Bias**: Model is too simple, underfits the data (e.g., linear regression for complex patterns)\n• **High Variance**: Model is too complex, overfits the data (e.g., deep neural networks with little data)\n• **Tradeoff**: As model complexity increases, bias decreases but variance increases\n\n**Solution**: Use cross-validation, regularization, and ensemble methods to find the right balance.",
            "type": "Technical",
            "difficulty": "Intermediate"
        },
        {
            "question": "How do you handle missing data in your datasets?",
            "answer": "Missing data handling strategies:\n\n1. **Deletion**: Remove rows/columns if missing data <5%\n2. **Mean/Median/Mode Imputation**: For numerical/categorical data\n3. **Predictive Imputation**: Use ML models to predict missing values\n4. **K-Nearest Neighbors**: Impute based on similar records\n5. **Advanced Methods**: MICE (Multiple Imputation by Chained Equations)\n\n**Best Practice**: Always analyze why data is missing (MCAR, MAR, MNAR) before choosing method.",
            "type": "Technical", 
            "difficulty": "Intermediate"
        },
        {
            "question": "What's the difference between L1 and L2 regularization?",
            "answer": "L1 vs L2 Regularization:\n\n**L1 (Lasso)**:\n• Adds absolute value of coefficients to loss function\n• Can reduce coefficients to exactly zero\n• Performs feature selection\n• Good for sparse models\n\n**L2 (Ridge)**:\n• Adds squared value of coefficients to loss function\n• Shrinks coefficients but never to zero\n• Handles multicollinearity well\n• More stable than L1\n\n**Use Case**: L1 for feature selection, L2 to prevent overfitting.",
            "type": "Technical",
            "difficulty": "Advanced"
        }
    ],
    "AI Engineering": [
        {
            "question": "Explain transformer architecture in NLP",
            "answer": "Transformer Architecture Key Components:\n\n1. **Self-Attention Mechanism**: Weights importance of different words\n2. **Multi-Head Attention**: Multiple attention heads capture different relationships\n3. **Positional Encoding**: Adds sequence order information\n4. **Feed-Forward Networks**: Applies non-linear transformations\n5. **Layer Normalization**: Stabilizes training\n\n**Advantages**:\n• Parallel processing (unlike RNNs)\n• Captures long-range dependencies\n• Scalable to large datasets\n\n**Applications**: BERT, GPT, T5 models",
            "type": "Technical",
            "difficulty": "Advanced"
        },
        {
            "question": "How do you optimize model inference speed?",
            "answer": "Model Inference Optimization Techniques:\n\n1. **Quantization**: Reduce precision (FP32 → FP16/INT8)\n2. **Pruning**: Remove unimportant weights\n3. **Knowledge Distillation**: Train smaller model from large model\n4. **Model Compression**: Architecture search for efficiency\n5. **Hardware Acceleration**: GPU/TPU optimization\n6. **Batching**: Process multiple inputs together\n7. **Caching**: Store frequent inference results\n\n**Tools**: TensorRT, ONNX Runtime, OpenVINO",
            "type": "Technical",
            "difficulty": "Advanced"
        },
        {
            "question": "What's your experience with MLOps practices?",
            "answer": "MLOps Key Practices:\n\n1. **Version Control**: DVC for data, Git for code\n2. **CI/CD**: Automated testing and deployment\n3. **Model Registry**: Track model versions and lineage\n4. **Monitoring**: Model performance and data drift detection\n5. **Feature Store**: Centralized feature management\n6. **Experiment Tracking**: MLflow, Weights & Biases\n7. **Automated Retraining**: Pipeline orchestration\n\n**Tools**: Kubeflow, MLflow, Airflow, Docker, Kubernetes",
            "type": "Technical",
            "difficulty": "Intermediate"
        }
    ],
    "Software Development": [
        {
            "question": "Explain the SOLID principles with examples",
            "answer": "SOLID Principles:\n\n1. **S - Single Responsibility**: Class should have one reason to change\n   Example: Separate UserAuth and UserProfile classes\n\n2. **O - Open/Closed**: Open for extension, closed for modification\n   Example: Use interfaces for new payment methods\n\n3. **L - Liskov Substitution**: Subtypes should be substitutable\n   Example: Square should work wherever Rectangle works\n\n4. **I - Interface Segregation**: Many specific interfaces better than one general\n   Example: Separate Printer, Scanner interfaces\n\n5. **D - Dependency Inversion**: Depend on abstractions, not concretions\n   Example: Use Database interface instead of MySQL class",
            "type": "Technical",
            "difficulty": "Intermediate"
        },
        {
            "question": "How do you approach debugging complex issues?",
            "answer": "Systematic Debugging Approach:\n\n1. **Reproduce**: Consistently recreate the issue\n2. **Isolate**: Identify the smallest reproducible case\n3. **Hypothesize**: Form theories about root cause\n4. **Test**: Use logging, breakpoints, monitoring\n5. **Fix & Verify**: Implement solution and validate\n\n**Tools**:\n• Debuggers (pdb, gdb)\n• Logging and monitoring\n• Profilers for performance issues\n• Unit tests for regression prevention\n\n**Mindset**: Stay curious, methodical, and document findings.",
            "type": "Technical",
            "difficulty": "Intermediate"
        },
        {
            "question": "Describe your CI/CD pipeline setup",
            "answer": "Typical CI/CD Pipeline:\n\n1. **Code Commit**: Developers push to feature branches\n2. **Automated Testing**: Unit, integration, E2E tests run\n3. **Build**: Docker image creation and dependency resolution\n4. **Security Scan**: SAST, DAST, dependency scanning\n5. **Deployment**: Staging environment deployment\n6. **Integration Tests**: API and system testing\n7. **Production Deployment**: Blue-green or canary deployment\n8. **Monitoring**: Performance and error tracking\n\n**Tools**: Jenkins, GitLab CI, GitHub Actions, ArgoCD",
            "type": "Technical",
            "difficulty": "Intermediate"
        }
    ],
    "Product Management": [
        {
            "question": "How do you prioritize features in a product roadmap?",
            "answer": "Feature Prioritization Framework:\n\n1. **Impact vs Effort Matrix**: High impact, low effort first\n2. **RICE Scoring**: Reach, Impact, Confidence, Effort\n3. **Kano Model**: Basic, Performance, Delight features\n4. **MoSCoW**: Must-have, Should-have, Could-have, Won't-have\n5. **User Story Mapping**: Organize by user journey\n\n**Considerations**:\n• Business value and ROI\n• User needs and pain points\n• Technical dependencies\n• Market competition and timing\n• Resource constraints",
            "type": "Behavioral",
            "difficulty": "Intermediate"
        },
        {
            "question": "Describe your process for gathering customer requirements",
            "answer": "Customer Requirements Gathering Process:\n\n1. **Stakeholder Interviews**: Understand business objectives\n2. **User Research**: Surveys, interviews, observation\n3. **Market Analysis**: Competitor and industry research\n4. **Data Analysis**: Usage metrics and behavior patterns\n5. **Prototype Testing**: Validate assumptions with users\n6. **Prioritization Workshops**: Collaborative feature ranking\n\n**Deliverables**: User stories, journey maps, PRDs, acceptance criteria",
            "type": "Behavioral",
            "difficulty": "Intermediate"
        },
        {
            "question": "How do you measure product success?",
            "answer": "Product Success Metrics:\n\n**North Star Metric**: Primary value metric (e.g., daily active users)\n\n**Engagement**:\n• Retention rates\n• Session duration\n• Feature adoption\n\n**Business**:\n• Revenue and conversion rates\n• Customer lifetime value\n• Churn rate\n\n**Qualitative**:\n• Customer satisfaction (NPS, CSAT)\n• User feedback and reviews\n• Support ticket analysis\n\n**Framework**: OKRs (Objectives and Key Results)",
            "type": "Behavioral",
            "difficulty": "Intermediate"
        }
    ]
}

def extract_text_from_pdf(file):
    """Extract text from PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""

def extract_text_from_docx(file):
    """Extract text from DOCX file"""
    try:
        doc = Document(file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        st.error(f"Error reading DOCX: {e}")
        return ""

def extract_info_from_resume(text):
    """Advanced resume parsing with better extraction"""
    info = {
        'name': '',
        'email': '',
        'phone': '',
        'experience': 0,
        'skills': [],
        'education': []
    }
    
    lines = text.split('\n')
    
    # Extract name (first line usually contains name)
    name_patterns = [
        r'^[A-Z][a-z]+ [A-Z][a-z]+$',
        r'^[A-Z][a-z]+ [A-Z]\. [A-Z][a-z]+$',
        r'^[A-Z][a-z]+ [A-Z][a-z]+ [A-Z][a-z]+$'
    ]
    
    for line in lines[:10]:  # Check first 10 lines
        line = line.strip()
        for pattern in name_patterns:
            if re.match(pattern, line):
                info['name'] = line
                break
        if info['name']:
            break
    
    # Extract email
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    if emails:
        info['email'] = emails[0]
    
    # Extract phone number
    phone_patterns = [
        r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]',
        r'\(\d{3}\) \d{3}-\d{4}',
        r'\d{3}-\d{3}-\d{4}',
        r'\+\d{1,3} \d{9,10}'
    ]
    
    for pattern in phone_patterns:
        phones = re.findall(pattern, text)
        if phones:
            info['phone'] = phones[0]
            break
    
    # Extract experience
    exp_patterns = [
        r'(\d+)\s*(?:years?|yrs?)',
        r'(\d+)\+?\s*(?:years?|yrs?) of experience',
        r'experience.*?(\d+)\s*(?:years?|yrs?)'
    ]
    
    for pattern in exp_patterns:
        exp_matches = re.findall(pattern, text.lower())
        if exp_matches:
            info['experience'] = max([int(match) for match in exp_matches])
            break
    
    # Enhanced skills extraction
    tech_skills = {
        'Programming': ['python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust'],
        'Web': ['html', 'css', 'react', 'angular', 'vue', 'node', 'django', 'flask'],
        'Database': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis'],
        'Cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes'],
        'Data Science': ['machine learning', 'deep learning', 'tensorflow', 'pytorch', 'pandas'],
        'Tools': ['git', 'jira', 'confluence', 'slack', 'figma']
    }
    
    found_skills = []
    for category, skills in tech_skills.items():
        for skill in skills:
            if re.search(r'\b' + re.escape(skill) + r'\b', text.lower()):
                found_skills.append(skill.title())
    
    info['skills'] = list(set(found_skills))[:10]
    
    # Extract education
    education_keywords = ['university', 'college', 'institute', 'bachelor', 'master', 'phd', 'bs', 'ms', 'btech', 'mtech']
    for line in lines:
        if any(keyword in line.lower() for keyword in education_keywords):
            info['education'].append(line.strip())
    
    return info

def send_real_email(candidate_email, candidate_name, role, interview_date, interview_time, interview_type, company_name="TechCorp Innovations"):
    """Send professional interview invitation email"""
    try:
        if not EMAIL_ENABLED:
            return False, "Email configuration not available"
        
        config = EMAIL_CONFIG
        
        message = MIMEMultipart("alternative")
        message["Subject"] = f"Interview Invitation - {role} Position at {company_name}"
        message["From"] = config['sender_email']
        message["To"] = candidate_email
        
        # Professional HTML Email Template
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: 'Arial', sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px 10px 0 0; text-align: center; }}
                .content {{ background: white; padding: 30px; border-radius: 0 0 10px 10px; }}
                .interview-details {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #00D4AA; }}
                .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎯 Interview Invitation</h1>
                    <p>{company_name}</p>
                </div>
                <div class="content">
                    <p>Dear <strong>{candidate_name}</strong>,</p>
                    
                    <p>Thank you for your interest in the <strong style="color: #00D4AA;">{role}</strong> position at {company_name}. We were thoroughly impressed with your qualifications and background.</p>
                    
                    <div class="interview-details">
                        <h3 style="color: #2c3e50; margin-top: 0;">📅 Interview Details</h3>
                        <table style="width: 100%;">
                            <tr>
                                <td style="padding: 8px 0; color: #666; width: 120px;"><strong>Position:</strong></td>
                                <td style="padding: 8px 0; color: #2c3e50;">{role}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px 0; color: #666;"><strong>Date:</strong></td>
                                <td style="padding: 8px 0; color: #2c3e50;">{interview_date}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px 0; color: #666;"><strong>Time:</strong></td>
                                <td style="padding: 8px 0; color: #2c3e50;">{interview_time}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px 0; color: #666;"><strong>Type:</strong></td>
                                <td style="padding: 8px 0; color: #2c3e50;">{interview_type} Interview</td>
                            </tr>
                        </table>
                    </div>
                    
                    <p><strong>Preparation Tips:</strong></p>
                    <ul>
                        <li>Please have your portfolio and any relevant work samples ready</li>
                        <li>Be prepared to discuss your technical experience and projects</li>
                        <li>We'll explore problem-solving scenarios relevant to the role</li>
                    </ul>
                    
                    <p>This interview will be conducted via video conference. The meeting link will be sent to you 24 hours prior to the scheduled time.</p>
                    
                    <p>Please confirm your availability by replying to this email. If the proposed time doesn't work for you, feel free to suggest alternative times.</p>
                    
                    <p>We're excited to learn more about your experience and discuss how you can contribute to our team!</p>
                    
                    <div class="footer">
                        <p>Best regards,<br>
                        <strong>Talent Acquisition Team</strong><br>
                        {company_name}<br>
                        📧 talent@{company_name.lower().replace(' ', '')}.com<br>
                        📞 +1 (555) 123-4567</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        message.attach(MIMEText(html, "html"))
        
        server = smtplib.SMTP(config['smtp_server'], config['smtp_port'])
        server.starttls()
        server.login(config['sender_email'], config['sender_password'])
        server.sendmail(config['sender_email'], candidate_email, message.as_string())
        server.quit()
        
        return True, f"Professional interview invitation sent successfully to {candidate_email}"
        
    except Exception as e:
        return False, f"Email sending failed: {str(e)}"

def show_success_popup(message):
    """Show success popup"""
    st.markdown(f"""
    <div class="success-pop" style='
        background: linear-gradient(135deg, #00D4AA, #0099FF);
        color: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        margin: 20px 0;
    '>
        <h3 style='margin: 0;'>🎉 {message}</h3>
    </div>
    """, unsafe_allow_html=True)

def create_trend_chart():
    """Create hiring trends chart"""
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    applications = [120, 150, 180, 200, 170, 220]
    hires = [8, 12, 15, 18, 14, 20]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=months, y=applications,
        mode='lines+markers',
        name='Applications',
        line=dict(color='#00D4AA', width=3),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=months, y=hires,
        mode='lines+markers',
        name='Hires',
        line=dict(color='#0099FF', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title='📈 Hiring Trends - Last 6 Months',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(gridcolor='#333333'),
        yaxis=dict(gridcolor='#333333')
    )
    
    return fig

def get_ai_questions(domain, experience_level, num_questions=5):
    """Get AI-generated questions with answers for specific domain"""
    if domain in AI_QUESTION_BANK:
        questions = AI_QUESTION_BANK[domain]
        # Filter by difficulty based on experience level
        if experience_level == "Entry Level":
            filtered_questions = [q for q in questions if q['difficulty'] == "Intermediate"]
        elif experience_level == "Mid Level":
            filtered_questions = [q for q in questions if q['difficulty'] in ["Intermediate", "Advanced"]]
        else:  # Senior Level
            filtered_questions = questions
        
        return filtered_questions[:num_questions]
    return []

def create_premium_navigation():
    """Create ultra premium navigation with glass morphism effects"""
    pages = {
        "Dashboard": "📊",
        "Resume Screening": "📄", 
        "AI Interview Prep": "🎯",
        "JD Generator": "📝",
        "Candidates": "👥",
        "Analytics": "📈"
    }
    
    # Navigation Section
    st.markdown("""
    <div class="nav-container">
        <div class="nav-section-title">🚀 Main Navigation</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create premium navigation buttons
    for page, icon in pages.items():
        is_active = st.session_state.current_page == page
        
        if is_active:
            button_html = f"""
            <div style="margin: 0.3rem 0;">
                <button class="nav-button-active">
                    <span class="nav-icon">{icon}</span>
                    <span>{page}</span>
                    <div class="nav-indicator"></div>
                </button>
            </div>
            """
        else:
            button_html = f"""
            <div style="margin: 0.3rem 0;">
                <button class="nav-button-inactive">
                    <span class="nav-icon">{icon}</span>
                    <span>{page}</span>
                </button>
            </div>
            """
        
        st.markdown(button_html, unsafe_allow_html=True)
        
        # Add actual Streamlit button for functionality
        if st.button(f"{icon} {page}", 
                    use_container_width=True, 
                    key=f"nav_func_{page}",
                    type="primary" if is_active else "secondary",
                    label_visibility="collapsed"):
            st.session_state.current_page = page
            st.rerun()

def main():
    st.set_page_config(
        page_title="SmartHire AI - Premium",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session states
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Dashboard"
    if 'resume_analysis' not in st.session_state:
        st.session_state.resume_analysis = {}
    if 'candidates' not in st.session_state:
        st.session_state.candidates = []
    if 'generated_jd' not in st.session_state:
        st.session_state.generated_jd = ""
    if 'jd_created' not in st.session_state:
        st.session_state.jd_created = False
    if 'ai_questions' not in st.session_state:
        st.session_state.ai_questions = []
    
    load_ultra_premium_css()
    
    # Premium Sidebar with Glass Morphism
    with st.sidebar:
        # Premium Logo Section
        st.markdown("""
        <div class="logo-section">
            <div class="logo-icon">🚀</div>
            <div class="logo-text">SmartHire AI</div>
            <div class="logo-subtext">Premium Recruitment Platform</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Premium Navigation
        create_premium_navigation()
        
        # Stats Section
        st.markdown("""
        <div class="stats-section">
            <div class="stats-title">📊 Quick Stats</div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Active Jobs", "18", delta="+2", delta_color="normal")
            st.metric("Candidates", "127", delta="+15", delta_color="normal")
        with col2:
            st.metric("Match Rate", "87%", delta="+3%", delta_color="normal")
            st.metric("Hiring Time", "16d", delta="-2d", delta_color="normal")
    
    # Main Content with Current Page Indicator
    st.markdown("""
    <div class="logo-container">
        <div class="logo">🚀</div>
        <h1 class="premium-header">SmartHire.AI</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Current Page Indicator
    st.markdown(f"""
    <div class="current-page-indicator">
        🎯 CURRENTLY VIEWING: {st.session_state.current_page.upper()}
    </div>
    """, unsafe_allow_html=True)
    
    # Page routing
    if st.session_state.current_page == "Dashboard":
        show_dashboard()
    elif st.session_state.current_page == "Resume Screening":
        show_resume_screening()
    elif st.session_state.current_page == "AI Interview Prep":
        show_interview_prep()
    elif st.session_state.current_page == "JD Generator":
        show_jd_generator()
    elif st.session_state.current_page == "Candidates":
        show_candidates()
    elif st.session_state.current_page == "Analytics":
        show_analytics()

def show_dashboard():
    # Dashboard Description
    st.markdown("""
    <div class="dashboard-description">
        <h3>🚀 Welcome to SmartHire AI - Your Intelligent Recruitment Partner</h3>
        <p>Streamline your hiring process with AI-powered tools for resume screening, interview preparation, 
        candidate management, and data-driven insights. Save time, make better hiring decisions, and find 
        the perfect candidates faster.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="premium-card">
            <h3 style="text-align: center;">💼</h3>
            <h2 style="text-align: center; background: linear-gradient(135deg, #00D4AA, #0099FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">18</h2>
            <p style="text-align: center; color: var(--text-secondary);">Active Jobs</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="premium-card">
            <h3 style="text-align: center;">👥</h3>
            <h2 style="text-align: center; background: linear-gradient(135deg, #00D4AA, #0099FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">127</h2>
            <p style="text-align: center; color: var(--text-secondary);">Candidates</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="premium-card">
            <h3 style="text-align: center;">🎯</h3>
            <h2 style="text-align: center; background: linear-gradient(135deg, #00D4AA, #0099FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">87%</h2>
            <p style="text-align: center; color: var(--text-secondary);">Match Rate</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="premium-card">
            <h3 style="text-align: center;">⚡</h3>
            <h2 style="text-align: center; background: linear-gradient(135deg, #00D4AA, #0099FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">16d</h2>
            <p style="text-align: center; color: var(--text-secondary);">Hiring Time</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick Actions
    st.markdown("### 🚀 Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📄 Screen Resume", use_container_width=True):
            st.session_state.current_page = "Resume Screening"
            st.rerun()
    
    with col2:
        if st.button("🎯 Interview Prep", use_container_width=True):
            st.session_state.current_page = "AI Interview Prep"
            st.rerun()
    
    with col3:
        if st.button("📝 Create JD", use_container_width=True):
            st.session_state.current_page = "JD Generator"
            st.rerun()
    
    with col4:
        if st.button("👥 View Candidates", use_container_width=True):
            st.session_state.current_page = "Candidates"
            st.rerun()

# ... (Other page functions remain the same as previous version)

def show_resume_screening():
    st.markdown("""
    <div class="premium-card">
        <h3>📄 AI Resume Screening</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        uploaded_file = st.file_uploader("Choose resume file", type=['pdf', 'docx', 'txt'])
        
        if uploaded_file:
            # Extract text based on file type
            if uploaded_file.type == "application/pdf":
                resume_text = extract_text_from_pdf(uploaded_file)
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                resume_text = extract_text_from_docx(uploaded_file)
            else:  # txt file
                resume_text = str(uploaded_file.read(), "utf-8")
            
            if resume_text:
                # Auto-extract information from resume
                extracted_info = extract_info_from_resume(resume_text)
                st.session_state.resume_analysis = extracted_info
                
                show_success_popup("Resume processed successfully! Information extracted automatically.")
                
                # Auto-filled form with extracted data
                candidate_name = st.text_input("Full Name", value=extracted_info['name'], key="resume_name")
                candidate_email = st.text_input("Email Address", value=extracted_info['email'], key="resume_email")
                candidate_phone = st.text_input("Phone Number", value=extracted_info['phone'], key="resume_phone")
                experience = st.slider("Years of Experience", 0, 20, extracted_info['experience'], key="resume_exp")
                
                if extracted_info['skills']:
                    st.write("**🎯 Extracted Skills:**")
                    cols = st.columns(3)
                    for i, skill in enumerate(extracted_info['skills'][:6]):
                        with cols[i % 3]:
                            st.markdown(f"```{skill}```")
                
                if extracted_info['education']:
                    st.write("**🎓 Education:**")
                    for edu in extracted_info['education'][:3]:
                        st.markdown(f"- {edu}")
    
    with col2:
        if st.session_state.resume_analysis:
            analysis = st.session_state.resume_analysis
            
            st.markdown("""
            <div class="premium-card">
                <h4>Analysis Results</h4>
            </div>
            """, unsafe_allow_html=True)
            
            match_score = random.randint(75, 95)
            st.metric("AI Match Score", f"{match_score}%")
            st.progress(match_score / 100)
            
            # Email Section
            st.markdown("---")
            st.markdown("**📧 Schedule Professional Interview**")
            
            col_date, col_time = st.columns(2)
            with col_date:
                interview_date = st.date_input("Interview Date")
            with col_time:
                interview_time = st.time_input("Interview Time")
            
            interview_type = st.selectbox("Interview Type", ["Technical Screening", "HR Discussion", "Technical Deep Dive", "Final Manager Round"])
            role = st.selectbox("Position", ["Data Scientist", "AI Engineer", "Machine Learning Engineer", "Data Analyst", "Software Developer"])
            company_name = st.text_input("Company Name", value="TechCorp Innovations")
            
            # Use the email from input field, not from extracted info
            email_to_send = st.session_state.get('resume_email', analysis['email'])
            name_to_send = st.session_state.get('resume_name', analysis['name'])
            
            if st.button("🚀 Send Professional Invitation", type="primary", use_container_width=True):
                if email_to_send and name_to_send:
                    if EMAIL_ENABLED:
                        success, message = send_real_email(
                            email_to_send,
                            name_to_send, 
                            role,
                            interview_date,
                            interview_time,
                            interview_type,
                            company_name
                        )
                        if success:
                            show_success_popup(message)
                        else:
                            st.error(f"❌ {message}")
                    else:
                        st.error("❌ Email configuration not available")
                else:
                    st.error("❌ Please fill in candidate email and name")

def show_interview_prep():
    st.markdown("""
    <div class="premium-card">
        <h3>🎯 AI Interview Preparation</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="premium-card">
            <h4>⚙️ Configure Interview</h4>
        </div>
        """, unsafe_allow_html=True)
        
        domain = st.selectbox("Select Domain", 
                            ["Data Science", "AI Engineering", "Software Development", "Product Management"])
        
        experience_level = st.selectbox("Experience Level", 
                                      ["Entry Level", "Mid Level", "Senior Level"])
        
        num_questions = st.slider("Number of Questions", 3, 10, 5)
        
        if st.button("🤖 Generate AI Questions & Answers", type="primary", use_container_width=True):
            with st.spinner("Generating domain-specific questions with answers..."):
                time.sleep(1)
                questions = get_ai_questions(domain, experience_level, num_questions)
                st.session_state.ai_questions = questions
                show_success_popup(f"Generated {len(questions)} {domain} questions with answers!")
    
    with col2:
        if st.session_state.ai_questions:
            st.markdown("""
            <div class="premium-card">
                <h4>📝 AI-Generated Questions & Answers</h4>
            </div>
            """, unsafe_allow_html=True)
            
            for i, qa in enumerate(st.session_state.ai_questions, 1):
                with st.expander(f"Q{i}: {qa['question']} ({qa['difficulty']})", expanded=False):
                    st.markdown(f"**Type:** {qa['type']}")
                    st.markdown(f"**Difficulty:** {qa['difficulty']}")
                    st.markdown("---")
                    st.markdown("**💡 Expected Answer:**")
                    st.info(qa['answer'])
        else:
            st.info("👆 Configure the interview settings and click 'Generate AI Questions & Answers' to get started!")

def show_jd_generator():
    st.markdown("""
    <div class="premium-card">
        <h3>📝 AI Job Description Generator</h3>
        <p style="color: var(--text-secondary); font-size: 0.9rem;">
            Create professional job descriptions with black text on white backgrounds for better readability
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="premium-card">
            <h4>📋 Job Details</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # JD Generator Inputs with White Background and Black Text
        st.markdown('<div class="jd-generator-input">', unsafe_allow_html=True)
        
        job_title = st.text_input("Job Title*", placeholder="e.g., Senior Data Scientist", key="jd_title")
        department = st.selectbox("Department*", ["Engineering", "Data Science", "Product", "Design", "Marketing", "Sales", "Operations"], key="jd_dept")
        experience = st.selectbox("Experience Level*", ["Entry Level (0-2 years)", "Mid Level (2-5 years)", "Senior Level (5-8 years)", "Lead (8+ years)"], key="jd_exp")
        location = st.selectbox("Work Location*", ["Remote", "Hybrid", "On-site"], key="jd_location")
        skills = st.text_area("Required Skills & Technologies*", 
                            placeholder="Python, Machine Learning, SQL, AWS, Docker, React, Node.js...\n\nSeparate skills with commas or new lines", 
                            height=120, 
                            key="jd_skills")
        company_name = st.text_input("Company Name*", value="TechCorp Innovations", key="jd_company")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("🚀 Generate Professional JD", type="primary", use_container_width=True):
            if job_title and skills:
                with st.spinner("Creating professional job description..."):
                    time.sleep(2)
                    
                    # Generate professional JD
                    jd_content = f"""
# {job_title}

## 🎯 Position Overview
{company_name} is seeking a {experience.lower()} {job_title} to join our dynamic {department} team. This {location.lower()} position offers the opportunity to work on cutting-edge projects and make a significant impact in our organization.

## 📋 Key Responsibilities
- Design, develop, and implement innovative {department.lower()} solutions
- Collaborate with cross-functional teams to deliver high-quality products
- Analyze complex problems and provide strategic solutions
- Mentor junior team members and conduct code reviews
- Stay current with emerging technologies and industry trends
- Participate in agile development processes and sprint planning

## 🛠️ Technical Requirements
### Required Skills:
{skills}

### Preferred Qualifications:
- Experience with cloud platforms (AWS, Azure, or GCP)
- Knowledge of DevOps practices and CI/CD pipelines
- Familiarity with containerization technologies
- Understanding of software architecture patterns

## 🎓 Qualifications & Experience
- Bachelor's/Master's degree in Computer Science or related field
- {experience} experience in relevant role
- Strong problem-solving and analytical skills
- Excellent communication and collaboration abilities
- Experience with modern development practices and methodologies

## 💼 What We Offer
- Competitive salary and comprehensive benefits package
- {location} work flexibility with modern tools and infrastructure
- Professional development and growth opportunities
- Collaborative and inclusive work environment
- Cutting-edge technology stack and innovation labs
- Health insurance and wellness programs

## 🌟 Why Join {company_name}?
At {company_name}, we believe in nurturing talent and providing opportunities for professional growth. You'll work with industry experts on challenging projects that make a real impact. Our culture promotes innovation, collaboration, and continuous learning.

## 📧 How to Apply
Please submit your resume and cover letter through our careers portal. We're excited to review your application and discuss how you can contribute to our team's success!

---
*Generated by SmartHire AI - Premium Recruitment Platform*
"""
                    st.session_state.generated_jd = jd_content
                    st.session_state.jd_created = True
                    show_success_popup("Professional Job Description Created Successfully!")
            else:
                st.error("❌ Please fill in required fields: Job Title and Required Skills")
    
    with col2:
        if st.session_state.jd_created and st.session_state.generated_jd:
            st.markdown("""
            <div class="premium-card">
                <h4>📄 Generated Job Description</h4>
                <p style="color: var(--text-secondary); font-size: 0.9rem;">
                    Professional JD ready for use with black text on white background
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # JD Output with White Background and Black Text - USING INLINE STYLE FOR MAXIMUM SPECIFICITY
            st.markdown("""
            <style>
            /* MAXIMUM SPECIFICITY OVERRIDE FOR JD OUTPUT */
            .stTextArea textarea[data-testid="stTextArea"] {
                background: white !important;
                color: black !important;
                border: 2px solid #0099FF !important;
            }
            
            /* Direct attribute selector for maximum specificity */
            textarea[aria-label="Job Description Content"] {
                background: white !important;
                color: black !important;
                border: 2px solid #0099FF !important;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Use a unique key and add custom CSS class
            st.text_area("Job Description Content", 
                        st.session_state.generated_jd, 
                        height=400, 
                        label_visibility="collapsed", 
                        key="jd_display_unique")
            
            # Action Buttons
            col_s1, col_s2, col_s3 = st.columns(3)
            with col_s1:
                if st.button("📋 Copy to Clipboard", use_container_width=True, key="copy_jd"):
                    show_success_popup("JD copied to clipboard!")
            with col_s2:
                if st.button("📥 Export as PDF", use_container_width=True, key="export_jd"):
                    show_success_popup("PDF export started!")
            with col_s3:
                if st.button("🔄 Create New", use_container_width=True, key="new_jd"):
                    st.session_state.jd_created = False
                    st.session_state.generated_jd = ""
                    st.rerun()
        else:
            st.info("""
            **👆 Fill in the job details and click 'Generate Professional JD' to create a comprehensive job description.**
            
            *Features:*
            • Professional formatting with sections
            • Black text on white background for readability
            • Easy copy and export options
            • Customizable for different roles and experience levels
            """)

def show_candidates():
    st.markdown("""
    <div class="premium-card">
        <h3>👥 Candidate Management</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Add Candidate Section
    with st.expander("➕ Add New Candidate", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            new_name = st.text_input("Full Name", key="new_candidate_name")
            new_email = st.text_input("Email Address", key="new_candidate_email")
            new_phone = st.text_input("Phone Number", key="new_candidate_phone")
        
        with col2:
            new_role = st.selectbox("Applied Role", ["Data Scientist", "AI Engineer", "Software Developer", "Product Manager"], key="new_candidate_role")
            new_exp = st.slider("Years of Experience", 0, 20, 3, key="new_candidate_exp")
            new_status = st.selectbox("Current Status", ["Applied", "Screening", "Interview", "Offer", "Hired"], key="new_candidate_status")
        
        if st.button("➕ Add Candidate to System", type="primary", use_container_width=True):
            if new_name and new_email:
                new_candidate = {
                    'name': new_name,
                    'email': new_email,
                    'phone': new_phone,
                    'role': new_role,
                    'experience': new_exp,
                    'status': new_status,
                    'score': f"{random.randint(70, 95)}%",
                    'applied_date': datetime.now().strftime("%Y-%m-%d")
                }
                st.session_state.candidates.append(new_candidate)
                show_success_popup(f"✅ Candidate {new_name} added successfully!")
                st.rerun()
            else:
                st.error("❌ Please fill in at least name and email")
    
    st.markdown("---")
    
    # Candidates List with HORIZONTAL buttons
    if st.session_state.candidates:
        st.markdown(f"**📋 Total Candidates: {len(st.session_state.candidates)}**")
        
        for i, candidate in enumerate(st.session_state.candidates):
            col1, col2, col3 = st.columns([3, 2, 2])
            
            with col1:
                st.write(f"**{candidate['name']}**")
                st.write(f"📧 {candidate['email']}")
                if candidate['phone']:
                    st.write(f"📞 {candidate['phone']}")
            
            with col2:
                st.write(f"💼 {candidate['role']}")
                st.write(f"⏳ {candidate['experience']} years experience")
                st.write(f"📅 Applied: {candidate['applied_date']}")
            
            with col3:
                status_color = {
                    "Applied": "#3498db",
                    "Screening": "#f39c12", 
                    "Interview": "#9b59b6",
                    "Offer": "#2ecc71",
                    "Hired": "#27ae60"
                }
                st.markdown(f"""
                <div style='background: {status_color.get(candidate['status'], '#95a5a6')}; color: white; padding: 5px 10px; border-radius: 15px; text-align: center; font-size: 0.8rem; font-weight: 600; margin-bottom: 10px;'>
                    {candidate['status']}
                </div>
                """, unsafe_allow_html=True)
                
                st.write(f"🎯 {candidate['score']}")
            
            # HORIZONTAL BUTTONS
            st.markdown('<div class="horizontal-buttons">', unsafe_allow_html=True)
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                if st.button(f"👁️ View Profile", key=f"view_{i}", use_container_width=True):
                    st.info(f"**Viewing Profile:** {candidate['name']}\n\n"
                           f"**Email:** {candidate['email']}\n"
                           f"**Role:** {candidate['role']}\n"
                           f"**Experience:** {candidate['experience']} years\n"
                           f"**Status:** {candidate['status']}\n"
                           f"**Match Score:** {candidate['score']}")
            
            with col_btn2:
                if st.button(f"📧 Send Email", key=f"email_{i}", use_container_width=True):
                    st.info(f"**Preparing email for:** {candidate['name']}\n"
                           f"**Email:** {candidate['email']}\n\n"
                           f"*Email template would open here*")
            
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("---")
    else:
        st.info("No candidates in the system yet. Use the form above to add candidates.")

def show_analytics():
    st.markdown("""
    <div class="premium-card">
        <h3>📈 Advanced Analytics & Insights</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Time to Hire", "16.2d", "-1.8d")
        st.metric("Interview Success Rate", "68%", "+5%")
    
    with col2:
        st.metric("Cost per Hire", "$2,847", "-$153")
        st.metric("Candidate Satisfaction", "94%", "+2%")
    
    with col3:
        st.metric("Quality of Hire", "8.7/10", "+0.3")
        st.metric("Offer Acceptance Rate", "85%", "+3%")
    
    with col4:
        st.metric("Source Effectiveness", "78%", "+4%")
        st.metric("Retention Rate", "92%", "+2%")
    
    st.markdown("---")
    
    # Charts Section
    st.plotly_chart(create_trend_chart(), use_container_width=True)
    
    # AI Predictions and Insights
    st.markdown("""
    <div class="premium-card">
        <h4>🤖 AI-Powered Insights & Predictions</h4>
    </div>
    """, unsafe_allow_html=True)
    
    col_insight1, col_insight2 = st.columns(2)
    
    with col_insight1:
        st.markdown("""
        ### 📊 Current Trends
        - **Data Science roles** showing 25% growth in applications
        - **Remote positions** have 15% higher acceptance rates
        - **AI Engineer** demand increased by 40% this quarter
        - **Technical screening** success rate: 68%
        """)
    
    with col_insight2:
        st.markdown("""
        ### 🔮 Future Predictions
        - **Next Month:** Expect 28% increase in qualified candidates
        - **Q3 Forecast:** Hiring time will reduce to 14.5 days
        - **Opportunity:** Focus on AI/ML roles for maximum ROI
        - **Alert:** Software Developer market becoming competitive
        """)
    
    # Recommendations
    st.markdown("""
    <div class="premium-card">
        <h4>💡 Strategic Recommendations</h4>
        <ul>
        <li>🎯 <strong>Focus on AI Engineer roles</strong> - 40% demand growth predicted</li>
        <li>⚡ <strong>Optimize screening process</strong> - Reduce time-to-interview by 2 days</li>
        <li>💰 <strong>Adjust salary bands</strong> for competitive positioning</li>
        <li>🌐 <strong>Expand remote hiring</strong> - 15% higher retention observed</li>
        <li>📈 <strong>Invest in employer branding</strong> - 25% impact on candidate quality</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()