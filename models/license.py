import sqlite3
from datetime import datetime, timedelta

class LicenseModel:
    def __init__(self):
        self.conn = sqlite3.connect('fitapp.db')
        self.cursor = self.conn.cursor()
    
    def get_all_licenses(self):
        """Obtiene todas las licencias"""
        self.cursor.execute("""
            SELECT l.id, u.nombre_gimnasio, l.tipo, l.fecha_inicio, l.fecha_vencimiento, l.precio, l.activa
            FROM licencias l
            JOIN usuarios u ON l.usuario_id = u.id
            ORDER BY l.fecha_vencimiento DESC
        """)
        return self.cursor.fetchall()
    
    def get_active_gyms(self):
        """Obtiene todos los gimnasios activos para asignar licencias"""
        self.cursor.execute("""
            SELECT id, nombre_gimnasio
            FROM usuarios
            WHERE tipo = 'gimnasio' AND activo = 1
            ORDER BY nombre_gimnasio
        """)
        return self.cursor.fetchall()
    
    def add_license(self, gym_id, license_type, start_date, price):
        """Añade una nueva licencia a un gimnasio"""
        # Calcular fecha de vencimiento según tipo
        days_mapping = {
            "Mensual": 30,
            "Trimestral": 90,
            "Semestral": 180,
            "Anual": 365
        }
        
        days = days_mapping.get(license_type, 30)
        end_date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=days)).strftime("%Y-%m-%d")
        
        # Verificar si ya existe una licencia activa
        self.cursor.execute("""
            SELECT id FROM licencias
            WHERE usuario_id = ? AND activa = 1
        """, (gym_id,))
        
        existing_license = self.cursor.fetchone()
        
        if existing_license:
            # Revocar licencia anterior
            self.cursor.execute("""
                UPDATE licencias
                SET activa = 0
                WHERE usuario_id = ? AND activa = 1
            """, (gym_id,))
        
        # Insertar nueva licencia
        self.cursor.execute("""
            INSERT INTO licencias (usuario_id, tipo, fecha_inicio, fecha_vencimiento, precio, activa)
            VALUES (?, ?, ?, ?, ?, 1)
        """, (gym_id, license_type, start_date, end_date, price))
        
        self.conn.commit()
        return True
    
    def revoke_license(self, license_id):
        """Revoca una licencia activa"""
        self.cursor.execute("UPDATE licencias SET activa = 0 WHERE id = ?", (license_id,))
        self.conn.commit()
        return True
    
    def get_gym_license_info(self, gym_id):
        """Obtiene información de la licencia activa de un gimnasio"""
        self.cursor.execute("""
            SELECT fecha_vencimiento FROM licencias
            WHERE usuario_id = ? AND activa = 1
            ORDER BY fecha_vencimiento DESC
            LIMIT 1
        """, (gym_id,))
        
        license_info = self.cursor.fetchone()
        
        if license_info:
            fecha_venc = license_info[0]
            days_left = (datetime.strptime(fecha_venc, "%Y-%m-%d") - datetime.now()).days
            return {"fecha_vencimiento": fecha_venc, "days_left": days_left}
        
        return None
    
    def get_license_stats(self):
        """Obtiene estadísticas de licencias"""
        # Total de gimnasios
        self.cursor.execute("SELECT COUNT(*) FROM usuarios WHERE tipo = 'gimnasio'")
        total_gyms = self.cursor.fetchone()[0]
        
        # Gimnasios activos
        self.cursor.execute("SELECT COUNT(*) FROM usuarios WHERE tipo = 'gimnasio' AND activo = 1")
        active_gyms = self.cursor.fetchone()[0]
        
        # Licencias activas
        self.cursor.execute("SELECT COUNT(*) FROM licencias WHERE activa = 1")
        active_licenses = self.cursor.fetchone()[0]
        
        # Calcular ingresos totales
        self.cursor.execute("SELECT SUM(precio) FROM licencias")
        total_revenue = self.cursor.fetchone()[0] or 0
        
        return {
            "total_gyms": total_gyms,
            "active_gyms": active_gyms,
            "active_licenses": active_licenses,
            "total_revenue": total_revenue,
            "percent_active": (active_gyms/total_gyms*100) if total_gyms > 0 else 0
        }
    
    def close(self):
        """Cierra la conexión a la base de datos"""
        if hasattr(self, 'conn'):
            self.conn.close()