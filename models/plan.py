import sqlite3

class PlanModel:
    def __init__(self):
        self.conn = sqlite3.connect('gym.db')
        self.cursor = self.conn.cursor()
    
    def get_all_plans(self):
        """Obtiene todos los planes"""
        self.cursor.execute("SELECT id, nombre, descripcion, precio FROM planes")
        return self.cursor.fetchall()
    
    def get_plan_by_id(self, plan_id):
        """Obtiene un plan por su ID"""
        self.cursor.execute("SELECT id, nombre, descripcion, precio FROM planes WHERE id = ?", (plan_id,))
        return self.cursor.fetchone()
    
    def get_plan_by_name(self, name):
        """Obtiene un plan por su nombre"""
        self.cursor.execute("SELECT id FROM planes WHERE nombre = ?", (name,))
        return self.cursor.fetchone()
    
    def add_plan(self, nombre, descripcion, precio):
        """Agrega un nuevo plan"""
        # Verificar si el nombre ya existe
        self.cursor.execute("SELECT id FROM planes WHERE nombre = ?", (nombre,))
        if self.cursor.fetchone():
            return False, f"Ya existe un plan con el nombre {nombre}."
        
        # Insertar nuevo plan
        self.cursor.execute('''
            INSERT INTO planes (nombre, descripcion, precio)
            VALUES (?, ?, ?)
        ''', (nombre, descripcion, precio))
        
        self.conn.commit()
        return True, None
    
    def update_plan(self, plan_id, nombre, descripcion, precio):
        """Actualiza un plan existente"""
        # Verificar si el nombre pertenece a otro plan
        self.cursor.execute("SELECT id FROM planes WHERE nombre = ? AND id != ?", (nombre, plan_id))
        if self.cursor.fetchone():
            return False, f"Ya existe otro plan con el nombre {nombre}."
        
        # Actualizar plan
        self.cursor.execute('''
            UPDATE planes
            SET nombre = ?, descripcion = ?, precio = ?
            WHERE id = ?
        ''', (nombre, descripcion, precio, plan_id))
        
        self.conn.commit()
        return True, None
    
    def delete_plan(self, plan_id, gym_id):
        """Elimina un plan"""
        # Verificar si hay socios usando este plan
        self.cursor.execute("SELECT COUNT(*) FROM socios WHERE plan_id = ? AND gimnasio_id = ?", 
                          (plan_id, gym_id))
        count = self.cursor.fetchone()[0]
        
        if count > 0:
            return False, f"No se puede eliminar este plan porque hay {count} socios que lo están usando."
        
        # Eliminar plan
        self.cursor.execute("DELETE FROM planes WHERE id = ?", (plan_id,))
        self.conn.commit()
        return True, None
    
    def get_all_plan_names(self):
        """Obtiene los nombres de todos los planes"""
        self.cursor.execute("SELECT nombre FROM planes ORDER BY nombre")
        return [plan[0] for plan in self.cursor.fetchall()]
    
    def close(self):
        """Cierra la conexión a la base de datos"""
        if hasattr(self, 'conn'):
            self.conn.close()