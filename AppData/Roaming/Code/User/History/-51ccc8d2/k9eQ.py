# database.py - SIMPLE FIXED VERSION
import mysql.connector
from mysql.connector import Error
import streamlit as st
import hashlib

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

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, email, password, role="user"):
    """Create new user in database"""
    hashed_password = hash_password(password)
    query = """
    INSERT INTO users (username, email, password_hash, role, created_at)
    VALUES (%s, %s, %s, %s, NOW())
    """
    return execute_insert(query, (username, email, hashed_password, role))

def verify_user(username, password):
    """Verify user credentials"""
    hashed_password = hash_password(password)
    query = "SELECT * FROM users WHERE username = %s AND password_hash = %s"
    result = execute_query(query, (username, hashed_password))
    return result[0] if result else None

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

def get_user_by_username(username):
    """Get user by username"""
    query = "SELECT * FROM users WHERE username = %s"
    result = execute_query(query, (username,))
    return result[0] if result else None