from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, 
                           QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, 
                           QHeaderView, QFrame, QComboBox, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from config.constants import (TEXT_PRIMARY, FRAME_STYLE, INPUT_STYLE, BUTTON_STYLE, 
                            SECONDARY_BUTTON_STYLE, COMBOBOX_STYLE, TABLE_STYLE)
from models.member import MemberModel
from models.plan import PlanModel

class MembersTab(QWidget):
    def __init__(self, gym_id):
        super().__init__()
        self.gym_id = gym_id
        self.member_model = MemberModel()
        self.plan_model = PlanModel()
        self.selected_member_id = None
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la pestaña de gestión de socios"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 40, 20, 40)
        
        # Formulario de registro/edición
        form_frame = QFrame()
        form_frame.setFrameShape(QFrame.Shape.StyledPanel)
        form_frame.setStyleSheet(FRAME_STYLE)
        form_layout = QFormLayout(form_frame)
        
        self.nombre_input = QLineEdit()
        self.nombre_input.setStyleSheet(INPUT_STYLE)
        
        self.apellido_input = QLineEdit()
        self.apellido_input.setStyleSheet(INPUT_STYLE)
        
        self.member_dni_input = QLineEdit()
        self.member_dni_input.setStyleSheet(INPUT_STYLE)
        
        self.telefono_input = QLineEdit()
        self.telefono_input.setStyleSheet(INPUT_STYLE)
        
        # Selector de planes
        self.plan_combo = QComboBox()
        self.plan_combo.setStyleSheet(COMBOBOX_STYLE)
        # Aumentar el ancho mínimo del combo box
        self.plan_combo.setMinimumWidth(300)
        # Aumentar la altura
        self.plan_combo.setMinimumHeight(30)
        
        # Selector de estado de cuota
        self.estado_cuota = QComboBox()
        self.estado_cuota.setStyleSheet(COMBOBOX_STYLE)
        self.estado_cuota.setMinimumWidth(300)
        self.estado_cuota.setMinimumHeight(30)
        self.estado_cuota.addItems(["Pagada", "No Pagada"])
        
        # Actualizar lista de planes
        self.update_plan_combo()
        
        form_layout.addRow("Nombre:", self.nombre_input)
        form_layout.addRow("Apellido:", self.apellido_input)
        form_layout.addRow("DNI:", self.member_dni_input)
        form_layout.addRow("Teléfono:", self.telefono_input)
        form_layout.addRow("Plan:", self.plan_combo)
        form_layout.addRow("Estado Cuota:", self.estado_cuota)
        
        layout.addWidget(form_frame)
        
        button_layout = QHBoxLayout()
        
        self.add_button = QPushButton("Registrar Socio")
        self.add_button.setStyleSheet(BUTTON_STYLE)
        self.add_button.clicked.connect(self.add_member)
        
        self.update_button = QPushButton("Actualizar Socio")
        self.update_button.setStyleSheet(SECONDARY_BUTTON_STYLE)
        self.update_button.clicked.connect(self.update_member)
        self.update_button.setEnabled(False)
        
        self.delete_button = QPushButton("Eliminar Socio")
        self.delete_button.setStyleSheet(SECONDARY_BUTTON_STYLE)
        self.delete_button.clicked.connect(self.delete_member)
        self.delete_button.setEnabled(False)
        
        self.clear_button = QPushButton("Limpiar")
        self.clear_button.setStyleSheet(SECONDARY_BUTTON_STYLE)
        self.clear_button.clicked.connect(self.clear_form)
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.clear_button)
        
        layout.addLayout(button_layout)
        
        # Tabla de socios
        self.members_table = QTableWidget()
        self.members_table.setStyleSheet(TABLE_STYLE)
        self.members_table.setColumnCount(8)
        self.members_table.setHorizontalHeaderLabels([
            "ID", "Nombre", "Apellido", "DNI", "Teléfono", "Fecha Vencimiento", "Estado Cuota", "Plan"
        ])
        self.members_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.members_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.members_table.cellClicked.connect(self.select_member)
        self.members_table.setAlternatingRowColors(True)
        
        layout.addWidget(self.members_table)
        
        # Cargar datos en la tabla
        self.load_members()
    
    def update_plan_combo(self):
        """Actualiza el combo box de planes"""
        self.plan_combo.clear()
        plans = self.plan_model.get_all_plan_names()
        self.plan_combo.addItems(plans)
    
    def clear_form(self):
        """Limpia el formulario de socios"""
        self.nombre_input.clear()
        self.apellido_input.clear()
        self.member_dni_input.clear()
        self.telefono_input.clear()
        self.estado_cuota.setCurrentIndex(0)
        if self.plan_combo.count() > 0:
            self.plan_combo.setCurrentIndex(0)
        
        self.add_button.setEnabled(True)
        self.update_button.setEnabled(False)
        self.delete_button.setEnabled(False)
        
        # Limpiar selección de la tabla
        self.members_table.clearSelection()
        self.selected_member_id = None
    
    def load_members(self):
        """Carga la lista de socios en la tabla"""
        members = self.member_model.get_all_members(self.gym_id)
        
        self.members_table.setRowCount(0)  # Limpiar tabla
        
        for row_idx, member in enumerate(members):
            self.members_table.insertRow(row_idx)
            
            for col_idx, value in enumerate(member):
                item = QTableWidgetItem(str(value))
                # Aplicar color según el estado de la cuota
                if col_idx == 6:  # Columna de estado de cuota
                    if value == "Pagada":
                        item.setForeground(QColor("#2ecc71"))  # Verde para pagada
                    else:
                        item.setForeground(QColor("#e74c3c"))  # Rojo para no pagada
                
                # Hacer las celdas no editables
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.members_table.setItem(row_idx, col_idx, item)
    
    def select_member(self, row, column):
        """Selecciona un socio de la tabla para editar"""
        self.selected_member_id = int(self.members_table.item(row, 0).text())
        
        # Cargar datos en el formulario
        self.nombre_input.setText(self.members_table.item(row, 1).text())
        self.apellido_input.setText(self.members_table.item(row, 2).text())
        self.member_dni_input.setText(self.members_table.item(row, 3).text())
        self.telefono_input.setText(self.members_table.item(row, 4).text())
        
        # Seleccionar el plan
        plan_nombre = self.members_table.item(row, 7).text()
        for i in range(self.plan_combo.count()):
            if self.plan_combo.itemText(i) == plan_nombre:
                self.plan_combo.setCurrentIndex(i)
                break
        
        estado = self.members_table.item(row, 6).text()
        index = 0 if estado == "Pagada" else 1
        self.estado_cuota.setCurrentIndex(index)
        
        # Activar botones
        self.add_button.setEnabled(False)
        self.update_button.setEnabled(True)
        self.delete_button.setEnabled(True)
    
    def add_member(self):
        """Agrega un nuevo socio a la base de datos"""
        nombre = self.nombre_input.text().strip()
        apellido = self.apellido_input.text().strip()
        dni = self.member_dni_input.text().strip()
        telefono = self.telefono_input.text().strip()
        estado_cuota = self.estado_cuota.currentText()
        
        # Obtener el ID del plan seleccionado
        plan_nombre = self.plan_combo.currentText()
        plan_id = self.plan_model.get_plan_by_name(plan_nombre)[0]
        
        # Validación básica
        if not nombre or not apellido or not dni:
            QMessageBox.warning(self, "Error", "Los campos Nombre, Apellido y DNI son obligatorios.")
            return
        
        success, error_msg = self.member_model.add_member(nombre, apellido, dni, telefono, plan_id, estado_cuota, self.gym_id)
        
        if success:
            QMessageBox.information(self, "Éxito", "Socio registrado correctamente.")
            self.clear_form()
            self.load_members()
        else:
            QMessageBox.warning(self, "Error", error_msg)
    
    def update_member(self):
        """Actualiza los datos de un socio existente"""
        if not self.selected_member_id:
            return
        
        nombre = self.nombre_input.text().strip()
        apellido = self.apellido_input.text().strip()
        dni = self.member_dni_input.text().strip()
        telefono = self.telefono_input.text().strip()
        estado_cuota = self.estado_cuota.currentText()
        
        # Obtener el ID del plan seleccionado
        plan_nombre = self.plan_combo.currentText()
        plan_id = self.plan_model.get_plan_by_name(plan_nombre)[0]
        
        # Validación básica
        if not nombre or not apellido or not dni:
            QMessageBox.warning(self, "Error", "Los campos Nombre, Apellido y DNI son obligatorios.")
            return
        
        success, error_msg = self.member_model.update_member(self.selected_member_id, nombre, apellido, dni, telefono, plan_id, estado_cuota)
        
        if success:
            QMessageBox.information(self, "Éxito", "Socio actualizado correctamente.")
            self.clear_form()
            self.load_members()
        else:
            QMessageBox.warning(self, "Error", error_msg)
    
    def delete_member(self):
        """Elimina un socio de la base de datos"""
        if not self.selected_member_id:
            return
        
        reply = QMessageBox.question(self, "Confirmar", 
                                    "¿Está seguro que desea eliminar este socio? Esta acción no se puede deshacer.",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            self.member_model.delete_member(self.selected_member_id)
            QMessageBox.information(self, "Éxito", "Socio eliminado correctamente.")
            self.clear_form()
            self.load_members()