import sqlite3
from datetime import datetime, timedelta

class MemberModel:
    def __init__(self):
        self.conn = sqlite3.connect('gym.db')
        self.cursor = self.conn.cursor()
    
    def get_all_members(self, gym_id):
        """Obtiene todos los socios de un gimnasio"""
        self.cursor.execute("""
            SELECT s.id, s.nombre, s.apellido, s.dni, s.telefono, s.fecha_vencimiento, s.estado_cuota, p.nombre 
            FROM socios s
            LEFT JOIN planes p ON s.plan_id = p.id
            WHERE s.gimnasio_id = ?
        """, (gym_id,))
        return self.cursor.fetchall()
    
    def get_member_by_dni(self, dni, gym_id):
        """Busca un socio por su DNI"""
        self.cursor.execute('''
            SELECT s.id, s.nombre, s.apellido, s.fecha_vencimiento, s.estado_cuota, 
                p.nombre as plan_nombre, p.descripcion as plan_descripcion
            FROM socios s
            LEFT JOIN planes p ON s.plan_id = p.id
            WHERE s.dni = ? AND s.gimnasio_id = ?
        ''', (dni, gym_id))
        return self.cursor.fetchone()
    
    def register_attendance(self, member_id):
        """Registra la asistencia de un socio"""
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("INSERT INTO asistencias (socio_id, fecha) VALUES (?, ?)", 
                         (member_id, fecha_actual))
        self.conn.commit()
        return True
    
    def check_membership_status(self, member_id, fecha_vencimiento):
        """Verifica el estado de la membresía de un socio"""
        fecha_venc = datetime.strptime(fecha_vencimiento, "%Y-%m-%d")
        fecha_actual = datetime.now()
        dias_restantes = (fecha_venc - fecha_actual).days
        
        if dias_restantes <= 0:
            # Actualizar estado a no pagada si venció
            self.cursor.execute('''
                UPDATE socios
                SET estado_cuota = 'No Pagada'
                WHERE id = ?
            ''', (member_id,))
            self.conn.commit()
            
            return "vencida", 0
        elif dias_restantes <= 10:
            return "por_vencer", dias_restantes
        else:
            return "al_dia", dias_restantes
    
    def add_member(self, nombre, apellido, dni, telefono, plan_id, estado_cuota, gym_id):
        """Agrega un nuevo socio"""
        # Verificar si el DNI ya existe
        self.cursor.execute("SELECT id FROM socios WHERE dni = ?", (dni,))
        if self.cursor.fetchone():
            return False, f"Ya existe un socio con el DNI {dni}."
        
        # Fechas de registro y vencimiento
        fecha_registro = datetime.now().strftime("%Y-%m-%d")
        fecha_vencimiento = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        
        # Insertar nuevo socio
        self.cursor.execute('''
            INSERT INTO socios (nombre, apellido, dni, telefono, plan_id, fecha_registro, fecha_vencimiento, estado_cuota, gimnasio_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (nombre, apellido, dni, telefono, plan_id, fecha_registro, fecha_vencimiento, estado_cuota, gym_id))
        
        self.conn.commit()
        return True, None
    
    def update_member(self, member_id, nombre, apellido, dni, telefono, plan_id, estado_cuota):
        """Actualiza los datos de un socio existente"""
        # Verificar si el DNI pertenece a otro socio
        self.cursor.execute("SELECT id FROM socios WHERE dni = ? AND id != ?", (dni, member_id))
        if self.cursor.fetchone():
            return False, f"Ya existe otro socio con el DNI {dni}."
        
        # Obtener el estado actual
        self.cursor.execute("SELECT estado_cuota FROM socios WHERE id = ?", (member_id,))
        estado_actual = self.cursor.fetchone()[0]
        
        # Si el estado cambia a "Pagada", actualizar la fecha de vencimiento
        if estado_cuota == "Pagada" and estado_actual == "No Pagada":
            # Actualizar fecha de vencimiento
            fecha_vencimiento = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
            
            self.cursor.execute('''
                UPDATE socios
                SET nombre = ?, apellido = ?, dni = ?, telefono = ?, plan_id = ?,
                    fecha_vencimiento = ?, estado_cuota = ?
                WHERE id = ?
            ''', (nombre, apellido, dni, telefono, plan_id, fecha_vencimiento, estado_cuota, member_id))
        else:
            # Mantener la fecha de vencimiento actual
            self.cursor.execute('''
                UPDATE socios
                SET nombre = ?, apellido = ?, dni = ?, telefono = ?, plan_id = ?, estado_cuota = ?
                WHERE id = ?
            ''', (nombre, apellido, dni, telefono, plan_id, estado_cuota, member_id))
        
        self.conn.commit()
        return True, None
    
    def delete_member(self, member_id):
        """Elimina un socio y sus asistencias"""
        # Eliminar socio
        self.cursor.execute("DELETE FROM socios WHERE id = ?", (member_id,))
        # Eliminar asistencias asociadas
        self.cursor.execute("DELETE FROM asistencias WHERE socio_id = ?", (member_id,))
        
        self.conn.commit()
        return True
    
    def get_attendance_stats(self, gym_id):
        """Obtiene estadísticas de asistencia para un gimnasio"""
        first_day = datetime.now().replace(day=1).strftime("%Y-%m-%d")
        self.cursor.execute("""
            SELECT COUNT(*) FROM asistencias a
            JOIN socios s ON a.socio_id = s.id
            WHERE s.gimnasio_id = ? AND a.fecha >= ?
        """, (gym_id, first_day))
        return self.cursor.fetchone()[0]
    
    def get_member_status_stats(self, gym_id):
        """Obtiene estadísticas sobre el estado de los socios"""
        # Total de socios
        self.cursor.execute("SELECT COUNT(*) FROM socios WHERE gimnasio_id = ?", (gym_id,))
        total_members = self.cursor.fetchone()[0]
        
        # Socios con cuota al día
        self.cursor.execute("SELECT COUNT(*) FROM socios WHERE gimnasio_id = ? AND estado_cuota = 'Pagada'", (gym_id,))
        active_members = self.cursor.fetchone()[0]
        
        return {
            "total": total_members,
            "active": active_members,
            "percent_active": (active_members / total_members * 100) if total_members > 0 else 0
        }
    
    def export_members_report(self, gym_id):
        """Obtiene datos para exportar reporte de socios"""
        self.cursor.execute("""
            SELECT s.id, s.nombre, s.apellido, s.dni, s.telefono, s.fecha_registro, 
                   s.fecha_vencimiento, s.estado_cuota, p.nombre as plan 
            FROM socios s
            LEFT JOIN planes p ON s.plan_id = p.id
            WHERE s.gimnasio_id = ?
            ORDER BY s.apellido, s.nombre
        """, (gym_id,))
        
        return self.cursor.fetchall()
    
    def export_attendance_report(self, gym_id):
        """Obtiene datos para exportar reporte de asistencias"""
        # Obtener rango de fechas
        start_date = datetime.now().replace(day=1).strftime("%Y-%m-%d")  # Primer día del mes
        end_date = datetime.now().strftime("%Y-%m-%d")  # Hoy
        
        self.cursor.execute("""
            SELECT a.fecha, s.nombre, s.apellido, s.dni
            FROM asistencias a
            JOIN socios s ON a.socio_id = s.id
            WHERE s.gimnasio_id = ? AND a.fecha BETWEEN ? AND ?
            ORDER BY a.fecha DESC, s.apellido, s.nombre
        """, (gym_id, start_date, end_date))
        
        return self.cursor.fetchall()
    
    def close(self):
        """Cierra la conexión a la base de datos"""
        if hasattr(self, 'conn'):
            self.conn.close()