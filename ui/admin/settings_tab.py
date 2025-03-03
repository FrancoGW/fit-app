from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLabel, 
                           QLineEdit, QPushButton, QFrame, QMessageBox)

from config.constants import (FRAME_STYLE, INPUT_STYLE, BUTTON_STYLE)
from models.user import UserModel

class SettingsTab(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.user_model = UserModel()
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la pestaña de configuración"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Título de la sección
        title_label = QLabel("Configuración de la Cuenta")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title_label)
        
        # Panel de cambio de contraseña
        password_frame = QFrame()
        password_frame.setFrameShape(QFrame.Shape.StyledPanel)
        password_frame.setStyleSheet(FRAME_STYLE)
        password_layout = QVBoxLayout(password_frame)
        
        password_title = QLabel("Cambiar Contraseña")
        password_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        password_layout.addWidget(password_title)
        
        form_layout = QFormLayout()
        
        self.current_password_input = QLineEdit()
        self.current_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.current_password_input.setStyleSheet(INPUT_STYLE)
        
        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_password_input.setStyleSheet(INPUT_STYLE)
        
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password_input.setStyleSheet(INPUT_STYLE)
        
        form_layout.addRow("Contraseña Actual:", self.current_password_input)
        form_layout.addRow("Nueva Contraseña:", self.new_password_input)
        form_layout.addRow("Confirmar Contraseña:", self.confirm_password_input)
        
        password_layout.addLayout(form_layout)
        
        change_password_button = QPushButton("Cambiar Contraseña")
        change_password_button.setStyleSheet(BUTTON_STYLE)
        change_password_button.clicked.connect(self.change_password)
        password_layout.addWidget(change_password_button)
        
        layout.addWidget(password_frame)
        
        # Información del sistema
        info_frame = QFrame()
        info_frame.setFrameShape(QFrame.Shape.StyledPanel)
        info_frame.setStyleSheet(FRAME_STYLE)
        info_layout = QVBoxLayout(info_frame)
        
        info_title = QLabel("Información del Sistema")
        info_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        info_layout.addWidget(info_title)
        
        version_label = QLabel("Versión: FIT APP 1.0")
        build_label = QLabel("Build: 2025.03.01")
        license_label = QLabel("Licencia: Comercial")
        
        info_layout.addWidget(version_label)
        info_layout.addWidget(build_label)
        info_layout.addWidget(license_label)
        
        layout.addWidget(info_frame)
        layout.addStretch()
    
    def change_password(self):
        """Cambia la contraseña del administrador"""
        current_password = self.current_password_input.text()
        new_password = self.new_password_input.text()
        confirm_password = self.confirm_password_input.text()
        
        if not current_password or not new_password or not confirm_password:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return
        
        if new_password != confirm_password:
            QMessageBox.warning(self, "Error", "Las nuevas contraseñas no coinciden.")
            return
        
        if len(new_password) < 6:
            QMessageBox.warning(self, "Error", "La nueva contraseña debe tener al menos 6 caracteres.")
            return
        
        success, error_msg = self.user_model.change_password(self.user_id, current_password, new_password)
        
        if success:
            QMessageBox.information(self, "Éxito", "Contraseña actualizada correctamente.")
            
            # Limpiar campos
            self.current_password_input.clear()
            self.new_password_input.clear()
            self.confirm_password_input.clear()
        else:
            QMessageBox.warning(self, "Error", error_msg)