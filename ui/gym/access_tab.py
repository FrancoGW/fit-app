from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, 
                           QLabel, QLineEdit, QPushButton, QFrame)
from PyQt6.QtCore import Qt

from config.constants import (INPUT_STYLE, BUTTON_STYLE, FRAME_STYLE)
from models.member import MemberModel

class AccessTab(QWidget):
    def __init__(self, gym_id):
        super().__init__()
        self.gym_id = gym_id
        self.member_model = MemberModel()
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la pestaña de control de acceso"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Título
        title_label = QLabel("CONTROL DE ACCESO")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; margin: 20px;")
        layout.addWidget(title_label)
        
        # Entrada de DNI
        form_layout = QFormLayout()
        self.dni_input = QLineEdit()
        self.dni_input.setPlaceholderText("Ingrese DNI...")
        self.dni_input.setStyleSheet(INPUT_STYLE)
        self.dni_input.setMaximumWidth(300)
        self.dni_input.returnPressed.connect(self.verify_member)
        
        form_layout.addRow("DNI:", self.dni_input)
        
        form_container = QWidget()
        form_container.setLayout(form_layout)
        form_container.setMaximumWidth(500)
        
        form_hlayout = QHBoxLayout()
        form_hlayout.addWidget(form_container)
        form_hlayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addLayout(form_hlayout)
        
        # Botón de verificar
        verify_button = QPushButton("Verificar")
        verify_button.setStyleSheet(BUTTON_STYLE)
        verify_button.clicked.connect(self.verify_member)
        verify_button.setMaximumWidth(500)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(verify_button)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addLayout(button_layout)
        
        # Resultado
        result_frame = QFrame()
        result_frame.setStyleSheet(FRAME_STYLE)
        result_frame.setFrameShape(QFrame.Shape.StyledPanel)
        result_frame.setFixedSize(400, 300)  # Establece el tamaño exacto (ancho x alto)
        result_layout = QVBoxLayout(result_frame)
        
        self.member_name_label = QLabel("")
        self.member_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.member_name_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        
        self.quota_status_label = QLabel("")
        self.quota_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.quota_status_label.setStyleSheet("font-size: 16px;")
        
        self.plan_desc_label = QLabel("")
        self.plan_desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.plan_desc_label.setStyleSheet("font-size: 14px; font-style: italic;")
        
        result_layout.addWidget(self.member_name_label)
        result_layout.addWidget(self.quota_status_label)
        result_layout.addWidget(self.plan_desc_label)
        
        result_container = QHBoxLayout()
        result_container.addWidget(result_frame)
        result_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addLayout(result_container)
        layout.addStretch()
        
    def verify_member(self):
        """Verifica el estado de un socio por su DNI"""
        dni = self.dni_input.text().strip()
        
        if not dni:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Error", "Debe ingresar un DNI.")
            return
        
        member = self.member_model.get_member_by_dni(dni, self.gym_id)
        
        if not member:
            self.member_name_label.setText("Socio no encontrado")
            self.quota_status_label.setText("")
            self.plan_desc_label.setText("")
            return
        
        member_id, nombre, apellido, fecha_vencimiento, estado_cuota, plan_nombre, plan_descripcion = member
        
        # Registrar asistencia
        self.member_model.register_attendance(member_id)
        
        # Mostrar nombre del socio y plan
        self.member_name_label.setText(f"{nombre} {apellido}")
        if plan_nombre:
            self.member_name_label.setText(f"{nombre} {apellido} - {plan_nombre}")
        
        if plan_descripcion:
            self.plan_desc_label.setText(f"{plan_descripcion}")
        else:
            self.plan_desc_label.setText("")
        
        # Verificar estado de cuota
        if estado_cuota == "No Pagada":
            self.quota_status_label.setText("Cuota no pagada")
            self.quota_status_label.setStyleSheet("font-size: 16px; color: #e74c3c; font-weight: bold;")
        else:
            # Verificar estado de membresía
            status, dias_restantes = self.member_model.check_membership_status(member_id, fecha_vencimiento)
            
            if status == "vencida":
                self.quota_status_label.setText("Cuota vencida")
                self.quota_status_label.setStyleSheet("font-size: 16px; color: #e74c3c; font-weight: bold;")
            elif status == "por_vencer":
                self.quota_status_label.setText(f"Vence en {dias_restantes} días")
                self.quota_status_label.setStyleSheet("font-size: 16px; color: #f39c12; font-weight: bold;")
            else:
                self.quota_status_label.setText("Cuota al día")
                self.quota_status_label.setStyleSheet("font-size: 16px; color: #2ecc71; font-weight: bold;")