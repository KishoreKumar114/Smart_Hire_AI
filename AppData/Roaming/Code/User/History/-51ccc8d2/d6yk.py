# database.py - UPDATED WITH USER MANAGEMENT
import mysql.connector
from mysql.connector import Error
import streamlit as st
import hashlib
import secrets

def get_connection():
    """Create a new connection for each query"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="pass123",
            database="smarthire_ai",
            auth_plugin='mysql_native_password'
        )
        return connection
    except Error as e:
        st.error(f"❌ Database connection failed: {e}")
        return None

def execute_query(query, params=None):
    """Execute SELECT query"""
    conn = get_connection()
    if not conn:
        return None
    
    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        result = cursor.fetchall()
        return result
    except Error as e:
        st.error(f"Query error: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def execute_insert(query, params=None):
    """Execute INSERT/UPDATE query"""
    conn = get_connection()
    if not conn:
        return None
    
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        st.error(f"Insert error: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# USER MANAGEMENT FUNCTIONS
def init_users_table():
    """Initialize users table if it doesn't exist"""
    conn = get_connection()
    if not conn:
        return False
    
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                full_name VARCHAR(255) NOT NULL,
                company VARCHAR(255),
                role VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP NULL,
                is_active BOOLEAN DEFAULT TRUE
            )
        """)
        conn.commit()
        return True
    except Error as e:
        st.error(f"Table creation error: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, email, password, full_name, company="", role=""):
    """Create new user"""
    password_hash = hash_password(password)
    
    query = """
        INSERT INTO users (username, email, password_hash, full_name, company, role)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    params = (username, email, password_hash, full_name, company, role)
    
    user_id = execute_insert(query, params)
    return user_id

def authenticate_user(username, password):
    """Authenticate user and update last login"""
    password_hash = hash_password(password)
    
    query = "SELECT * FROM users WHERE username = %s AND password_hash = %s AND is_active = TRUE"
    user = execute_query(query, (username, password_hash))
    
    if user:
        # Update last login
        update_query = "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE username = %s"
        execute_insert(update_query, (username,))
        return user[0]
    return None

def check_username_exists(username):
    """Check if username already exists"""
    query = "SELECT id FROM users WHERE username = %s"
    result = execute_query(query, (username,))
    return len(result) > 0

def check_email_exists(email):
    """Check if email already exists"""
    query = "SELECT id FROM users WHERE email = %s"
    result = execute_query(query, (email,))
    return len(result) > 0

def get_user_stats(user_id):
    """Get user statistics"""
    query = "SELECT COUNT(*) as total_logins FROM users WHERE id = %s"
    result = execute_query(query, (user_id,))
    return result[0] if result else {"total_logins": 0}