import pandas as pd
from database.db_handler import Database
import os
from datetime import datetime

class ExcelExporter:
    def __init__(self):
        self.db = Database()

    def export_attendance(self, start_date=None, end_date=None):
        """Export attendance data to Excel."""
        query = """
            SELECT a.attendance_date, a.attendance_time, s.student_id, s.name, s.class_name, a.status 
            FROM attendance a 
            JOIN students s ON a.student_id = s.student_id
        """
        params = []
        if start_date and end_date:
            query += " WHERE a.attendance_date BETWEEN %s AND %s"
            params = [start_date, end_date]
        
        data = self.db.fetch_all(query, params)
        if not data:
            return False, "No data found for the selected range."

        df = pd.DataFrame(data)
        
        if not os.path.exists('exports'):
            os.makedirs('exports')
            
        filename = f"exports/Attendance_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        df.to_excel(filename, index=False)
        return True, filename
