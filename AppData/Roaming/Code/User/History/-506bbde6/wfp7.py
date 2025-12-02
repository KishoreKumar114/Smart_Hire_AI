# test_connection.py
import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="pass123",
        database="smarthire_ai"
    )
    
    if connection.is_connected():
        print("✅ MySQL Connection Successful!")
        
        # Check if database exists
        cursor = connection.cursor()
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        print("Available databases:")
        for db in databases:
            print(f" - {db[0]}")
            
        cursor.close()
        connection.close()
        
except Error as e:
    print(f"❌ Connection failed: {e}")