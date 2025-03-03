import sqlite3
from datetime import datetime

class AttendanceModel:
    def __init__(self):
        self.conn = sqlite3.connect('gym.db')
        self.cursor = self.conn.cursor()
    
    def register_attendance(self, member_id):
        """Registra la asistencia de un socio"""
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("INSERT INTO asistencias (socio_id, fecha) VALUES (?, ?)", 
                         (member_id, fecha_actual))
        self.conn.commit()
        return True
    
    def get_monthly_attendance(self, gym_id):
        """Obtiene las asistencias del mes actual para un gimnasio"""
        first_day = datetime.now().replace(day=1).strftime("%Y-%m-%d")
        self.cursor.execute("""
            SELECT a.fecha, s.nombre, s.apellido, s.dni
            FROM asistencias a
            JOIN socios s ON a.socio_id = s.id
            WHERE s.gimnasio_id = ? AND a.fecha >= ?
            ORDER BY a.fecha DESC
        """, (gym_id, first_day))
        return self.cursor.fetchall()
    
    def get_attendance_count(self, gym_id):
        """Obtiene el número de asistencias del mes para un gimnasio"""
        first_day = datetime.now().replace(day=1).strftime("%Y-%m-%d")
        self.cursor.execute("""
            SELECT COUNT(*) FROM asistencias a
            JOIN socios s ON a.socio_id = s.id
            WHERE s.gimnasio_id = ? AND a.fecha >= ?
        """, (gym_id, first_day))
        return self.cursor.fetchone()[0]
    
    def close(self):
        """Cierra la conexión a la base de datos"""
        if hasattr(self, 'conn'):
            self.conn.close()