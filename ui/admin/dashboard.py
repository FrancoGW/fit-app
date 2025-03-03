from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QLabel, QPushButton, QListWidget, QListWidgetItem, 
                           QStackedWidget, QMessageBox)
from PyQt6.QtCore import Qt, QSize

from config.constants import (BG_COLOR, TEXT_PRIMARY, TEXT_SECONDARY, 
                            SIDEBAR_BG, BORDER_COLOR, PRIMARY_COLOR,
                            CARD_COLOR, SECONDARY_BUTTON_STYLE, SIDEBAR_STYLE)
from ui.admin.gyms_tab import GymsTab
from ui.admin.licenses_tab import LicensesTab
from ui.admin.stats_tab import StatsTab
from ui.admin.settings_tab import SettingsTab
from models.user import UserModel

class AdminDashboard(QMainWindow):
    """Panel de administración para el dueño de la aplicación"""
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("FIT APP - Panel de Administración")
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
        """)
        
        self.user_model = UserModel()
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
        logo_label.setStyleSheet(f"""
            color: {PRIMARY_COLOR}; 
            font-size: 24px; 
            font-weight: bold;
        """)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addWidget(logo_label)
        
        left_layout.addWidget(logo_container)
        
        # Menú de navegación
        self.menu_list = QListWidget()
        self.menu_list.setIconSize(QSize(24, 24))
        self.menu_list.setStyleSheet(SIDEBAR_STYLE)
        
        # Opciones de menú para admin
        menu_items = [
            ("Gestionar Gimnasios", "gyms_page"),
            ("Gestionar Licencias", "licenses_page"),
            ("Estadísticas", "stats_page"),
            ("Configuración", "settings_page")
        ]
        
        for text, page_name in menu_items:
            item = QListWidgetItem(text)
            item.setData(Qt.ItemDataRole.UserRole, page_name)
            self.menu_list.addItem(item)
        
        left_layout.addWidget(self.menu_list)
        
        # Widget para mostrar información en la parte inferior del menú
        info_widget = QWidget()
        info_widget.setFixedHeight(120)
        info_widget.setStyleSheet(f"""
            background-color: {SIDEBAR_BG}; 
            border-top: 1px solid {BORDER_COLOR};
        """)
        info_layout = QVBoxLayout(info_widget)
        info_layout.setSpacing(5)
        
        # Obtener el nombre de usuario
        self.user_model.cursor.execute("SELECT username FROM usuarios WHERE id = ?", (self.user_id,))
        username = self.user_model.cursor.fetchone()[0]
        
        user_label = QLabel(f"Usuario: {username}")
        user_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        user_label.setStyleSheet(f"color: {TEXT_PRIMARY}; font-weight: bold;")
        info_layout.addWidget(user_label)
        
        role_label = QLabel("Rol: Administrador")
        role_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        role_label.setStyleSheet(f"color: {TEXT_SECONDARY};")
        info_layout.addWidget(role_label)
        
        version_label = QLabel("FIT APP v1.0")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version_label.setStyleSheet(f"color: {TEXT_SECONDARY};")
        info_layout.addWidget(version_label)
        
        left_layout.addWidget(info_widget)
        
        # Panel derecho (contenido)
        right_panel = QWidget()
        right_panel.setStyleSheet(f"background-color: {BG_COLOR};")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        # Barra superior
        top_bar = QWidget()
        top_bar.setFixedHeight(70)
        top_bar.setStyleSheet(f"background-color: {CARD_COLOR}; border-bottom: 1px solid {BORDER_COLOR};")
        top_bar_layout = QHBoxLayout(top_bar)
        top_bar_layout.setContentsMargins(20, 0, 20, 0)
        
        self.page_title = QLabel("Gestionar Gimnasios")
        self.page_title.setObjectName("pageTitle")
        top_bar_layout.addWidget(self.page_title)
        
        top_bar_layout.addStretch()
        
        # Botón de cerrar sesión
        logout_button = QPushButton("Cerrar Sesión")
        logout_button.setStyleSheet(SECONDARY_BUTTON_STYLE)
        logout_button.setFixedWidth(150)
        logout_button.clicked.connect(self.logout)
        top_bar_layout.addWidget(logout_button)
        
        right_layout.addWidget(top_bar)
        
        # Contenido principal (páginas apiladas)
        self.content_stack = QStackedWidget()
        
        # Configurar páginas
        self.gyms_page = GymsTab(self.user_id)
        self.content_stack.addWidget(self.gyms_page)
        
        self.licenses_page = LicensesTab()
        self.content_stack.addWidget(self.licenses_page)
        
        self.stats_page = StatsTab()
        self.content_stack.addWidget(self.stats_page)
        
        self.settings_page = SettingsTab(self.user_id)
        self.content_stack.addWidget(self.settings_page)
        
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
        """Maneja el cierre de la ventana"""
        # Cerrar conexión a la base de datos
        if hasattr(self, 'user_model'):
            self.user_model.close()
        
        event.accept()