import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._conn = None
        return cls._instance

    def connect(self):
        try:
            if self._conn is None or not self._conn.is_connected():
                self._conn = mysql.connector.connect(
                    host=os.getenv('DB_HOST', 'localhost'),
                    user=os.getenv('DB_USER', 'root'),
                    password=os.getenv('DB_PASS', ''),
                    database=os.getenv('DB_NAME', 'faceabsensi')
                )
            return self._conn
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None

    def execute_query(self, query, params=None):
        conn = self.connect()
        if conn:
            try:
                cursor = conn.cursor(dictionary=True, buffered=True)
                cursor.execute(query, params or ())
                conn.commit()
                return cursor
            except Error as e:
                print(f"Query error: {e}")
        return None

    def fetch_all(self, query, params=None):
        cursor = self.execute_query(query, params)
        if cursor:
            results = cursor.fetchall()
            cursor.close()
            return results
        return []

    def fetch_one(self, query, params=None):
        cursor = self.execute_query(query, params)
        if cursor:
            result = cursor.fetchone()
            # Consume remaining results if any to avoid "Unread result found"
            cursor.fetchall() 
            cursor.close()
            return result
        return None

    # Specific Methods
    def authenticate_user(self, username, password):
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        return self.fetch_one(query, (username, password))

    def add_student(self, student_id, name, class_name, face_encoding, photo_path):
        query = "INSERT INTO students (student_id, name, class_name, face_encoding, photo_path) VALUES (%s, %s, %s, %s, %s)"
        return self.execute_query(query, (student_id, name, class_name, face_encoding, photo_path))

    def get_all_students(self):
        return self.fetch_all("SELECT * FROM students")

    def log_attendance(self, student_id, date, time, proof_path):
        query = "INSERT IGNORE INTO attendance (student_id, attendance_date, attendance_time, proof_path) VALUES (%s, %s, %s, %s)"
        return self.execute_query(query, (student_id, date, time, proof_path))

    def get_todays_stats(self):
        stats = self.fetch_one("SELECT COUNT(*) as count FROM students")
        total_students = stats['count'] if stats else 0
        
        stats_today = self.fetch_one("SELECT COUNT(*) as count FROM attendance WHERE attendance_date = CURDATE()")
        present_today = stats_today['count'] if stats_today else 0
        
        return total_students, present_today

    def get_recent_activity(self, limit=10):
        query = """
            SELECT a.attendance_time, s.name, s.class_name, a.status 
            FROM attendance a 
            JOIN students s ON a.student_id = s.student_id 
            ORDER BY a.id DESC LIMIT %s
        """
        return self.fetch_all(query, (limit,))
