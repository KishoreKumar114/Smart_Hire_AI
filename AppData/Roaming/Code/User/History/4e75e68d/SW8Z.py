# check_tables.py
import mysql.connector
from mysql.connector import Error

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root", 
        password="pass123",
        database="smarthire_ai"
    )
    
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    
    print("📊 Tables in smarthire_ai database:")
    for table in tables:
        print(f" - {table[0]}")
    
    cursor.close()
    conn.close()
    
except Error as e:
    print(f"Error: {e}")