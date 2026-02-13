import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def initialize_database():
    host = os.getenv('DB_HOST', 'localhost')
    user = os.getenv('DB_USER', 'root')
    password = os.getenv('DB_PASS', '')
    db_name = os.getenv('DB_NAME', 'faceabsensi')

    try:
        # Connect to MySQL (without database)
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        cursor = conn.cursor()

        # Create database if not exists
        print(f"Creating database '{db_name}' if it doesn't exist...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        
        # Switch to the database
        cursor.execute(f"USE {db_name}")

        # Read schema.sql
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        if not os.path.exists(schema_path):
            print(f"Error: {schema_path} not found!")
            return

        with open(schema_path, 'r') as f:
            sql_commands = f.read().split(';')

        # Execute each command
        print("Executing schema commands...")
        for command in sql_commands:
            if command.strip():
                try:
                    cursor.execute(command)
                except Error as e:
                    print(f"Error executing command: {e}")
        
        conn.commit()
        print("Database initialized successfully!")

    except Error as e:
        print(f"Error: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    initialize_database()
