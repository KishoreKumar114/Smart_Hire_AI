# app.py - SMART HIRE AI MAIN APPLICATION
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

# Import the login page module
from login_page import show_login_page, check_authentication

# Import email configuration
try:
    from email_config import get_email_config, validate_email_config
    EMAIL_CONFIG = get_email_config()
    EMAIL_ENABLED = True
except ImportError:
    st.error("❌ email_config.py file not found. Please create the configuration file.")
    EMAIL_ENABLED = False
    EMAIL_CONFIG = {}

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
        }
    ],
    "AI Engineering": [
        {
            "question": "Explain transformer architecture in NLP",
            "answer": "Transformer Architecture Key Components:\n\n1. **Self-Attention Mechanism**: Weights importance of different words\n2. **Multi-Head Attention**: Multiple attention heads capture different relationships\n3. **Positional Encoding**: Adds sequence order information\n4. **Feed-Forward Networks**: Applies non-linear transformations\n5. **Layer Normalization**: Stabilizes training\n\n**Advantages**:\n• Parallel processing (unlike RNNs)\n• Captures long-range dependencies\n• Scalable to large datasets\n\n**Applications**: BERT, GPT, T5 models",
            "type": "Technical",
            "difficulty": "Advanced"
        }
    ]
}

# Resume Processing Functions
def extract_text_from_pdf(pdf_file):
    """Extract text from PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def extract_text_from_docx(docx_file):
    """Extract text from DOCX file"""
    try:
        doc = Document(docx_file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        return f"Error reading DOCX: {str(e)}"

def extract_info_from_resume(text):
    """Extract information from resume text"""
    info = {
        "name": "",
        "email": "",
        "phone": "",
        "skills": [],
        "experience": "",
        "education": "",
        "score": 0
    }
    
    # Extract email
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    if emails:
        info["email"] = emails[0]
    
    # Extract phone number
    phone_pattern = r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]'
    phones = re.findall(phone_pattern, text)
    if phones:
        info["phone"] = phones[0]
    
    # Calculate score based on content
    score = 0
    if info["email"]:
        score += 25
    if info["phone"]:
        score += 25
    if len(text) > 100:
        score += 25
    if any(word in text.lower() for word in ["experience", "education", "skills"]):
        score += 25
    
    info["score"] = score
    return info

# Email Functions
def send_real_email(to_email, subject, message):
    """Send real email using SMTP"""
    if not EMAIL_ENABLED:
        return False, "Email configuration not available"
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_CONFIG['smtp_username']
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add body to email
        msg.attach(MIMEText(message, 'plain'))
        
        # Create server
        server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
        server.starttls()
        server.login(EMAIL_CONFIG['smtp_username'], EMAIL_CONFIG['smtp_password'])
        
        # Send email
        text = msg.as_string()
        server.sendmail(EMAIL_CONFIG['smtp_username'], to_email, text)
        server.quit()
        
        return True, "Email sent successfully!"
    except Exception as e:
        return False, f"Failed to send email: {str(e)}"

def show_success_popup():
    """Show success popup animation"""
    st.markdown("""
    <style>
    @keyframes successPop {
        0% { transform: scale(0.8); opacity: 0; }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); opacity: 1; }
    }
    .success-pop {
        animation: successPop 0.6s ease-out;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="success-pop">✅</div>', unsafe_allow_html=True)

# Analytics Functions
def create_trend_chart():
    """Create hiring trend chart"""
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    applications = [45, 52, 48, 67, 75, 82]
    hires = [3, 5, 4, 7, 8, 10]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=months, y=applications, mode='lines+markers', name='Applications', line=dict(color='#00D4AA')))
    fig.add_trace(go.Scatter(x=months, y=hires, mode='lines+markers', name='Hires', line=dict(color='#0099FF')))
    
    fig.update_layout(
        title='Hiring Trends 2024',
        xaxis_title='Months',
        yaxis_title='Count',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        hovermode='x unified'
    )
    
    return fig

def get_ai_questions(role, difficulty="All", num_questions=5):
    """Get AI-generated interview questions"""
    if role not in AI_QUESTION_BANK:
        return []
    
    questions = AI_QUESTION_BANK[role]
    
    # Filter by difficulty if specified
    if difficulty != "All":
        questions = [q for q in questions if q['difficulty'] == difficulty]
    
    # Randomly select questions
    if len(questions) > num_questions:
        questions = random.sample(questions, num_questions)
    
    return questions

# Premium Theme CSS for Main App
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
    }
    
    .stApp {
        background: var(--bg-primary) !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar - Dark Color */
    section[data-testid="stSidebar"] {
        background: var(--bg-sidebar) !important;
        border-right: 1px solid var(--border) !important;
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
    
    /* Current Page Indicator */
    .current-page-indicator {
        background: linear-gradient(135deg, #00D4AA, #0099FF);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        display: inline-block;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0, 212, 170, 0.3);
    }
    
    /* Dashboard Description */
    .dashboard-description {
        text-align: center;
        color: var(--text-secondary);
        font-size: 1.1rem;
        margin-bottom: 2rem;
        line-height: 1.6;
    }
    
    /* Fix all text colors */
    .stMarkdown, .stText, .stAlert, .stInfo, .stSuccess, .stWarning, .stError {
        color: white !important;
    }
    
    /* Input field fixes */
    .stTextInput>div>div>input, .stTextArea>div>textarea {
        background: var(--input-bg) !important;
        color: var(--input-text) !important;
        border: 2px solid var(--border) !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
    }
    
    /* Select box fixes */
    .stSelectbox > div > div {
        background: var(--input-bg) !important;
        color: var(--input-text) !important;
        border: 2px solid var(--border) !important;
        border-radius: 10px !important;
    }
    
    /* JD Generator specific styles */
    .jd-generator-output textarea {
        background: white !important;
        color: black !important;
        border: 2px solid #0099FF !important;
        font-family: 'Courier New', monospace !important;
    }
    </style>
    """, unsafe_allow_html=True)

def create_premium_navigation():
    """Create premium navigation with user info"""
    pages = {
        "Dashboard": "📊",
        "Resume Screening": "📄", 
        "AI Interview Prep": "🎯",
        "JD Generator": "📝",
        "Candidates": "👥",
        "Analytics": "📈"
    }
    
    # User info at top
    st.markdown(f"""
    <div style='text-align: center; padding: 20px 0;'>
        <div style='font-size: 2.5rem; background: linear-gradient(135deg, #00D4AA, #0099FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900;'>🚀</div>
        <h1 style='margin: 10px 0; color: white;'>SmartHire AI</h1>
        <p style='margin: 0; color: #E0E0E0;'>Premium Recruitment Platform</p>
        <div style='background: rgba(0, 212, 170, 0.2); padding: 8px 16px; border-radius: 20px; margin-top: 10px;'>
            <p style='margin: 0; color: #00D4AA; font-size: 0.9rem;'>Welcome, {st.session_state.current_user}!</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navigation buttons
    for page, icon in pages.items():
        if st.button(f"{icon} {page}", 
                    use_container_width=True, 
                    key=f"nav_{page}",
                    type="primary" if st.session_state.current_page == page else "secondary"):
            st.session_state.current_page = page
            st.rerun()
    
    st.markdown("---")
    
    # Quick Stats
    st.markdown("**📊 Quick Stats**")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Active Jobs", "18")
        st.metric("Candidates", "127")
    with col2:
        st.metric("Match Rate", "87%")
        st.metric("Hiring Time", "16d")
    
    # Logout button at bottom
    st.markdown("---")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.show_login = True
        st.rerun()

# Page Functions
def show_dashboard():
    """Show main dashboard"""
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

def show_resume_screening():
    """Show resume screening page"""
    st.markdown("### 📄 AI Resume Screening")
    
    uploaded_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=['pdf', 'docx'])
    
    if uploaded_file is not None:
        # Process file
        if uploaded_file.type == "application/pdf":
            text = extract_text_from_pdf(uploaded_file)
        else:
            text = extract_text_from_docx(uploaded_file)
        
        info = extract_info_from_resume(text)
        
        # Display results
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="premium-card">
                <h4>📊 Resume Score</h4>
            """, unsafe_allow_html=True)
            
            # Score visualization
            score = info['score']
            st.metric("Overall Score", f"{score}/100")
            st.progress(score/100)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="premium-card">
                <h4>👤 Candidate Info</h4>
            """, unsafe_allow_html=True)
            
            st.write(f"**Email:** {info['email'] if info['email'] else 'Not found'}")
            st.write(f"**Phone:** {info['phone'] if info['phone'] else 'Not found'}")
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("✅ Shortlist Candidate", use_container_width=True):
                show_success_popup()
                st.success("Candidate shortlisted!")
        
        with col2:
            if st.button("📧 Send Email", use_container_width=True):
                if info['email']:
                    success, message = send_real_email(info['email'], "Interview Invitation", "We'd like to invite you for an interview.")
                    if success:
                        st.success("Email sent successfully!")
                    else:
                        st.error(message)
                else:
                    st.warning("No email found in resume")
        
        with col3:
            if st.button("📝 Schedule Interview", use_container_width=True):
                st.info("Interview scheduling feature coming soon!")

def show_interview_prep():
    """Show AI interview preparation page"""
    st.markdown("### 🎯 AI Interview Preparation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        role = st.selectbox("Select Role", ["Data Science", "AI Engineering", "Software Engineering", "Product Management"])
        difficulty = st.selectbox("Select Difficulty", ["All", "Beginner", "Intermediate", "Advanced"])
        num_questions = st.slider("Number of Questions", 1, 10, 5)
    
    with col2:
        st.markdown("""
        <div class="premium-card">
            <h4>💡 Tips</h4>
            <p>• Practice with role-specific questions</p>
            <p>• Focus on your experience</p>
            <p>• Prepare real-world examples</p>
            <p>• Research the company</p>
        </div>
        """, unsafe_allow_html=True)
    
    if st.button("🎯 Generate Interview Questions", use_container_width=True):
        questions = get_ai_questions(role, difficulty, num_questions)
        st.session_state.ai_questions = questions
        
        if questions:
            st.markdown("### 📝 Generated Questions")
            for i, q in enumerate(questions, 1):
                with st.expander(f"Q{i}: {q['question']} ({q['difficulty']})"):
                    st.write(q['answer'])
        else:
            st.warning("No questions available for the selected criteria.")

def show_jd_generator():
    """Show Job Description Generator page"""
    st.markdown("### 📝 AI Job Description Generator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        job_title = st.text_input("Job Title", placeholder="e.g., Senior Data Scientist")
        company = st.text_input("Company Name", placeholder="e.g., Tech Innovations Inc.")
        location = st.text_input("Location", placeholder="e.g., San Francisco, CA")
        job_type = st.selectbox("Job Type", ["Full-time", "Part-time", "Contract", "Remote"])
    
    with col2:
        experience = st.selectbox("Experience Level", ["Entry", "Mid", "Senior", "Lead"])
        department = st.selectbox("Department", ["Engineering", "Data Science", "Product", "Marketing", "Sales"])
        salary_range = st.text_input("Salary Range", placeholder="e.g., $120,000 - $150,000")
    
    # Skills and requirements
    required_skills = st.text_area("Required Skills", placeholder="Python, Machine Learning, SQL, AWS...")
    responsibilities = st.text_area("Key Responsibilities", placeholder="• Develop machine learning models\n• Analyze large datasets\n• Collaborate with cross-functional teams...")
    
    if st.button("🚀 Generate Job Description", use_container_width=True):
        # Generate JD template
        jd_template = f"""
# {job_title}

**Company:** {company}  
**Location:** {location}  
**Type:** {job_type} | **Level:** {experience}  
**Department:** {department}  
**Salary:** {salary_range}

## 📋 Job Overview
We are seeking a talented {experience.lower()} {job_title} to join our {department} team. This role offers an exciting opportunity to work on cutting-edge projects and make a significant impact.

## 🎯 Key Responsibilities
{responsibilities if responsibilities else "• To be defined based on role requirements"}

## ⚡ Required Skills & Qualifications
{required_skills if required_skills else "• To be defined based on role requirements"}

## 🎁 Benefits & Perks
• Competitive salary and equity package
• Comprehensive health benefits
• Flexible work arrangements
• Professional development opportunities
• Collaborative and innovative work environment

## 📧 How to Apply
Please submit your resume and cover letter through our application portal. We look forward to reviewing your application!

---
*Generated by SmartHire AI*
"""
        
        st.session_state.generated_jd = jd_template
        st.session_state.jd_created = True
    
    if st.session_state.jd_created:
        st.markdown("### 📄 Generated Job Description")
        st.text_area("Job Description Content", st.session_state.generated_jd, height=400, key="jd_output")
        
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="📥 Download JD",
                data=st.session_state.generated_jd,
                file_name=f"job_description_{job_title.replace(' ', '_')}.md",
                mime="text/markdown",
                use_container_width=True
            )
        
        with col2:
            if st.button("📧 Share JD", use_container_width=True):
                st.info("JD sharing feature coming soon!")

def show_candidates():
    """Show candidates management page"""
    st.markdown("### 👥 Candidate Management")
    
    # Sample candidate data
    candidates = [
        {"name": "John Smith", "role": "Data Scientist", "status": "Shortlisted", "score": 85, "applied_date": "2024-01-15"},
        {"name": "Sarah Johnson", "role": "AI Engineer", "status": "Interview", "score": 92, "applied_date": "2024-01-12"},
        {"name": "Mike Chen", "role": "ML Engineer", "status": "Applied", "score": 78, "applied_date": "2024-01-18"},
        {"name": "Emily Davis", "role": "Data Analyst", "status": "Rejected", "score": 65, "applied_date": "2024-01-10"},
        {"name": "David Wilson", "role": "AI Researcher", "status": "Offer", "score": 95, "applied_date": "2024-01-08"}
    ]
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_role = st.selectbox("Filter by Role", ["All", "Data Scientist", "AI Engineer", "ML Engineer", "Data Analyst", "AI Researcher"])
    with col2:
        filter_status = st.selectbox("Filter by Status", ["All", "Applied", "Shortlisted", "Interview", "Offer", "Rejected"])
    with col3:
        sort_by = st.selectbox("Sort by", ["Score", "Name", "Applied Date"])
    
    # Filter candidates
    filtered_candidates = candidates
    if filter_role != "All":
        filtered_candidates = [c for c in filtered_candidates if c["role"] == filter_role]
    if filter_status != "All":
        filtered_candidates = [c for c in filtered_candidates if c["status"] == filter_status]
    
    # Sort candidates
    if sort_by == "Score":
        filtered_candidates.sort(key=lambda x: x["score"], reverse=True)
    elif sort_by == "Name":
        filtered_candidates.sort(key=lambda x: x["name"])
    else:
        filtered_candidates.sort(key=lambda x: x["applied_date"], reverse=True)
    
    # Display candidates
    for candidate in filtered_candidates:
        with st.container():
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            
            with col1:
                st.write(f"**{candidate['name']}**")
                st.write(f"*{candidate['role']}*")
            
            with col2:
                status_color = {
                    "Applied": "blue",
                    "Shortlisted": "green", 
                    "Interview": "orange",
                    "Offer": "purple",
                    "Rejected": "red"
                }
                st.write(f"Status: :{status_color[candidate['status']]}[{candidate['status']}]")
            
            with col3:
                st.write(f"Score: **{candidate['score']}**")
            
            with col4:
                st.write(f"Applied: {candidate['applied_date']}")
            
            # Action buttons
            btn_col1, btn_col2, btn_col3, btn_col4 = st.columns(4)
            with btn_col1:
                st.button("👀 View", key=f"view_{candidate['name']}", use_container_width=True)
            with btn_col2:
                st.button("📞 Contact", key=f"contact_{candidate['name']}", use_container_width=True)
            with btn_col3:
                st.button("📅 Schedule", key=f"schedule_{candidate['name']}", use_container_width=True)
            with btn_col4:
                st.button("📊 Evaluate", key=f"evaluate_{candidate['name']}", use_container_width=True)
            
            st.markdown("---")

def show_analytics():
    """Show analytics dashboard"""
    st.markdown("### 📈 Hiring Analytics")
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Applications", "127", "12%")
    with col2:
        st.metric("Interview Rate", "24%", "3%")
    with col3:
        st.metric("Offer Acceptance", "85%", "5%")
    with col4:
        st.metric("Time to Hire", "16 days", "-2 days")
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_trend_chart(), use_container_width=True)
    
    with col2:
        # Source distribution
        sources = ['LinkedIn', 'Indeed', 'Company Website', 'Referral', 'Other']
        applications = [45, 32, 28, 15, 7]
        
        fig = go.Figure(data=[go.Pie(labels=sources, values=applications, hole=.3)])
        fig.update_layout(
            title='Application Sources',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed analytics
    st.markdown("### 📊 Detailed Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="premium-card">
            <h4>🎯 Conversion Funnel</h4>
            <p>Applied: 127</p>
            <p>Screen Pass: 89 (70%)</p>
            <p>Interview: 31 (24%)</p>
            <p>Offer: 13 (10%)</p>
            <p>Hired: 11 (9%)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="premium-card">
            <h4>⏱️ Time Metrics</h4>
            <p>Screen to Interview: 3.2 days</p>
            <p>Interview to Offer: 8.5 days</p>
            <p>Offer to Accept: 4.3 days</p>
            <p>Total Time: 16 days</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="premium-card">
            <h4>💰 Cost Metrics</h4>
            <p>Cost per Hire: $4,250</p>
            <p>Cost per Screen: $45</p>
            <p>Cost per Interview: $180</p>
            <p>ROI: 215%</p>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main application function"""
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
    
    # Check authentication
    if not check_authentication():
        show_login_page()
        return
    
    # Load main app CSS
    load_ultra_premium_css()
    
    # Main application after login
    with st.sidebar:
        create_premium_navigation()
    
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
        📍 Currently Viewing: {st.session_state.current_page} | 👤 User: {st.session_state.current_user}
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

if __name__ == "__main__":
    main()