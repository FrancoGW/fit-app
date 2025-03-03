from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLabel, 
                           QLineEdit, QCheckBox, QPushButton)
from PyQt6.QtCore import Qt

from config.constants import (BG_COLOR, TEXT_PRIMARY, TEXT_SECONDARY, 
                            PRIMARY_COLOR, BORDER_COLOR, DANGER_COLOR,
                            BUTTON_STYLE, INPUT_STYLE)
from models.user import UserModel
from config.database import init_admin_database

class LoginWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("FIT APP - Iniciar Sesión")
        self.setFixedSize(400, 500)
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {BG_COLOR};
                color: {TEXT_PRIMARY};
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
            QLabel {{
                color: {TEXT_PRIMARY};
            }}
            QLabel#titleLabel {{
                color: {PRIMARY_COLOR};
                font-size: 28px;
                font-weight: bold;
            }}
            QLabel#subtitleLabel {{
                color: {TEXT_SECONDARY};
                font-size: 14px;
            }}
            QCheckBox {{
                color: {TEXT_SECONDARY};
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border: 1px solid {BORDER_COLOR};
                border-radius: 4px;
            }}
            QCheckBox::indicator:checked {{
                background-color: {PRIMARY_COLOR};
                border: 1px solid {PRIMARY_COLOR};
            }}
        """)
        
        self.setup_ui()
        init_admin_database()
        self.user_model = UserModel()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        # Logo y título
        title_label = QLabel("FIT APP")
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        subtitle_label = QLabel("Sistema de Gestión para Gimnasios")
        subtitle_label.setObjectName("subtitleLabel")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle_label)
        
        # Espacio
        layout.addSpacing(20)
        
        # Formulario
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        
        # Username
        username_label = QLabel("Usuario:")
        self.username_input = QLineEdit()
        self.username_input.setStyleSheet(INPUT_STYLE)
        self.username_input.setPlaceholderText("Ingrese su nombre de usuario")
        form_layout.addRow(username_label, self.username_input)
        
        # Password
        password_label = QLabel("Contraseña:")
        self.password_input = QLineEdit()
        self.password_input.setStyleSheet(INPUT_STYLE)
        self.password_input.setPlaceholderText("Ingrese su contraseña")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow(password_label, self.password_input)
        
        layout.addLayout(form_layout)
        
        # Remember me
        self.remember_checkbox = QCheckBox("Recordar usuario")
        layout.addWidget(self.remember_checkbox)
        
        # Espacio
        layout.addSpacing(10)
        
        # Login button
        login_button = QPushButton("Iniciar Sesión")
        login_button.setStyleSheet(BUTTON_STYLE)
        login_button.setFixedHeight(45)
        login_button.clicked.connect(self.authenticate)
        layout.addWidget(login_button)
        
        # Info about default admin account
        info_label = QLabel("Admin por defecto: usuario=admin, contraseña=admin123")
        info_label.setStyleSheet(f"color: {TEXT_SECONDARY}; font-size: 12px;")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info_label)
        
        # Error message
        self.error_label = QLabel("")
        self.error_label.setStyleSheet(f"color: {DANGER_COLOR}; font-weight: bold;")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.error_label)
        
        layout.addStretch()
        
    def authenticate(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            self.error_label.setText("Ingrese usuario y contraseña")
            return
        
        # Verificar credenciales
        success, result = self.user_model.check_credentials(username, password)
        
        if success:
            # Guardar los datos de la sesión
            self.user_id = result["user_id"]
            self.user_type = result["user_type"]
            self.gym_name = result["gym_name"]
            if "license_expiry" in result:
                self.license_expiry = result["license_expiry"]
            
            self.accept()
        else:
            self.error_label.setText(result)
            
    def accept(self):
        self.accepted = True
        self.close()
        
    def closeEvent(self, event):
        # Cerrar conexión a la base de datos
        if hasattr(self, 'user_model'):
            self.user_model.close()
        event.accept()