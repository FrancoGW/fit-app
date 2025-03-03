from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QLabel, QPushButton, QListWidget, QListWidgetItem, 
                           QStackedWidget, QMessageBox)
from PyQt6.QtCore import Qt, QSize

from config.constants import (BG_COLOR, TEXT_PRIMARY, TEXT_SECONDARY, 
                            SIDEBAR_BG, BORDER_COLOR, PRIMARY_COLOR,
                            CARD_COLOR, SECONDARY_BUTTON_STYLE, SIDEBAR_STYLE,
                            WARNING_COLOR, SUCCESS_COLOR)
from ui.gym.access_tab import AccessTab
from ui.gym.members_tab import MembersTab
from ui.gym.plans_tab import PlansTab
from ui.gym.reports_tab import ReportsTab
from models.license import LicenseModel
from config.database import init_gym_database

class GymApp(QMainWindow):
    """Aplicación principal para los gimnasios"""
    def __init__(self, user_id, user_type, gym_name):
        super().__init__()
        self.user_id = user_id
        self.user_type = user_type
        self.gym_name = gym_name
        
        # Configurar la ventana principal
        self.setWindowTitle(f"FIT APP - {gym_name}")
        self.setGeometry(100, 100, 1200, 700)
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {BG_COLOR};
                color: {TEXT_PRIMARY};
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
            QLabel {{
                color: {TEXT_PRIMARY};
            }}
            QLabel#pageTitle {{
                font-size: 22px;
                font-weight: bold;
                color: {TEXT_PRIMARY};
            }}
            QLabel#sectionTitle {{
                font-size: 18px;
                font-weight: bold;
                color: {TEXT_PRIMARY};
            }}
            QLabel#statsLabel {{
                font-size: 24px;
                font-weight: bold;
                color: {PRIMARY_COLOR};
            }}
            QLabel#statsDescription {{
                color: {TEXT_SECONDARY};
                font-size: 14px;
            }}
        """)
        
        init_gym_database()
        self.license_model = LicenseModel()
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz de usuario principal"""
        # Widget central y layout principal
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Panel izquierdo (menú lateral)
        left_panel = QWidget()
        left_panel.setFixedWidth(250)
        left_panel.setStyleSheet(f"background-color: {SIDEBAR_BG};")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)
        
        # Logo en la parte superior del panel izquierdo
        logo_container = QWidget()
        logo_container.setFixedHeight(100)
        logo_container.setStyleSheet(f"background-color: {SIDEBAR_BG}; border-bottom: 1px solid {BORDER_COLOR};")
        logo_layout = QHBoxLayout(logo_container)
        
        # Logo
        logo_label = QLabel("FIT APP")
        logo_label.setStyleSheet("color: white; font-size: 22px; font-weight: bold;")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addWidget(logo_label)
        
        left_layout.addWidget(logo_container)
        
        # Menú de navegación
        self.menu_list = QListWidget()
        self.menu_list.setIconSize(QSize(24, 24))
        self.menu_list.setSpacing(5)
        self.menu_list.setStyleSheet(SIDEBAR_STYLE)
        
        # Agregar opciones de menú para gimnasios
        menu_items = [
            ("Control de Acceso", "access_tab"),
            ("Gestión de Socios", "members_tab"),
            ("Gestión de Planes", "plans_tab"),
            ("Informes", "reports_tab")
        ]
        
        for text, page_name in menu_items:
            item = QListWidgetItem(text)
            item.setData(Qt.ItemDataRole.UserRole, page_name)
            self.menu_list.addItem(item)
        
        left_layout.addWidget(self.menu_list)
        
        # Widget para mostrar información en la parte inferior del menú
        info_widget = QWidget()
        info_widget.setFixedHeight(100)
        info_widget.setStyleSheet(f"background-color: {SIDEBAR_BG}; border-top: 1px solid {BORDER_COLOR};")
        info_layout = QVBoxLayout(info_widget)
        
        # Obtener información de licencia
        license_info = self.license_model.get_gym_license_info(self.user_id)
        
        gym_label = QLabel(f"Gimnasio: {self.gym_name}")
        gym_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        gym_label.setStyleSheet(f"""
            color: {TEXT_PRIMARY}; 
            font-weight: bold;
            padding: 5px;
        """)
        info_layout.addWidget(gym_label)
        
        if license_info:
            days_left = license_info["days_left"]
            license_label = QLabel(f"Licencia: {days_left} días restantes")
            license_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            color = SUCCESS_COLOR if days_left > 30 else WARNING_COLOR
            license_label.setStyleSheet(f"color: {color}; padding: 5px;")
            info_layout.addWidget(license_label)
        
        version_label = QLabel("FIT APP v1.0")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version_label.setStyleSheet(f"color: {TEXT_SECONDARY}; padding: 5px;")
        info_layout.addWidget(version_label)
        
        left_layout.addWidget(info_widget)
        
        # Panel derecho (contenido)
        right_panel = QWidget()
        right_panel.setStyleSheet(f"background-color: {BG_COLOR};")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        # Barra superior
        top_bar = QWidget()
        top_bar.setFixedHeight(60)
        top_bar.setStyleSheet(f"background-color: {CARD_COLOR}; border-bottom: 1px solid {BORDER_COLOR};")
        top_bar_layout = QHBoxLayout(top_bar)
        
        self.page_title = QLabel("Control de Acceso")
        self.page_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        top_bar_layout.addWidget(self.page_title)
        
        top_bar_layout.addStretch()
        
        # Botón de cerrar sesión
        logout_button = QPushButton("Cerrar Sesión")
        logout_button.setStyleSheet(SECONDARY_BUTTON_STYLE)
        logout_button.setFixedWidth(120)
        logout_button.clicked.connect(self.logout)
        top_bar_layout.addWidget(logout_button)
        
        right_layout.addWidget(top_bar)
        
        # Contenido principal (páginas apiladas)
        self.content_stack = QStackedWidget()
        
        # Configurar páginas para gimnasios
        self.access_tab = AccessTab(self.user_id)
        self.content_stack.addWidget(self.access_tab)
        
        self.members_tab = MembersTab(self.user_id)
        self.content_stack.addWidget(self.members_tab)
        
        self.plans_tab = PlansTab(self.user_id)
        self.content_stack.addWidget(self.plans_tab)
        
        self.reports_tab = ReportsTab(self.user_id)
        self.content_stack.addWidget(self.reports_tab)
        
        right_layout.addWidget(self.content_stack)
        
        # Agregar paneles al layout principal
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel)
        
        # Conectar eventos
        self.menu_list.currentRowChanged.connect(self.change_page)
        self.menu_list.setCurrentRow(0)  # Seleccionar la primera opción por defecto
    
    def logout(self):
        """Cierra la sesión actual y regresa a la pantalla de login."""
        reply = QMessageBox.question(self, "Cerrar Sesión", 
                                    "¿Está seguro que desea cerrar la sesión?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            self.close()
            # El flujo regresará al main() que mostrará nuevamente la ventana de login
    
    def change_page(self, index):
        """Cambia la página mostrada en el contenido principal"""
        # Cambiar el título de la página
        self.page_title.setText(self.menu_list.item(index).text())
        # Cambiar la página mostrada
        self.content_stack.setCurrentIndex(index)
        
    def closeEvent(self, event):
        """Maneja el cierre de la aplicación"""
        # Cerrar conexión a la base de datos
        if hasattr(self, 'license_model'):
            self.license_model.close()
        event.accept()