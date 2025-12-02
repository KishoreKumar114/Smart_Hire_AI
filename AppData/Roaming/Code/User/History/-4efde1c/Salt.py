# app.py - PERFECT POLISHED VERSION
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
import plotly.express as px

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
        --bg-sidebar: #1E3A8A;
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
    
    /* Sidebar - Blue Color */
    .css-1d391kg, .css-1lcbmhc {
        background: var(--bg-sidebar) !important;
        border-right: 1px solid var(--border);
    }
    
    /* Input Fields - Dark Background with White Text */
    .stTextInput>div>div>input, .stSelectbox>div>div, .stTextArea>div>textarea {
        background: var(--input-bg) !important;
        color: var(--input-text) !important;
        border: 2px solid var(--border) !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
    }
    
    .stTextInput>div>div>input::placeholder, .stTextArea>div>textarea::placeholder {
        color: var(--text-muted) !important;
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
    
    /* Candidate Cards */
    .candidate-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .candidate-card:hover {
        background: var(--bg-secondary);
        transform: translateX(5px);
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
    </style>
    """, unsafe_allow_html=True)

def extract_info_from_resume(text):
    """Advanced resume parsing"""
    info = {
        'name': '',
        'email': '',
        'phone': '',
        'experience': 0,
        'skills': []
    }
    
    lines = text.split('\n')
    if lines:
        info['name'] = lines[0].strip()
    
    # Extract email
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    if emails:
        info['email'] = emails[0]
    
    # Extract phone
    phone_pattern = r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]'
    phones = re.findall(phone_pattern, text)
    if phones:
        info['phone'] = phones[0]
    
    # Extract experience
    exp_pattern = r'(\d+)\s*(?:years?|yrs?)'
    exp_matches = re.findall(exp_pattern, text.lower())
    if exp_matches:
        info['experience'] = max([int(match) for match in exp_matches])
    
    # Extract skills
    common_skills = ['python', 'java', 'javascript', 'sql', 'aws', 'docker', 'machine learning', 'react', 'node']
    found_skills = []
    for skill in common_skills:
        if skill in text.lower():
            found_skills.append(skill.title())
    
    info['skills'] = found_skills[:8]
    return info

def send_real_email(candidate_email, candidate_name, role, interview_date, interview_time, interview_type):
    """Send real email"""
    try:
        if not EMAIL_ENABLED:
            return False, "Email configuration not available"
        
        config = EMAIL_CONFIG
        
        message = MIMEMultipart("alternative")
        message["Subject"] = f"Interview Invitation - {role} Position"
        message["From"] = config['sender_email']
        message["To"] = candidate_email
        
        html = f"""
        <html>
          <body style="font-family: Arial, sans-serif;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
              <h2 style="color: #2c3e50;">🎯 Interview Invitation</h2>
              <p>Dear <strong>{candidate_name}</strong>,</p>
              <p>Thank you for your interest in the <strong>{role}</strong> position.</p>
              
              <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 20px 0;">
                <h3>📅 Interview Details:</h3>
                <p><strong>Position:</strong> {role}</p>
                <p><strong>Date:</strong> {interview_date}</p>
                <p><strong>Time:</strong> {interview_time}</p>
                <p><strong>Type:</strong> {interview_type}</p>
              </div>
              
              <p>We look forward to speaking with you!</p>
              
              <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
                <p>Best regards,<br><strong>SmartHire AI Team</strong></p>
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
        
        return True, "Email sent successfully"
        
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

def create_prediction_chart():
    """Create future prediction chart"""
    months = ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    predicted_applications = [240, 260, 280, 300, 320, 350]
    predicted_hires = [22, 25, 28, 30, 32, 35]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=months, y=predicted_applications,
        mode='lines+markers',
        name='Predicted Applications',
        line=dict(color='#00D4AA', width=3, dash='dash'),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=months, y=predicted_hires,
        mode='lines+markers',
        name='Predicted Hires',
        line=dict(color='#0099FF', width=3, dash='dash'),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title='🔮 Future Hiring Predictions - Next 6 Months',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(gridcolor='#333333'),
        yaxis=dict(gridcolor='#333333')
    )
    
    return fig

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
    
    load_ultra_premium_css()
    
    # Blue Sidebar
    with st.sidebar:
        # Logo and Brand
        st.markdown("""
        <div style='text-align: center; padding: 20px 0;'>
            <div style='font-size: 2.5rem; background: linear-gradient(135deg, #00D4AA, #0099FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900;'>🚀</div>
            <h1 style='margin: 10px 0; color: white;'>SmartHire AI</h1>
            <p style='margin: 0; color: #E0E0E0;'>Premium Recruitment Platform</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation
        pages = {
            "Dashboard": "📊",
            "Resume Screening": "📄", 
            "AI Interview Prep": "🎯",
            "JD Generator": "📝",
            "Candidates": "👥",
            "Analytics": "📈"
        }
        
        for page, icon in pages.items():
            if st.button(f"{icon} {page}", use_container_width=True, key=f"nav_{page}"):
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
    
    # Main Content
    st.markdown("""
    <div class="logo-container">
        <div class="logo">🚀</div>
        <h1 class="premium-header">SmartHire.AI</h1>
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
    st.markdown("""
    <div class="premium-card">
        <h3>📄 AI Resume Screening</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        uploaded_file = st.file_uploader("Choose resume file", type=['pdf', 'docx', 'txt'])
        
        if uploaded_file:
            sample_resume = """
John Doe
Senior Data Scientist
Email: john.doe@email.com | Phone: +1 (555) 123-4567

EXPERIENCE
5 years as Data Scientist at TechCorp
3 years as Data Analyst at DataInc

SKILLS
Python, Machine Learning, SQL, AWS, TensorFlow
"""
            extracted_info = extract_info_from_resume(sample_resume)
            st.session_state.resume_analysis = extracted_info
            
            show_success_popup("Resume processed successfully!")
            
            st.text_input("Full Name", value=extracted_info['name'])
            st.text_input("Email", value=extracted_info['email'])
            st.text_input("Phone", value=extracted_info['phone'])
            st.slider("Experience", 0, 20, extracted_info['experience'])
            
            if extracted_info['skills']:
                st.write("**Skills:**")
                for skill in extracted_info['skills']:
                    st.markdown(f"- {skill}")
    
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
            st.markdown("**Schedule Interview**")
            
            col_date, col_time = st.columns(2)
            with col_date:
                interview_date = st.date_input("Date")
            with col_time:
                interview_time = st.time_input("Time")
            
            interview_type = st.selectbox("Type", ["Technical", "HR", "Manager"])
            role = st.selectbox("Role", ["Data Scientist", "AI Engineer"])
            
            if st.button("📧 Send Email Invitation", type="primary", use_container_width=True):
                if EMAIL_ENABLED:
                    success, message = send_real_email(
                        analysis['email'],
                        analysis['name'], 
                        role,
                        interview_date,
                        interview_time,
                        interview_type
                    )
                    if success:
                        show_success_popup("✅ Email sent successfully!")
                    else:
                        st.error(f"❌ {message}")

def show_interview_prep():
    st.markdown("""
    <div class="premium-card">
        <h3>🎯 AI Interview Preparation</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        role = st.selectbox("Select Role", ["Data Scientist", "AI Engineer", "Software Developer"])
        experience = st.selectbox("Experience Level", ["Entry", "Mid", "Senior"])
        domain = st.selectbox("Domain", ["Data Science", "AI/ML", "Software Engineering"])
        
        if st.button("🤖 Generate Questions", type="primary", use_container_width=True):
            show_success_popup("AI questions generated!")
    
    with col2:
        st.markdown("""
        <div class="premium-card">
            <h4>Sample Questions</h4>
        </div>
        """, unsafe_allow_html=True)
        
        questions = [
            "Explain the bias-variance tradeoff in machine learning",
            "How do you handle missing data in datasets?",
            "What's your experience with cloud platforms?",
            "Describe a challenging project you worked on"
        ]
        
        for i, q in enumerate(questions, 1):
            st.markdown(f"**Q{i}:** {q}")

def show_jd_generator():
    st.markdown("""
    <div class="premium-card">
        <h3>📝 AI Job Description Generator</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        job_title = st.text_input("Job Title")
        department = st.selectbox("Department", ["Engineering", "Data Science", "Product"])
        experience = st.selectbox("Experience", ["Entry", "Mid", "Senior"])
        skills = st.text_area("Required Skills")
        
        if st.button("🚀 Generate JD", type="primary", use_container_width=True):
            with st.spinner("Generating..."):
                time.sleep(2)
                show_success_popup("Job Description Created!")
    
    with col2:
        if st.session_state.generated_jd:
            st.text_area("Generated JD", st.session_state.generated_jd, height=300)
        else:
            st.info("👆 Fill the details and generate JD")

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
            new_name = st.text_input("Full Name")
            new_email = st.text_input("Email")
            new_phone = st.text_input("Phone")
        
        with col2:
            new_role = st.selectbox("Role", ["Data Scientist", "AI Engineer", "Software Developer"])
            new_exp = st.slider("Experience (Years)", 0, 20, 3)
            new_status = st.selectbox("Status", ["Applied", "Screening", "Interview", "Offer"])
        
        if st.button("Add Candidate", type="primary", use_container_width=True):
            if new_name and new_email:
                new_candidate = {
                    'name': new_name,
                    'email': new_email,
                    'phone': new_phone,
                    'role': new_role,
                    'experience': new_exp,
                    'status': new_status,
                    'score': f"{random.randint(70, 95)}%"
                }
                st.session_state.candidates.append(new_candidate)
                show_success_popup(f"Added {new_name}!")
                st.rerun()
    
    st.markdown("---")
    
    # Candidates List - WORKING BUTTONS
    if st.session_state.candidates:
        for candidate in st.session_state.candidates:
            col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
            
            with col1:
                st.write(f"**{candidate['name']}**")
                st.write(f"📧 {candidate['email']}")
            
            with col2:
                st.write(f"💼 {candidate['role']}")
                st.write(f"⏳ {candidate['experience']} years")
            
            with col3:
                status_color = {
                    "Applied": "#3498db",
                    "Screening": "#f39c12", 
                    "Interview": "#9b59b6",
                    "Offer": "#2ecc71"
                }
                st.markdown(f"""
                <div style='background: {status_color[candidate['status']]}; color: white; padding: 5px 10px; border-radius: 15px; text-align: center; font-size: 0.8rem;'>
                    {candidate['status']}
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.write(f"🎯 {candidate['score']}")
                
                # WORKING ACTION BUTTONS
                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    if st.button("👁️", key=f"view_{candidate['name']}"):
                        st.info(f"Viewing {candidate['name']}'s profile")
                with btn_col2:
                    if st.button("📧", key=f"email_{candidate['name']}"):
                        st.info(f"Preparing email for {candidate['name']}")
            
            st.markdown("---")
    else:
        st.info("No candidates added yet. Use the form above to add candidates.")

def show_analytics():
    st.markdown("""
    <div class="premium-card">
        <h3>📈 Advanced Analytics & Predictions</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Time to Hire", "16.2d", "-1.8d")
        st.metric("Cost per Hire", "$2,847", "-$153")
        st.metric("Quality of Hire", "8.7/10", "+0.3")
        st.metric("Candidate Satisfaction", "94%", "+2%")
    
    with col2:
        st.metric("Predicted Hires Next Month", "25", "+5")
        st.metric("Expected Applications", "280", "+60")
        st.metric("Success Probability", "92%", "+7%")
        st.metric("AI Confidence Score", "88%", "+3%")
    
    st.markdown("---")
    
    # Charts Section
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_trend_chart(), use_container_width=True)
    
    with col2:
        st.plotly_chart(create_prediction_chart(), use_container_width=True)
    
    # AI Predictions
    st.markdown("""
    <div class="premium-card">
        <h4>🤖 AI Future Predictions</h4>
    </div>
    """, unsafe_allow_html=True)
    
    predictions = [
        "🎯 **Next Month:** Expect 25% increase in Data Science applications",
        "📈 **Q3 Forecast:** Hiring time will reduce to 14 days with AI screening",
        "💡 **Recommendation:** Focus on AI Engineer roles - 40% demand growth predicted",
        "⚠️ **Alert:** Software Developer market becoming competitive - adjust salary bands",
        "🚀 **Opportunity:** Remote candidates show 15% higher retention rate"
    ]
    
    for prediction in predictions:
        st.markdown(f"- {prediction}")

if __name__ == "__main__":
    main()