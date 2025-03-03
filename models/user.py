import sqlite3
from datetime import datetime
from utils.auth import verify_password, hash_password

class UserModel:
    def __init__(self):
        self.conn = sqlite3.connect('fitapp.db')
        self.cursor = self.conn.cursor()
    
    def check_credentials(self, username, password):
        """Verifica las credenciales del usuario y devuelve la información si son correctas"""
        # Verificar hash de contraseña
        self.cursor.execute("SELECT id, password, tipo, nombre_gimnasio FROM usuarios WHERE username = ? AND activo = 1", (username,))
        user = self.cursor.fetchone()
        
        if user and verify_password(password, user[1]):
            # Guardar ID, tipo de usuario y nombre del gimnasio para la sesión
            user_id = user[0]
            user_type = user[2]
            gym_name = user[3]
            
            # Actualizar último acceso
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute("UPDATE usuarios SET ultimo_acceso = ? WHERE id = ?", (current_time, user_id))
            self.conn.commit()
            
            # Verificar licencia para gimnasios
            if user_type == "gimnasio":
                self.cursor.execute("""
                    SELECT fecha_vencimiento, activa
                    FROM licencias
                    WHERE usuario_id = ? AND activa = 1
                    ORDER BY fecha_vencimiento DESC
                    LIMIT 1
                """, (user_id,))
                
                license_info = self.cursor.fetchone()
                if not license_info:
                    error_msg = "Su gimnasio no tiene una licencia activa. Contacte al administrador."
                    return False, error_msg
                
                fecha_venc = datetime.strptime(license_info[0], "%Y-%m-%d")
                if fecha_venc < datetime.now():
                    error_msg = "Su licencia ha vencido. Contacte al administrador para renovarla."
                    return False, error_msg
                
                # Licencia activa y no vencida
                license_expiry = license_info[0]
                return True, {"user_id": user_id, "user_type": user_type, "gym_name": gym_name, "license_expiry": license_expiry}
            
            return True, {"user_id": user_id, "user_type": user_type, "gym_name": gym_name}
        
        return False, "Usuario o contraseña incorrectos"
    
    def get_all_gyms(self):
        """Obtiene todos los gimnasios registrados"""
        self.cursor.execute("""
            SELECT id, nombre_gimnasio, username, email, fecha_registro, activo
            FROM usuarios
            WHERE tipo = 'gimnasio'
            ORDER BY nombre_gimnasio
        """)
        return self.cursor.fetchall()
    
    def add_gym(self, nombre, username, email, password):
        """Agrega un nuevo gimnasio"""
        # Verificar si el usuario o email ya existe
        self.cursor.execute("SELECT id FROM usuarios WHERE username = ?", (username,))
        if self.cursor.fetchone():
            return False, f"Ya existe un usuario con el nombre '{username}'."
        
        self.cursor.execute("SELECT id FROM usuarios WHERE email = ?", (email,))
        if self.cursor.fetchone():
            return False, f"Ya existe un usuario con el email '{email}'."
        
        # Crear hash de la contraseña
        hashed_password = hash_password(password)
        
        # Fecha de registro
        fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Insertar nuevo gimnasio
        self.cursor.execute('''
            INSERT INTO usuarios (username, password, email, tipo, nombre_gimnasio, fecha_registro, activo)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (username, hashed_password, email, "gimnasio", nombre, fecha_registro, 1))
        
        self.conn.commit()
        return True, None
    
    def update_gym(self, gym_id, nombre, username, email, password=None):
        """Actualiza los datos de un gimnasio existente"""
        # Verificar si el usuario o email pertenece a otro usuario
        self.cursor.execute("SELECT id FROM usuarios WHERE username = ? AND id != ?", (username, gym_id))
        if self.cursor.fetchone():
            return False, f"Ya existe otro usuario con el nombre '{username}'."
        
        self.cursor.execute("SELECT id FROM usuarios WHERE email = ? AND id != ?", (email, gym_id))
        if self.cursor.fetchone():
            return False, f"Ya existe otro usuario con el email '{email}'."
        
        # Actualizar datos
        if password:  # Si se proporciona nueva contraseña
            hashed_password = hash_password(password)
            self.cursor.execute('''
                UPDATE usuarios
                SET nombre_gimnasio = ?, username = ?, email = ?, password = ?
                WHERE id = ?
            ''', (nombre, username, email, hashed_password, gym_id))
        else:  # Mantener la misma contraseña
            self.cursor.execute('''
                UPDATE usuarios
                SET nombre_gimnasio = ?, username = ?, email = ?
                WHERE id = ?
            ''', (nombre, username, email, gym_id))
        
        self.conn.commit()
        return True, None
    
    def toggle_gym_active(self, gym_id):
        """Activa o desactiva un gimnasio"""
        self.cursor.execute("SELECT activo FROM usuarios WHERE id = ?", (gym_id,))
        current_state = self.cursor.fetchone()[0]
        new_state = 0 if current_state == 1 else 1
        
        self.cursor.execute("UPDATE usuarios SET activo = ? WHERE id = ?", (new_state, gym_id))
        self.conn.commit()
        
        return True
    
    def get_gym_name(self, gym_id):
        """Obtiene el nombre de un gimnasio por su ID"""
        self.cursor.execute("SELECT nombre_gimnasio FROM usuarios WHERE id = ?", (gym_id,))
        return self.cursor.fetchone()[0]
    
    def change_password(self, user_id, current_password, new_password):
        """Cambia la contraseña de un usuario"""
        # Verificar contraseña actual
        self.cursor.execute("SELECT password FROM usuarios WHERE id = ?", (user_id,))
        stored_password = self.cursor.fetchone()[0]
        
        if not verify_password(current_password, stored_password):
            return False, "La contraseña actual es incorrecta."
        
        # Actualizar contraseña
        hashed_new_password = hash_password(new_password)
        self.cursor.execute("UPDATE usuarios SET password = ? WHERE id = ?", (hashed_new_password, user_id))
        self.conn.commit()
        
        return True, None
    
    def close(self):
        """Cierra la conexión a la base de datos"""
        if hasattr(self, 'conn'):
            self.conn.close()