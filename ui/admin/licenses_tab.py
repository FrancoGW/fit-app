from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, 
                           QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, 
                           QHeaderView, QFrame, QComboBox, QDateEdit, QMessageBox)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor

from config.constants import (TEXT_PRIMARY, FRAME_STYLE, INPUT_STYLE, BUTTON_STYLE, 
                            SECONDARY_BUTTON_STYLE, COMBOBOX_STYLE, TABLE_STYLE, 
                            SUCCESS_COLOR, DANGER_COLOR, DANGER_BUTTON_STYLE)
from models.license import LicenseModel

class LicensesTab(QWidget):
    def __init__(self):
        super().__init__()
        self.license_model = LicenseModel()
        self.selected_license_id = None
        self.selected_license_state = None
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz de usuario de la pestaña de licencias"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Título de la sección
        title_label = QLabel("Gestión de Licencias")
        title_label.setObjectName("sectionTitle")
        layout.addWidget(title_label)
        
        # Formulario para añadir/editar licencias
        form_frame = QFrame()
        form_frame.setStyleSheet(FRAME_STYLE)
        form_frame.setFrameShape(QFrame.Shape.StyledPanel)
        form_layout = QFormLayout(form_frame)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setSpacing(15)
        
        # Selector de gimnasio
        self.license_gym_combo = QComboBox()
        self.license_gym_combo.setStyleSheet(COMBOBOX_STYLE)
        self.update_gym_combo()
        
        # Tipo de licencia
        self.license_type_combo = QComboBox()
        self.license_type_combo.setStyleSheet(COMBOBOX_STYLE)
        self.license_type_combo.addItems(["Mensual", "Trimestral", "Semestral", "Anual"])
        
        # Fecha de inicio
        self.license_start_date = QDateEdit()
        self.license_start_date.setStyleSheet(INPUT_STYLE)
        self.license_start_date.setCalendarPopup(True)
        self.license_start_date.setDate(QDate.currentDate())
        
        # Precio
        self.license_price_input = QLineEdit()
        self.license_price_input.setStyleSheet(INPUT_STYLE)
        self.license_price_input.setPlaceholderText("Ej: 5000.00")
        
        form_layout.addRow("Gimnasio:", self.license_gym_combo)
        form_layout.addRow("Tipo de Licencia:", self.license_type_combo)
        form_layout.addRow("Fecha de Inicio:", self.license_start_date)
        form_layout.addRow("Precio:", self.license_price_input)
        
        layout.addWidget(form_frame)
        
        # Botones para gestionar licencias
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.add_license_button = QPushButton("Añadir Licencia")
        self.add_license_button.setStyleSheet(BUTTON_STYLE)
        self.add_license_button.clicked.connect(self.add_license)
        
        self.revoke_license_button = QPushButton("Revocar Licencia")
        self.revoke_license_button.setStyleSheet(DANGER_BUTTON_STYLE)
        self.revoke_license_button.clicked.connect(self.revoke_license)
        self.revoke_license_button.setEnabled(False)
        
        self.clear_license_button = QPushButton("Limpiar")
        self.clear_license_button.setStyleSheet(SECONDARY_BUTTON_STYLE)
        self.clear_license_button.clicked.connect(self.clear_license_form)
        
        button_layout.addWidget(self.add_license_button)
        button_layout.addWidget(self.revoke_license_button)
        button_layout.addWidget(self.clear_license_button)
        
        layout.addLayout(button_layout)
        
        # Tabla de licencias
        self.licenses_table = QTableWidget()
        self.licenses_table.setStyleSheet(TABLE_STYLE)
        self.licenses_table.setColumnCount(7)
        self.licenses_table.setHorizontalHeaderLabels([
            "ID", "Gimnasio", "Tipo", "Fecha Inicio", "Fecha Vencimiento", "Precio", "Estado"
        ])
        self.licenses_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.licenses_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.licenses_table.cellClicked.connect(self.select_license)
        self.licenses_table.setAlternatingRowColors(True)
        
        layout.addWidget(self.licenses_table)
        
        # Cargar datos en la tabla
        self.load_licenses()
    
    def update_gym_combo(self):
        """Actualiza el combo box de gimnasios"""
        self.license_gym_combo.clear()
        
        gyms = self.license_model.get_active_gyms()
        
        for gym_id, gym_name in gyms:
            self.license_gym_combo.addItem(gym_name, gym_id)
    
    def load_licenses(self):
        """Carga la lista de licencias en la tabla"""
        licenses = self.license_model.get_all_licenses()
        
        self.licenses_table.setRowCount(0)  # Limpiar tabla
        
        for row_idx, license in enumerate(licenses):
            self.licenses_table.insertRow(row_idx)
            
            for col_idx, value in enumerate(license):
                # Formatear precio
                if col_idx == 5:
                    value = f"${value:.2f}"
                
                # Formatear estado
                if col_idx == 6:
                    value = "Activa" if value == 1 else "Revocada"
                
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                
                # Colorear según el estado
                if col_idx == 6:
                    if value == "Activa":
                        item.setForeground(QColor(SUCCESS_COLOR))
                    else:
                        item.setForeground(QColor(DANGER_COLOR))
                
                self.licenses_table.setItem(row_idx, col_idx, item)
    
    def clear_license_form(self):
        """Limpia el formulario de licencias"""
        if self.license_gym_combo.count() > 0:
            self.license_gym_combo.setCurrentIndex(0)
        
        self.license_type_combo.setCurrentIndex(0)
        self.license_start_date.setDate(QDate.currentDate())
        self.license_price_input.clear()
        
        self.add_license_button.setEnabled(True)
        self.revoke_license_button.setEnabled(False)
        
        # Limpiar selección de la tabla
        self.licenses_table.clearSelection()
        self.selected_license_id = None
        self.selected_license_state = None
    
    def select_license(self, row, column):
        """Selecciona una licencia de la tabla"""
        self.selected_license_id = int(self.licenses_table.item(row, 0).text())
        self.selected_license_state = self.licenses_table.item(row, 6).text()
        
        # Activar botones según estado
        self.add_license_button.setEnabled(True)
        self.revoke_license_button.setEnabled(self.selected_license_state == "Activa")
    
    def add_license(self):
        """Añade una nueva licencia a un gimnasio"""
        # Obtener datos del formulario
        if self.license_gym_combo.count() == 0:
            QMessageBox.warning(self, "Error", "No hay gimnasios activos disponibles.")
            return
        
        gym_id = self.license_gym_combo.currentData()
        license_type = self.license_type_combo.currentText()
        start_date = self.license_start_date.date().toString("yyyy-MM-dd")
        
        # Verificar precio
        price_text = self.license_price_input.text().strip()
        if not price_text:
            QMessageBox.warning(self, "Error", "Debe ingresar un precio.")
            return
        
        try:
            price = float(price_text)
            if price <= 0:
                QMessageBox.warning(self, "Error", "El precio debe ser mayor que cero.")
                return
        except ValueError:
            QMessageBox.warning(self, "Error", "El precio debe ser un número válido.")
            return
        
        try:
            # Añadir licencia
            self.license_model.add_license(gym_id, license_type, start_date, price)
            
            gym_name = self.license_gym_combo.currentText()
            QMessageBox.information(self, "Éxito", f"Licencia {license_type} añadida al gimnasio '{gym_name}' correctamente.")
            
            self.clear_license_form()
            self.load_licenses()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al añadir licencia: {str(e)}")
    
    def revoke_license(self):
        """Revoca una licencia activa"""
        if not self.selected_license_id or self.selected_license_state != "Activa":
            return
        
        row = None
        for r in range(self.licenses_table.rowCount()):
            if int(self.licenses_table.item(r, 0).text()) == self.selected_license_id:
                row = r
                break
        
        if row is None:
            return
        
        gym_name = self.licenses_table.item(row, 1).text()
        license_type = self.licenses_table.item(row, 2).text()
        
        reply = QMessageBox.question(self, "Confirmar", 
                                   f"¿Está seguro que desea revocar la licencia {license_type} del gimnasio '{gym_name}'?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            self.license_model.revoke_license(self.selected_license_id)
            QMessageBox.information(self, "Éxito", f"Licencia revocada correctamente.")
            self.clear_license_form()
            self.load_licenses()