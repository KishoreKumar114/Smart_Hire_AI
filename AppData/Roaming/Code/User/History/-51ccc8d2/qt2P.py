# database.py
import mysql.connector
from mysql.connector import Error
import streamlit as st

@st.cache_resource
def init_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # change to your MySQL username
            password="pass123",  # change to your MySQL password
            database="smarthire_ai"
        )
        return connection
    except Error as e:
        st.error(f"Error connecting to MySQL: {e}")
        return None

def get_cursor():
    conn = init_connection()
    if conn:
        return conn.cursor(dictionary=True)
    return None

def execute_query(query, params=None):
    conn = init_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params or ())
            result = cursor.fetchall()
            conn.commit()
            return result
        except Error as e:
            st.error(f"Query error: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
    return None

def execute_insert(query, params=None):
    conn = init_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            conn.commit()
            return cursor.lastrowid
        except Error as e:
            st.error(f"Insert error: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
    return None