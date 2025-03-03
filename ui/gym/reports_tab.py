from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                    QLabel, QPushButton, QFrame, QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt
import csv

from config.constants import (FRAME_STYLE, BUTTON_STYLE)
from models.member import MemberModel

class ReportsTab(QWidget):
    def __init__(self, gym_id):
        super().__init__()
        self.gym_id = gym_id
        self.member_model = MemberModel()
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la pestaña de informes"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Título
        title_label = QLabel("INFORMES Y ESTADÍSTICAS")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; margin: 20px;")
        layout.addWidget(title_label)
        
        # Panel de estadísticas
        stats_frame = QFrame()
        stats_frame.setFrameShape(QFrame.Shape.StyledPanel)
        stats_frame.setStyleSheet(FRAME_STYLE)
        stats_layout = QVBoxLayout(stats_frame)
        
        stats_title = QLabel("Estadísticas del Gimnasio")
        stats_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        stats_layout.addWidget(stats_title)
        
        # Grid de estadísticas
        stats_grid = QGridLayout()
        
        # Obtener estadísticas
        member_stats = self.member_model.get_member_status_stats(self.gym_id)
        attendance_count = self.member_model.get_attendance_stats(self.gym_id)
        
        # Agregar al grid
        stats_grid.addWidget(QLabel("Total de Socios:"), 0, 0)
        stats_grid.addWidget(QLabel(str(member_stats["total"])), 0, 1)
        
        stats_grid.addWidget(QLabel("Socios con Cuota al Día:"), 1, 0)
        stats_grid.addWidget(QLabel(f"{member_stats['active']} ({member_stats['percent_active']:.1f}%)"), 1, 1)
        
        stats_grid.addWidget(QLabel("Asistencias este Mes:"), 2, 0)
        stats_grid.addWidget(QLabel(str(attendance_count)), 2, 1)
        
        stats_layout.addLayout(stats_grid)
        
        layout.addWidget(stats_frame)
        
        # Panel de exportación de informes
        export_frame = QFrame()
        export_frame.setFrameShape(QFrame.Shape.StyledPanel)
        export_frame.setStyleSheet(FRAME_STYLE)
        export_layout = QVBoxLayout(export_frame)
        
        export_title = QLabel("Exportar Informes")
        export_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        export_layout.addWidget(export_title)
        
        # Botones de exportación
        members_button = QPushButton("Exportar Lista de Socios")
        members_button.setStyleSheet(BUTTON_STYLE)
        members_button.clicked.connect(self.export_members_report)
        
        attendance_button = QPushButton("Exportar Informe de Asistencias")
        attendance_button.setStyleSheet(BUTTON_STYLE)
        attendance_button.clicked.connect(self.export_attendance_report)
        
        payments_button = QPushButton("Exportar Informe de Pagos")
        payments_button.setStyleSheet(BUTTON_STYLE)
        payments_button.clicked.connect(self.export_payments_report)
        
        export_layout.addWidget(members_button)
        export_layout.addWidget(attendance_button)
        export_layout.addWidget(payments_button)
        
        layout.addWidget(export_frame)
        
        layout.addStretch()
    
    def export_members_report(self):
        """Exporta un informe de socios a un archivo CSV"""
        file_path, _ = QFileDialog.getSaveFileName(self, "Guardar Informe de Socios", "", "CSV Files (*.csv)")
        
        if not file_path:
            return
        
        try:
            members = self.member_model.export_members_report(self.gym_id)
            
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                # Escribir encabezados
                writer.writerow(["ID", "Nombre", "Apellido", "DNI", "Teléfono", "Fecha Registro", 
                                "Fecha Vencimiento", "Estado Cuota", "Plan"])
                # Escribir datos
                for member in members:
                    writer.writerow(member)
            
            QMessageBox.information(self, "Exportación Exitosa", f"Informe de socios exportado a {file_path}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al exportar informe: {str(e)}")
    
    def export_attendance_report(self):
        """Exporta un informe de asistencias a un archivo CSV"""
        file_path, _ = QFileDialog.getSaveFileName(self, "Guardar Informe de Asistencias", "", "CSV Files (*.csv)")
        
        if not file_path:
            return
        
        try:
            attendances = self.member_model.export_attendance_report(self.gym_id)
            
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                # Escribir encabezados
                writer.writerow(["Fecha", "Nombre", "Apellido", "DNI"])
                # Escribir datos
                for attendance in attendances:
                    writer.writerow(attendance)
            
            QMessageBox.information(self, "Exportación Exitosa", f"Informe de asistencias exportado a {file_path}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al exportar informe: {str(e)}")
    
    def export_payments_report(self):
        """Exporta un informe de pagos a un archivo CSV (pendiente para implementación futura)"""
        QMessageBox.information(self, "Funcionalidad no implementada", 
                             "Esta funcionalidad se implementará en futuras versiones.")