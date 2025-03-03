from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, 
                           QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, 
                           QHeaderView, QFrame, QMessageBox)
from PyQt6.QtCore import Qt

from config.constants import (FRAME_STYLE, INPUT_STYLE, BUTTON_STYLE, 
                            SECONDARY_BUTTON_STYLE, TABLE_STYLE)
from models.plan import PlanModel

class PlansTab(QWidget):
    def __init__(self, gym_id):
        super().__init__()
        self.gym_id = gym_id
        self.plan_model = PlanModel()
        self.selected_plan_id = None
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la pestaña de gestión de planes"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Formulario para crear/editar planes
        form_frame = QFrame()
        form_frame.setFrameShape(QFrame.Shape.StyledPanel)
        form_frame.setStyleSheet(FRAME_STYLE)
        form_layout = QFormLayout(form_frame)
        
        self.plan_nombre_input = QLineEdit()
        self.plan_nombre_input.setStyleSheet(INPUT_STYLE)
        
        self.plan_descripcion_input = QLineEdit()
        self.plan_descripcion_input.setStyleSheet(INPUT_STYLE)
        
        self.plan_precio_input = QLineEdit()
        self.plan_precio_input.setStyleSheet(INPUT_STYLE)
        self.plan_precio_input.setPlaceholderText("Ej: 5000.00")
        
        form_layout.addRow("Nombre:", self.plan_nombre_input)
        form_layout.addRow("Descripción:", self.plan_descripcion_input)
        form_layout.addRow("Precio:", self.plan_precio_input)
        
        layout.addWidget(form_frame)
        
        button_layout = QHBoxLayout()
        
        self.add_plan_button = QPushButton("Agregar Plan")
        self.add_plan_button.setStyleSheet(BUTTON_STYLE)
        self.add_plan_button.clicked.connect(self.add_plan)
        
        self.update_plan_button = QPushButton("Actualizar Plan")
        self.update_plan_button.setStyleSheet(SECONDARY_BUTTON_STYLE)
        self.update_plan_button.clicked.connect(self.update_plan)
        self.update_plan_button.setEnabled(False)
        
        self.delete_plan_button = QPushButton("Eliminar Plan")
        self.delete_plan_button.setStyleSheet(SECONDARY_BUTTON_STYLE)
        self.delete_plan_button.clicked.connect(self.delete_plan)
        self.delete_plan_button.setEnabled(False)
        
        self.clear_plan_button = QPushButton("Limpiar")
        self.clear_plan_button.setStyleSheet(SECONDARY_BUTTON_STYLE)
        self.clear_plan_button.clicked.connect(self.clear_plan_form)
        
        button_layout.addWidget(self.add_plan_button)
        button_layout.addWidget(self.update_plan_button)
        button_layout.addWidget(self.delete_plan_button)
        button_layout.addWidget(self.clear_plan_button)
        
        layout.addLayout(button_layout)
        
        # Tabla de planes
        self.plans_table = QTableWidget()
        self.plans_table.setStyleSheet(TABLE_STYLE)
        self.plans_table.setColumnCount(4)
        self.plans_table.setHorizontalHeaderLabels(["ID", "Nombre", "Descripción", "Precio"])
        self.plans_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.plans_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.plans_table.cellClicked.connect(self.select_plan)
        self.plans_table.setAlternatingRowColors(True)
        
        layout.addWidget(self.plans_table)
        
        # Cargar datos en la tabla
        self.load_plans()
    
    def clear_plan_form(self):
        """Limpia el formulario de planes"""
        self.plan_nombre_input.clear()
        self.plan_descripcion_input.clear()
        self.plan_precio_input.clear()
        
        self.add_plan_button.setEnabled(True)
        self.update_plan_button.setEnabled(False)
        self.delete_plan_button.setEnabled(False)
        
        # Limpiar selección de la tabla
        self.plans_table.clearSelection()
        self.selected_plan_id = None
    
    def load_plans(self):
        """Carga la lista de planes en la tabla"""
        planes = self.plan_model.get_all_plans()
        
        self.plans_table.setRowCount(0)  # Limpiar tabla
        
        for row_idx, plan in enumerate(planes):
            self.plans_table.insertRow(row_idx)
            
            for col_idx, value in enumerate(plan):
                if col_idx == 3:  # Formatear el precio
                    value = f"${value:.2f}"
                
                item = QTableWidgetItem(str(value))
                # Hacer las celdas no editables
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.plans_table.setItem(row_idx, col_idx, item)
    
    def select_plan(self, row, column):
        """Selecciona un plan de la tabla para editar"""
        self.selected_plan_id = int(self.plans_table.item(row, 0).text())
        
        # Cargar datos en el formulario
        self.plan_nombre_input.setText(self.plans_table.item(row, 1).text())
        self.plan_descripcion_input.setText(self.plans_table.item(row, 2).text())
        
        # Obtener precio sin el símbolo $
        precio_text = self.plans_table.item(row, 3).text().replace('$', '')
        self.plan_precio_input.setText(precio_text)
        
        # Activar botones
        self.add_plan_button.setEnabled(False)
        self.update_plan_button.setEnabled(True)
        self.delete_plan_button.setEnabled(True)
    
    def add_plan(self):
        """Agrega un nuevo plan a la base de datos"""
        nombre = self.plan_nombre_input.text().strip()
        descripcion = self.plan_descripcion_input.text().strip()
        precio_text = self.plan_precio_input.text().strip()
        
        # Validación básica
        if not nombre:
            QMessageBox.warning(self, "Error", "El nombre del plan es obligatorio.")
            return
        
        try:
            precio = float(precio_text)
            if precio <= 0:
                QMessageBox.warning(self, "Error", "El precio debe ser mayor que cero.")
                return
        except ValueError:
            QMessageBox.warning(self, "Error", "El precio debe ser un número válido.")
            return
        
        success, error_msg = self.plan_model.add_plan(nombre, descripcion, precio)
        
        if success:
            QMessageBox.information(self, "Éxito", "Plan registrado correctamente.")
            self.clear_plan_form()
            self.load_plans()
        else:
            QMessageBox.warning(self, "Error", error_msg)
    
    def update_plan(self):
        """Actualiza los datos de un plan existente"""
        if not self.selected_plan_id:
            return
        
        nombre = self.plan_nombre_input.text().strip()
        descripcion = self.plan_descripcion_input.text().strip()
        precio_text = self.plan_precio_input.text().strip()
        
        # Validación básica
        if not nombre:
            QMessageBox.warning(self, "Error", "El nombre del plan es obligatorio.")
            return
        
        try:
            precio = float(precio_text)
            if precio <= 0:
                QMessageBox.warning(self, "Error", "El precio debe ser mayor que cero.")
                return
        except ValueError:
            QMessageBox.warning(self, "Error", "El precio debe ser un número válido.")
            return
        
        success, error_msg = self.plan_model.update_plan(self.selected_plan_id, nombre, descripcion, precio)
        
        if success:
            QMessageBox.information(self, "Éxito", "Plan actualizado correctamente.")
            self.clear_plan_form()
            self.load_plans()
        else:
            QMessageBox.warning(self, "Error", error_msg)

    def delete_plan(self):
        """Elimina un plan de la base de datos"""
        if not self.selected_plan_id:
            return
        
        success, error_msg = self.plan_model.delete_plan(self.selected_plan_id, self.gym_id)
        
        if not success:
            QMessageBox.warning(self, "Error", error_msg)
            return
        
        reply = QMessageBox.question(self, "Confirmar", 
                                    "¿Está seguro que desea eliminar este plan? Esta acción no se puede deshacer.",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            QMessageBox.information(self, "Éxito", "Plan eliminado correctamente.")
            self.clear_plan_form()
            self.load_plans()