# app.py - MODERN CLEAN VERSION
import streamlit as st
import database as db
import pandas as pd
from datetime import datetime
import time
import io

# Modern CSS with clean design
def load_modern_css():
    st.markdown("""
    <style>
    /* Modern Color Scheme */
    :root {
        --primary: #2563eb;
        --primary-dark: #1d4ed8;
        --secondary: #64748b;
        --success: #10b981;
        --warning: #f59e0b;
        --error: #ef4444;
        --bg-primary: #ffffff;
        --bg-secondary: #f8fafc;
        --bg-sidebar: #1e293b;
        --text-primary: #1e293b;
        --text-secondary: #64748b;
        --text-light: #94a3b8;
        --border: #e2e8f0;
        --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }
    
    .dark-mode {
        --bg-primary: #0f172a;
        --bg-secondary: #1e293b;
        --bg-sidebar: #0f172a;
        --text-primary: #f1f5f9;
        --text-secondary: #cbd5e1;
        --text-light: #94a3b8;
        --border: #334155;
        --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.3), 0 1px 2px 0 rgba(0, 0, 0, 0.2);
    }
    
    /* Base Styles */
    .stApp {
        background: var(--bg-primary);
        color: var(--text-primary);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Modern Header */
    .modern-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--text-primary);
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(135deg, var(--primary), #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Clean Cards */
    .clean-card {
        background: var(--bg-primary);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 24px;
        margin: 16px 0;
        box-shadow: var(--shadow);
        transition: all 0.2s ease;
    }
    
    .clean-card:hover {
        box-shadow: var(--shadow-lg);
        transform: translateY(-2px);
    }
    
    /* Metric Cards */
    .metric-card {
        background: var(--bg-primary);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin: 8px;
        transition: all 0.2s ease;
    }
    
    .metric-card:hover {
        border-color: var(--primary);
        transform: translateY(-2px);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary);
        margin: 8px 0;
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: var(--text-secondary);
        font-weight: 500;
    }
    
    /* Modern Buttons */
    .stButton > button {
        background: var(--primary);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background: var(--primary-dark);
        transform: translateY(-1px);
        box-shadow: var(--shadow-lg);
    }
    
    /* Sidebar Styling */
    .css-1d391kg, .css-1lcbmhc {
        background: var(--bg-sidebar);
    }
    
    .sidebar-item {
        background: transparent !important;
        border: none !important;
        color: var(--text-secondary) !important;
        padding: 12px 16px !important;
        margin: 4px 0 !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
        text-align: left !important;
        width: 100% !important;
    }
    
    .sidebar-item:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
    }
    
    .sidebar-item.active {
        background: var(--primary) !important;
        color: white !important;
    }
    
    /* Form Elements */
    .stTextInput>div>div>input, .stSelectbox>div>div, .stTextArea>div>textarea {
        background: var(--bg-primary) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        padding: 10px 12px !important;
    }
    
    .stTextInput>div>div>input:focus, .stSelectbox>div>div:focus, .stTextArea>div>textarea:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.1) !important;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--primary), #8b5cf6) !important;
    }
    
    /* File Uploader */
    .stFileUploader > div > div {
        border: 2px dashed var(--border) !important;
        border-radius: 12px !important;
        background: var(--bg-secondary) !important;
    }
    
    /* Dataframe Styling */
    .dataframe {
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
    }
    
    /* Badge Styles */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        background: var(--bg-secondary);
        color: var(--text-secondary);
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .badge-success {
        background: #dcfce7;
        color: #166534;
    }
    
    .badge-warning {
        background: #fef3c7;
        color: #92400e;
    }
    
    .badge-primary {
        background: #dbeafe;
        color: var(--primary-dark);
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    # Page configuration
    st.set_page_config(
        page_title="SmartHire AI",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session states
    if 'generated_jd' not in st.session_state:
        st.session_state.generated_jd = ""
    if 'page_loaded' not in st.session_state:
        st.session_state.page_loaded = False
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Dashboard"
    
    # Load CSS
    load_modern_css()
    
    # Apply dark mode
    if st.session_state.dark_mode:
        st.markdown('<div class="dark-mode">', unsafe_allow_html=True)
    
    # Modern Sidebar
    with st.sidebar:
        # Header
        st.markdown("""
        <div style='padding: 2rem 1rem; text-align: center; border-bottom: 1px solid var(--border); margin-bottom: 2rem;'>
            <h1 style='margin: 0; font-size: 1.5rem; color: white; font-weight: 700;'>🚀 SmartHire</h1>
            <p style='margin: 0; color: var(--text-light); font-size: 0.875rem;'>AI Recruitment Platform</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation
        st.markdown("### Navigation")
        
        nav_items = {
            "Dashboard": "📊",
            "JD Generator": "📝", 
            "Resume Screening": "📄",
            "Analytics": "📈",
            "Settings": "⚙️"
        }
        
        for item, icon in nav_items.items():
            is_active = st.session_state.current_page == item
            if st.button(f"{icon} {item}", key=f"nav_{item}", use_container_width=True):
                st.session_state.current_page = item
                st.rerun()
        
        st.markdown("---")
        
        # Quick Stats
        st.markdown("### Quick Stats")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Jobs", "25", "+3")
            st.metric("Candidates", "142", "+12")
        with col2:
            st.metric("Match Rate", "82%", "+5%")
            st.metric("Hiring Time", "18d", "-2d")
        
        # Theme Toggle at bottom
        st.markdown("---")
        theme_label = "Switch to Light" if st.session_state.dark_mode else "Switch to Dark"
        if st.button(f"🌙 {theme_label}", use_container_width=True):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
    
    # Main Content
    st.markdown(f"<h1 class='modern-header'>SmartHire AI</h1>", unsafe_allow_html=True)
    
    # Show loading
    if not st.session_state.page_loaded:
        with st.spinner("Loading SmartHire AI..."):
            time.sleep(1)
        st.session_state.page_loaded = True
        st.rerun()
    
    # Page routing
    if st.session_state.current_page == "Dashboard":
        show_modern_dashboard()
    elif st.session_state.current_page == "JD Generator":
        show_modern_jd_generator()
    elif st.session_state.current_page == "Resume Screening":
        show_modern_resume_screening()
    elif st.session_state.current_page == "Analytics":
        show_modern_analytics()
    elif st.session_state.current_page == "Settings":
        show_modern_settings()

def show_modern_dashboard():
    # Connection Status
    test_result = db.execute_query("SELECT 1 as test")
    if test_result:
        st.success("✅ System connected successfully")
    
    # KPI Section
    st.markdown("### Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 1.5rem; margin-bottom: 8px;">💼</div>
            <div class="metric-value">25</div>
            <div class="metric-label">Active Jobs</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 1.5rem; margin-bottom: 8px;">👥</div>
            <div class="metric-value">142</div>
            <div class="metric-label">Candidates</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 1.5rem; margin-bottom: 8px;">⚡</div>
            <div class="metric-value">18d</div>
            <div class="metric-label">Avg Hiring Time</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 1.5rem; margin-bottom: 8px;">🎯</div>
            <div class="metric-value">94%</div>
            <div class="metric-label">Success Rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Main Content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Recent Activity
        st.markdown("""
        <div class="clean-card">
            <h3 style="margin-bottom: 1rem; color: var(--text-primary);">Recent Activity</h3>
            <div style="display: grid; gap: 12px;">
        """, unsafe_allow_html=True)
        
        activities = [
            {"icon": "🚀", "text": "Senior AI Engineer - JD Created", "time": "2h ago", "badge": "success"},
            {"icon": "✅", "text": "Raj Kumar - Screened (85% match)", "time": "4h ago", "badge": "primary"},
            {"icon": "📊", "text": "Q3 Report - Analysis Completed", "time": "1d ago", "badge": "warning"},
            {"icon": "🎯", "text": "Technical Interview - Scheduled", "time": "Tomorrow", "badge": "success"}
        ]
        
        for activity in activities:
            st.markdown(f"""
            <div style="display: flex; align-items: center; padding: 12px; background: var(--bg-secondary); border-radius: 8px;">
                <div style="font-size: 1.2rem; margin-right: 12px;">{activity['icon']}</div>
                <div style="flex: 1;">
                    <div style="font-weight: 500; color: var(--text-primary);">{activity['text']}</div>
                </div>
                <div style="font-size: 0.875rem; color: var(--text-secondary);">{activity['time']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)
        
        # Quick Actions
        st.markdown("""
        <div class="clean-card">
            <h3 style="margin-bottom: 1rem; color: var(--text-primary);">Quick Actions</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px;">
        """, unsafe_allow_html=True)
        
        action_col1, action_col2, action_col3 = st.columns(3)
        with action_col1:
            if st.button("📝 Create JD", use_container_width=True):
                st.session_state.current_page = "JD Generator"
                st.rerun()
        with action_col2:
            if st.button("📄 Screen Resume", use_container_width=True):
                st.session_state.current_page = "Resume Screening"
                st.rerun()
        with action_col3:
            if st.button("📊 View Reports", use_container_width=True):
                st.session_state.current_page = "Analytics"
                st.rerun()
        
        st.markdown("</div></div>", unsafe_allow_html=True)
    
    with col2:
        # System Status
        st.markdown("""
        <div class="clean-card">
            <h3 style="margin-bottom: 1rem; color: var(--text-primary);">System Status</h3>
            <div style="display: grid; gap: 12px;">
                <div style="display: flex; justify-content: between; align-items: center;">
                    <span>Database</span>
                    <span style="color: var(--success); font-weight: 600;">Connected</span>
                </div>
                <div style="display: flex; justify-content: between; align-items: center;">
                    <span>AI Engine</span>
                    <span style="color: var(--success); font-weight: 600;">Active</span>
                </div>
                <div style="display: flex; justify-content: between; align-items: center;">
                    <span>Performance</span>
                    <span style="color: var(--warning); font-weight: 600;">Optimal</span>
                </div>
                <div style="display: flex; justify-content: between; align-items: center;">
                    <span>Storage</span>
                    <span style="color: var(--primary); font-weight: 600;">78% Free</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Today's Performance
        st.markdown("""
        <div class="clean-card">
            <h3 style="margin-bottom: 1rem; color: var(--text-primary);">Today's Performance</h3>
            <div style="display: grid; gap: 8px;">
                <div style="display: flex; justify-content: between;">
                    <span>JDs Created</span>
                    <span style="font-weight: 600; color: var(--primary);">3</span>
                </div>
                <div style="display: flex; justify-content: between;">
                    <span>Candidates Added</span>
                    <span style="font-weight: 600; color: var(--success);">12</span>
                </div>
                <div style="display: flex; justify-content: between;">
                    <span>Avg Response</span>
                    <span style="font-weight: 600; color: var(--warning);">2.1h</span>
                </div>
                <div style="display: flex; justify-content: between;">
                    <span>Efficiency</span>
                    <span style="font-weight: 600; color: var(--success);">+18%</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def show_modern_jd_generator():
    st.markdown("### Job Description Generator")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="clean-card">
            <h3 style="margin-bottom: 1rem; color: var(--text-primary);">Job Details</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Form
        companies = db.execute_query("SELECT id, name FROM companies")
        company_options = {company['name']: company['id'] for company in companies} if companies else {"Tech Solutions": 1}
        
        selected_company = st.selectbox("Company", list(company_options.keys()))
        job_title = st.text_input("Job Title", placeholder="e.g., Senior AI Engineer")
        department = st.selectbox("Department", ["Engineering", "Data Science", "Marketing", "Sales", "HR"])
        
        col_exp1, col_exp2 = st.columns(2)
        with col_exp1:
            min_exp = st.slider("Min Experience", 0, 15, 2)
        with col_exp2:
            max_exp = st.slider("Max Experience", 0, 20, 5)
        
        skills = st.text_area("Required Skills", placeholder="List key skills...", height=100)
        
        if st.button("Generate JD", type="primary", use_container_width=True):
            if job_title and skills:
                with st.spinner("Generating job description..."):
                    time.sleep(2)
                    generate_modern_jd(job_title, department, min_exp, max_exp, skills)
            else:
                st.error("Please fill required fields")
    
    with col2:
        st.markdown("""
        <div class="clean-card">
            <h3 style="margin-bottom: 1rem; color: var(--text-primary);">Generated Description</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.generated_jd:
            st.success("JD generated successfully!")
            
            edited_jd = st.text_area("Edit JD", st.session_state.generated_jd, height=400)
            st.session_state.generated_jd = edited_jd
            
            col_save, col_export, col_new = st.columns(3)
            with col_save:
                if st.button("💾 Save", use_container_width=True):
                    st.success("Saved to database!")
            with col_export:
                if st.button("📥 Export", use_container_width=True):
                    st.success("Export ready!")
            with col_new:
                if st.button("🔄 New", use_container_width=True):
                    st.session_state.generated_jd = ""
                    st.rerun()
        else:
            st.info("Fill the form and click 'Generate JD' to create a job description.")

def generate_modern_jd(title, department, min_exp, max_exp, skills):
    jd = f"""**Position:** {title}
**Department:** {department}
**Experience:** {min_exp}-{max_exp} years

**Job Summary**
We are looking for a skilled {title} to join our {department} team.

**Responsibilities**
• Develop and maintain software solutions
• Collaborate with team members
• Implement best practices

**Requirements**
{skills}

**Qualifications**
• {min_exp}+ years of experience
• Relevant degree or equivalent

*Generated by SmartHire AI • {datetime.now().strftime('%Y-%m-%d')}*"""
    
    st.session_state.generated_jd = jd
    st.rerun()

def show_modern_resume_screening():
    st.markdown("### Resume Screening")
    
    tab1, tab2 = st.tabs(["Upload Resume", "Candidate Database"])
    
    with tab1:
        st.markdown("""
        <div class="clean-card">
            <h3 style="margin-bottom: 1rem; color: var(--text-primary);">Upload Resume</h3>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Choose file", type=['pdf', 'docx', 'txt'])
        
        if uploaded_file:
            st.success(f"File uploaded: {uploaded_file.name}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                <div class="clean-card">
                    <h4>File Info</h4>
                    <p><strong>Name:</strong> {uploaded_file.name}</p>
                    <p><strong>Size:</strong> {uploaded_file.size / 1024:.1f} KB</p>
                </div>
                """.format(uploaded_file=uploaded_file), unsafe_allow_html=True)
            
            with col2:
                candidate_name = st.text_input("Candidate Name")
                candidate_email = st.text_input("Email")
                candidate_exp = st.slider("Experience (years)", 0, 30, 2)
            
            if st.button("Analyze Resume", type="primary", use_container_width=True):
                if candidate_name and candidate_email:
                    with st.spinner("Analyzing resume..."):
                        time.sleep(3)
                        show_modern_analysis()

def show_modern_analysis():
    st.markdown("---")
    st.markdown("### Analysis Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="clean-card">
            <h4>Match Scores</h4>
            <div style="display: grid; gap: 12px; margin-top: 1rem;">
                <div style="display: flex; justify-content: between;">
                    <span>Overall Match</span>
                    <span style="font-weight: 600; color: var(--success);">82%</span>
                </div>
                <div style="display: flex; justify-content: between;">
                    <span>Skill Fit</span>
                    <span style="font-weight: 600; color: var(--primary);">78%</span>
                </div>
                <div style="display: flex; justify-content: between;">
                    <span>Experience</span>
                    <span style="font-weight: 600; color: var(--success);">85%</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="clean-card">
            <h4>Recommendations</h4>
            <div style="margin-top: 1rem;">
                <div style="display: flex; align-items: center; margin: 8px 0;">
                    <span style="color: var(--success); margin-right: 8px;">✅</span>
                    <span>Strong technical skills</span>
                </div>
                <div style="display: flex; align-items: center; margin: 8px 0;">
                    <span style="color: var(--warning); margin-right: 8px;">⚠️</span>
                    <span>Consider cloud certification</span>
                </div>
                <div style="display: flex; align-items: center; margin: 8px 0;">
                    <span style="color: var(--success); margin-right: 8px;">🚀</span>
                    <span>Ready for interview</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def show_modern_analytics():
    st.markdown("### Analytics Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">25</div>
            <div class="metric-label">Total Jobs</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">142</div>
            <div class="metric-label">Candidates</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">68%</div>
            <div class="metric-label">Interview Rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">18d</div>
            <div class="metric-label">Hiring Time</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts section
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="clean-card">
            <h4>Hiring Trends</h4>
            <div style="height: 200px; display: flex; align-items: center; justify-content: center; color: var(--text-secondary);">
                [Chart: Hiring trends over time]
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="clean-card">
            <h4>Skill Demand</h4>
            <div style="height: 200px; display: flex; align-items: center; justify-content: center; color: var(--text-secondary);">
                [Chart: Top skills demand]
            </div>
        </div>
        """, unsafe_allow_html=True)

def show_modern_settings():
    st.markdown("### Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="clean-card">
            <h4>Theme Settings</h4>
            <p>Current theme: <strong>{}</strong></p>
            <p>Use the toggle in sidebar to switch themes.</p>
        </div>
        """.format("Dark" if st.session_state.dark_mode else "Light"), unsafe_allow_html=True)
        
        st.markdown("""
        <div class="clean-card">
            <h4>Notifications</h4>
            <div style="display: grid; gap: 12px;">
                <div style="display: flex; justify-content: between;">
                    <span>Email Alerts</span>
                    <span style="color: var(--success);">Enabled</span>
                </div>
                <div style="display: flex; justify-content: between;">
                    <span>Push Notifications</span>
                    <span style="color: var(--success);">Enabled</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="clean-card">
            <h4>System Configuration</h4>
            <div style="display: grid; gap: 8px;">
                <div style="display: flex; justify-content: between;">
                    <span>AI Model</span>
                    <span style="font-weight: 600;">v2.1</span>
                </div>
                <div style="display: flex; justify-content: between;">
                    <span>Data Retention</span>
                    <span style="font-weight: 600;">24 Months</span>
                </div>
                <div style="display: flex; justify-content: between;">
                    <span>Auto Backup</span>
                    <span style="font-weight: 600;">Daily</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()