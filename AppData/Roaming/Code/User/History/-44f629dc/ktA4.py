# email_config.py
"""
SMTP Email Configuration for SmartHire AI
Update these settings with your email credentials
"""

# Gmail SMTP Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "kishorekumarr2k4@gmail.com"  # Replace with your Gmail
SENDER_PASSWORD = "your-app-password"  # Replace with your Gmail App Password

# Email Settings
EMAIL_SUBJECT_PREFIX = "SmartHire AI - Interview Invitation"

# Company Information
COMPANY_NAME = "SmartHire AI"
HR_EMAIL = "hr@smarthire.com"
HR_PHONE = "+1 (555) 123-4567"

def validate_email_config():
    """Validate if email configuration is set up correctly"""
    if SENDER_EMAIL == "your-email@gmail.com" or SENDER_PASSWORD == "your-app-password":
        return False, "Please update email configuration in email_config.py"
    return True, "Email configuration is ready"

def get_email_config():
    """Get email configuration"""
    return {
        'smtp_server': SMTP_SERVER,
        'smtp_port': SMTP_PORT,
        'sender_email': SENDER_EMAIL,
        'sender_password': SENDER_PASSWORD
    }