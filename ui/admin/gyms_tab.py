from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, 
                           QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, 
                           QHeaderView, QFrame, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from config.constants import (TEXT_PRIMARY, FRAME_STYLE, INPUT_STYLE, BUTTON_STYLE, 
                            SECONDARY_BUTTON_STYLE, TABLE_STYLE, SUCCESS_COLOR, 
                            DANGER_COLOR)
from models.user import UserModel

class GymsTab(QWidget):
    def __init__(self, user_id, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.parent = parent  # Guardar referencia al padre
        self.user_model = UserModel()
        self.selected_gym_id = None
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz de usuario de la pestaña de gimnasios"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Título de la sección
        title_label = QLabel("Gestión de Clientes Gimnasios")
        title_label.setObjectName("sectionTitle")
        layout.addWidget(title_label)
        
        # Formulario para añadir/editar gimnasios
        form_frame = QFrame()
        form_frame.setStyleSheet(FRAME_STYLE)
        form_frame.setFrameShape(QFrame.Shape.StyledPanel)
        form_layout = QFormLayout(form_frame)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setSpacing(15)
        
        self.gym_name_input = QLineEdit()
        self.gym_name_input.setStyleSheet(INPUT_STYLE)
        self.gym_name_input.setPlaceholderText("Nombre del gimnasio")
        
        self.gym_username_input = QLineEdit()
        self.gym_username_input.setStyleSheet(INPUT_STYLE)
        self.gym_username_input.setPlaceholderText("Nombre de usuario")
        
        self.gym_email_input = QLineEdit()
        self.gym_email_input.setStyleSheet(INPUT_STYLE)
        self.gym_email_input.setPlaceholderText("Email")
        
        self.gym_password_input = QLineEdit()
        self.gym_password_input.setStyleSheet(INPUT_STYLE)
        self.gym_password_input.setPlaceholderText("Contraseña")
        self.gym_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        form_layout.addRow("Nombre del Gimnasio:", self.gym_name_input)
        form_layout.addRow("Nombre de Usuario:", self.gym_username_input)
        form_layout.addRow("Email:", self.gym_email_input)
        form_layout.addRow("Contraseña:", self.gym_password_input)
        
        layout.addWidget(form_frame)
        
        # Botones para gestionar gimnasios
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.add_gym_button = QPushButton("Registrar Gimnasio")
        self.add_gym_button.setStyleSheet(BUTTON_STYLE)
        self.add_gym_button.clicked.connect(self.add_gym)
        
        self.update_gym_button = QPushButton("Actualizar Gimnasio")
        self.update_gym_button.setStyleSheet(SECONDARY_BUTTON_STYLE)
        self.update_gym_button.clicked.connect(self.update_gym)
        self.update_gym_button.setEnabled(False)
        
        self.toggle_gym_button = QPushButton("Activar/Desactivar")
        self.toggle_gym_button.setStyleSheet(SECONDARY_BUTTON_STYLE)
        self.toggle_gym_button.clicked.connect(self.toggle_gym_active)
        self.toggle_gym_button.setEnabled(False)
        
        self.clear_gym_button = QPushButton("Limpiar")
        self.clear_gym_button.setStyleSheet(SECONDARY_BUTTON_STYLE)
        self.clear_gym_button.clicked.connect(self.clear_gym_form)
        
        button_layout.addWidget(self.add_gym_button)
        button_layout.addWidget(self.update_gym_button)
        button_layout.addWidget(self.toggle_gym_button)
        button_layout.addWidget(self.clear_gym_button)
        
        layout.addLayout(button_layout)
        
        # Tabla de gimnasios
        self.gyms_table = QTableWidget()
        self.gyms_table.setStyleSheet(TABLE_STYLE)
        self.gyms_table.setColumnCount(6)
        self.gyms_table.setHorizontalHeaderLabels([
            "ID", "Nombre", "Usuario", "Email", "Fecha Registro", "Estado"
        ])
        self.gyms_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.gyms_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.gyms_table.cellClicked.connect(self.select_gym)
        self.gyms_table.setAlternatingRowColors(True)
        
        layout.addWidget(self.gyms_table)
        
        # Cargar datos en la tabla
        self.load_gyms()
    
    def load_gyms(self):
        """Carga la lista de gimnasios en la tabla"""
        gyms = self.user_model.get_all_gyms()
        
        self.gyms_table.setRowCount(0)  # Limpiar tabla
        
        for row_idx, gym in enumerate(gyms):
            self.gyms_table.insertRow(row_idx)
            
            for col_idx, value in enumerate(gym):
                # Formatear el valor de activo
                if col_idx == 5:  # Columna de estado (activo/inactivo)
                    value = "Activo" if value == 1 else "Inactivo"
                
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                
                # Colorear según el estado
                if col_idx == 5:
                    if value == "Activo":
                        item.setForeground(QColor(SUCCESS_COLOR))
                    else:
                        item.setForeground(QColor(DANGER_COLOR))
                
                self.gyms_table.setItem(row_idx, col_idx, item)
    
    def clear_gym_form(self):
        """Limpia el formulario de gimnasios"""
        self.gym_name_input.clear()
        self.gym_username_input.clear()
        self.gym_email_input.clear()
        self.gym_password_input.clear()
        
        self.add_gym_button.setEnabled(True)
        self.update_gym_button.setEnabled(False)
        self.toggle_gym_button.setEnabled(False)
        
        # Limpiar selección de la tabla
        self.gyms_table.clearSelection()
        self.selected_gym_id = None
    
    def select_gym(self, row, column):
        """Selecciona un gimnasio de la tabla para editar"""
        self.selected_gym_id = int(self.gyms_table.item(row, 0).text())
        
        # Cargar datos en el formulario
        self.gym_name_input.setText(self.gyms_table.item(row, 1).text())
        self.gym_username_input.setText(self.gyms_table.item(row, 2).text())
        self.gym_email_input.setText(self.gyms_table.item(row, 3).text())
        
        # No cargar la contraseña por seguridad
        self.gym_password_input.clear()
        
        # Activar botones
        self.add_gym_button.setEnabled(False)
        self.update_gym_button.setEnabled(True)
        self.toggle_gym_button.setEnabled(True)
    
    def add_gym(self):
        """Agrega un nuevo gimnasio a la base de datos"""
        nombre = self.gym_name_input.text().strip()
        username = self.gym_username_input.text().strip()
        email = self.gym_email_input.text().strip()
        password = self.gym_password_input.text()
        
        # Validación básica
        if not nombre or not username or not email or not password:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return
        
        success, error_msg = self.user_model.add_gym(nombre, username, email, password)
        
        if success:
            QMessageBox.information(self, "Éxito", f"Gimnasio '{nombre}' registrado correctamente.")
            self.clear_gym_form()
            self.load_gyms()
            
            # Notificar al dashboard para actualizar otras pestañas
            if hasattr(self.parent, 'update_licenses_tab'):
                self.parent.update_licenses_tab()
        else:
            QMessageBox.warning(self, "Error", error_msg)
        
    def update_gym(self):
        """Actualiza los datos de un gimnasio existente"""
        if not self.selected_gym_id:
            return
        
        nombre = self.gym_name_input.text().strip()
        username = self.gym_username_input.text().strip()
        email = self.gym_email_input.text().strip()
        password = self.gym_password_input.text()
        
        # Validación básica
        if not nombre or not username or not email:
            QMessageBox.warning(self, "Error", "Los campos Nombre, Usuario y Email son obligatorios.")
            return
        
        success, error_msg = self.user_model.update_gym(self.selected_gym_id, nombre, username, email, password)
        
        if success:
            QMessageBox.information(self, "Éxito", f"Gimnasio '{nombre}' actualizado correctamente.")
            self.clear_gym_form()
            self.load_gyms()
        else:
            QMessageBox.warning(self, "Error", error_msg)
    
    def toggle_gym_active(self):
        """Activa o desactiva un gimnasio"""
        if not self.selected_gym_id:
            return
        
        # Obtener estado actual
        row = None
        for r in range(self.gyms_table.rowCount()):
            if int(self.gyms_table.item(r, 0).text()) == self.selected_gym_id:
                row = r
                break
        
        if row is None:
            return
        
        current_state = self.gyms_table.item(row, 5).text()
        nombre_gimnasio = self.gyms_table.item(row, 1).text()
        action = "desactivar" if current_state == "Activo" else "activar"
        
        reply = QMessageBox.question(self, "Confirmar", 
                                    f"¿Está seguro que desea {action} el gimnasio '{nombre_gimnasio}'?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            self.user_model.toggle_gym_active(self.selected_gym_id)
            QMessageBox.information(self, "Éxito", f"Gimnasio '{nombre_gimnasio}' {action}do correctamente.")
            self.clear_gym_form()
            self.load_gyms()
            
            # Si se activó un gimnasio, actualizar la lista de licencias
            if current_state == "Inactivo" and hasattr(self.parent, 'update_licenses_tab'):
                self.parent.update_licenses_tab()