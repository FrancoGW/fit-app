from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                           QLabel, QPushButton, QFrame, QFileDialog)
from PyQt6.QtCore import Qt
import csv

from config.constants import (FRAME_STYLE, BUTTON_STYLE)
from models.license import LicenseModel

class StatsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.license_model = LicenseModel()
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la pestaña de estadísticas"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Título de la sección
        title_label = QLabel("Estadísticas del Sistema")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title_label)
        
        # Panel de estadísticas generales
        stats_frame = QFrame()
        stats_frame.setFrameShape(QFrame.Shape.StyledPanel)
        stats_frame.setStyleSheet(FRAME_STYLE)
        stats_layout = QGridLayout(stats_frame)
        
        # Obtener estadísticas
        license_stats = self.license_model.get_license_stats()
        
        # Agregar datos al grid
        stats_layout.addWidget(QLabel("Total de Gimnasios:"), 0, 0)
        stats_layout.addWidget(QLabel(str(license_stats["total_gyms"])), 0, 1)
        
        stats_layout.addWidget(QLabel("Gimnasios Activos:"), 1, 0)
        stats_layout.addWidget(QLabel(f"{license_stats['active_gyms']} ({license_stats['percent_active']:.1f}% del total)"), 1, 1)
        
        stats_layout.addWidget(QLabel("Licencias Activas:"), 2, 0)
        stats_layout.addWidget(QLabel(str(license_stats["active_licenses"])), 2, 1)
        
        stats_layout.addWidget(QLabel("Ingresos Totales:"), 3, 0)
        stats_layout.addWidget(QLabel(f"${license_stats['total_revenue']:.2f}"), 3, 1)
        
        layout.addWidget(stats_frame)
        
        # Botones para exportar informes
        reports_frame = QFrame()
        reports_frame.setFrameShape(QFrame.Shape.StyledPanel)
        reports_frame.setStyleSheet(FRAME_STYLE)
        reports_layout = QVBoxLayout(reports_frame)
        
        export_title = QLabel("Exportar Informes")
        export_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        reports_layout.addWidget(export_title)
        
        export_gyms_button = QPushButton("Exportar Lista de Gimnasios")
        export_gyms_button.setStyleSheet(BUTTON_STYLE)
        export_gyms_button.clicked.connect(self.export_gyms_report)
        
        export_licenses_button = QPushButton("Exportar Informe de Licencias")
        export_licenses_button.setStyleSheet(BUTTON_STYLE)
        export_licenses_button.clicked.connect(self.export_licenses_report)
        
        reports_layout.addWidget(export_gyms_button)
        reports_layout.addWidget(export_licenses_button)
        
        layout.addWidget(reports_frame)
        layout.addStretch()
    
    def export_gyms_report(self):
        """Exporta un informe de gimnasios a CSV"""
        file_path, _ = QFileDialog.getSaveFileName(self, "Guardar Informe de Gimnasios", "", "CSV Files (*.csv)")
        
        if not file_path:
            return
        
        try:
            # Obtener datos de gimnasios
            gyms = self.license_model.conn.cursor().execute("""
                SELECT id, nombre_gimnasio, username, email, fecha_registro, 
                       ultimo_acceso, activo
                FROM usuarios
                WHERE tipo = 'gimnasio'
                ORDER BY nombre_gimnasio
            """).fetchall()
            
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                # Escribir encabezados
                writer.writerow(["ID", "Nombre", "Usuario", "Email", "Fecha Registro", 
                               "Último Acceso", "Estado"])
                
                # Escribir datos
                for gym in gyms:
                    # Formatear estado
                    row = list(gym)
                    row[6] = "Activo" if row[6] == 1 else "Inactivo"
                    writer.writerow(row)
            
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.information(self, "Exportación Exitosa", f"Informe exportado a {file_path}")
            
        except Exception as e:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Error", f"Error al exportar informe: {str(e)}")
    
    def export_licenses_report(self):
        """Exporta un informe de licencias a CSV"""
        file_path, _ = QFileDialog.getSaveFileName(self, "Guardar Informe de Licencias", "", "CSV Files (*.csv)")
        
        if not file_path:
            return
        
        try:
            # Obtener datos de licencias
            licenses = self.license_model.conn.cursor().execute("""
                SELECT l.id, u.nombre_gimnasio, l.tipo, l.fecha_inicio, 
                       l.fecha_vencimiento, l.precio, l.activa
                FROM licencias l
                JOIN usuarios u ON l.usuario_id = u.id
                ORDER BY l.fecha_vencimiento DESC
            """).fetchall()
            
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                # Escribir encabezados
                writer.writerow(["ID", "Gimnasio", "Tipo", "Fecha Inicio", 
                               "Fecha Vencimiento", "Precio", "Estado"])
                
                # Escribir datos
                for license in licenses:
                    # Formatear estado
                    row = list(license)
                    row[6] = "Activa" if row[6] == 1 else "Revocada"
                    writer.writerow(row)
            
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.information(self, "Exportación Exitosa", f"Informe exportado a {file_path}")
            
        except Exception as e:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Error", f"Error al exportar informe: {str(e)}")