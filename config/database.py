import sqlite3
from datetime import datetime
from utils.auth import hash_password
from config.constants import DEFAULT_ADMIN_USERNAME, DEFAULT_ADMIN_PASSWORD

def init_admin_database():
    """Inicializa la base de datos del administrador"""
    conn = sqlite3.connect('fitapp.db')
    cursor = conn.cursor()
    
    # Crear tabla de usuarios (dueños de gimnasios que compran el software)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE,
            tipo TEXT NOT NULL,
            nombre_gimnasio TEXT,
            fecha_registro TEXT NOT NULL,
            ultimo_acceso TEXT,
            activo INTEGER DEFAULT 1
        )
    ''')
    
    # Crear tabla de licencias para los usuarios (gimnasios)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS licencias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            tipo TEXT NOT NULL,
            fecha_inicio TEXT NOT NULL,
            fecha_vencimiento TEXT NOT NULL,
            precio REAL NOT NULL,
            activa INTEGER DEFAULT 1,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
    ''')
    
    # Verificar si existe el usuario admin
    cursor.execute("SELECT COUNT(*) FROM usuarios WHERE username = ?", (DEFAULT_ADMIN_USERNAME,))
    if cursor.fetchone()[0] == 0:
        # Crear usuario admin predeterminado
        hashed_password = hash_password(DEFAULT_ADMIN_PASSWORD)
        fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT INTO usuarios (username, password, email, tipo, nombre_gimnasio, fecha_registro, activo) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (DEFAULT_ADMIN_USERNAME, hashed_password, "admin@fitapp.com", "admin", "Administración FitApp", fecha_registro, 1)
        )
    
    conn.commit()
    conn.close()

def init_gym_database():
    """Inicializa la base de datos del gimnasio"""
    conn = sqlite3.connect('gym.db')
    cursor = conn.cursor()
    
    # Crear tabla de planes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS planes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            precio REAL NOT NULL
        )
    ''')
    
    # Crear tabla de socios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS socios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            dni TEXT UNIQUE NOT NULL,
            telefono TEXT,
            plan_id INTEGER,
            fecha_registro TEXT NOT NULL,
            fecha_vencimiento TEXT NOT NULL,
            estado_cuota TEXT NOT NULL,
            gimnasio_id INTEGER,
            FOREIGN KEY (plan_id) REFERENCES planes (id),
            FOREIGN KEY (gimnasio_id) REFERENCES usuarios (id)
        )
    ''')
    
    # Crear tabla de asistencias
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS asistencias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            socio_id INTEGER,
            fecha TEXT NOT NULL,
            FOREIGN KEY (socio_id) REFERENCES socios (id)
        )
    ''')   
    
    # Verificar si la columna plan_id existe en la tabla socios, y si no, añadirla
    try:
        cursor.execute("SELECT plan_id FROM socios LIMIT 1")
    except sqlite3.OperationalError:
        # Si ocurre un error, significa que la columna no existe
        cursor.execute("ALTER TABLE socios ADD COLUMN plan_id INTEGER")
        conn.commit()
        print("Columna plan_id añadida a la tabla socios")
    
    # Verificar si la columna gimnasio_id existe en la tabla socios, y si no, añadirla
    try:
        cursor.execute("SELECT gimnasio_id FROM socios LIMIT 1")
    except sqlite3.OperationalError:
        # Si ocurre un error, significa que la columna no existe
        cursor.execute("ALTER TABLE socios ADD COLUMN gimnasio_id INTEGER")
        conn.commit()
        print("Columna gimnasio_id añadida a la tabla socios")
    
    # Insertar plan básico si no existe ninguno
    cursor.execute("SELECT COUNT(*) FROM planes")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO planes (nombre, descripcion, precio)
            VALUES (?, ?, ?)
        ''', ("Plan Básico", "Acceso a todas las instalaciones", 5000.0))
    
    conn.commit()
    conn.close()