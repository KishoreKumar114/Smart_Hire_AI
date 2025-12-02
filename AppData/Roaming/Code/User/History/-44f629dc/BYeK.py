# email_config.py
def get_email_config():
    """Return email configuration for sending real emails"""
    return {
        'sender_email': 'your_email@gmail.com',
        'sender_password': 'your_app_password',
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587
    }

def validate_email_config():
    """Validate email configuration"""
    config = get_email_config()
    required_fields = ['sender_email', 'sender_password', 'smtp_server', 'smtp_port']
    for field in required_fields:
        if not config.get(field):
            return False, f"Missing {field}"
    return True, "Valid configuration"

# Company Information
COMPANY_NAME = "SmartHire AI"
HR_EMAIL = "hr@smarthire.com"
HR_PHONE = "+1 (555) 123-4567"