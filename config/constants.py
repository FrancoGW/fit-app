# Constantes

# Credenciales por defecto
DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "admin123"  # Este será hasheado

# Paleta de colores moderna - Tema Oscuro
SIDEBAR_BG = "#1E1E1E"        # Gris muy oscuro/casi negro para sidebar
SIDEBAR_HOVER = "#2D2D2D"     # Gris oscuro para hover
PRIMARY_COLOR = "#3B82F6"     # Azul brillante para selección/acciones principales
PRIMARY_DARK = "#2563EB"      # Azul oscuro para hover en botones principales
PRIMARY_LIGHT = "#60A5FA"     # Azul claro para acentos
SECONDARY_COLOR = "#4B5563"   # Gris para elementos secundarios
ACCENT_COLOR = "#10B981"      # Verde para éxito
SUCCESS_COLOR = "#10B981"      # Verde para éxito
DANGER_COLOR = "#EF4444"      # Rojo para errores/peligro
WARNING_COLOR = "#F59E0B"     # Ámbar para advertencias
BG_COLOR = "#111827"          # Fondo principal muy oscuro
CARD_COLOR = "#1F2937"        # Color para tarjetas/paneles
TEXT_PRIMARY = "#F9FAFB"      # Texto principal (casi blanco)
TEXT_SECONDARY = "#9CA3AF"    # Texto secundario (gris claro)
BORDER_COLOR = "#374151"      # Color para bordes

# Estilos para componentes
BUTTON_STYLE = f"""
    QPushButton {{
        background-color: {PRIMARY_COLOR};
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 6px;
        font-weight: bold;
        font-size: 14px;
    }}
    QPushButton:hover {{
        background-color: {PRIMARY_DARK};
    }}
    QPushButton:pressed {{
        background-color: {PRIMARY_DARK};
    }}
    QPushButton:disabled {{
        background-color: {SECONDARY_COLOR};
        color: {TEXT_SECONDARY};
    }}
"""

SECONDARY_BUTTON_STYLE = f"""
    QPushButton {{
        background-color: {CARD_COLOR};
        color: {TEXT_PRIMARY};
        border: 1px solid {BORDER_COLOR};
        padding: 10px 20px;
        border-radius: 6px;
        font-weight: bold;
        font-size: 14px;
    }}
    QPushButton:hover {{
        background-color: {SIDEBAR_HOVER};
        border-color: {PRIMARY_COLOR};
    }}
    QPushButton:pressed {{
        background-color: {SIDEBAR_HOVER};
    }}
    QPushButton:disabled {{
        background-color: {SECONDARY_COLOR};
        color: {TEXT_SECONDARY};
    }}
"""

INPUT_STYLE = f"""
    QLineEdit {{
        background-color: {CARD_COLOR};
        color: {TEXT_PRIMARY};
        border: 1px solid {BORDER_COLOR};
        border-radius: 6px;
        padding: 10px;
        font-size: 14px;
    }}
    QLineEdit:focus {{
        border: 1px solid {PRIMARY_COLOR};
    }}
"""

COMBOBOX_STYLE = f"""
    QComboBox {{
        background-color: {CARD_COLOR};
        color: {TEXT_PRIMARY};
        border: 1px solid {BORDER_COLOR};
        border-radius: 6px;
        padding: 10px;
        font-size: 14px;
        min-width: 200px;
    }}
    QComboBox:focus {{
        border: 1px solid {PRIMARY_COLOR};
    }}
    QComboBox::drop-down {{
        border: none;
        width: 20px;
    }}
    QComboBox::down-arrow {{
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 5px solid {TEXT_PRIMARY};
        margin-right: 10px;
    }}
    QComboBox QAbstractItemView {{
        background-color: {CARD_COLOR};
        color: {TEXT_PRIMARY};
        selection-background-color: {PRIMARY_COLOR};
        selection-color: white;
        border: 1px solid {BORDER_COLOR};
    }}
"""

TABLE_STYLE = f"""
    QTableWidget {{
        background-color: {CARD_COLOR};
        color: {TEXT_PRIMARY};
        border: 1px solid {BORDER_COLOR};
        border-radius: 6px;
        gridline-color: {BORDER_COLOR};
    }}
    QTableWidget::item {{
        padding: 5px;
    }}
    QTableWidget::item:selected {{
        background-color: {PRIMARY_COLOR};
        color: white;
    }}
    QHeaderView::section {{
        background-color: {SIDEBAR_BG};
        color: {TEXT_PRIMARY};
        padding: 10px;
        border: none;
        border-right: 1px solid {BORDER_COLOR};
        border-bottom: 1px solid {BORDER_COLOR};
        font-weight: bold;
    }}
    QTableWidget::item:alternate {{
        background-color: {SIDEBAR_HOVER};
    }}
"""

SIDEBAR_STYLE = f"""
    QListWidget {{
        background-color: {SIDEBAR_BG};
        border: none;
        border-right: 1px solid {BORDER_COLOR};
        font-size: 14px;
        outline: none;
        color: {TEXT_PRIMARY};
    }}
    QListWidget::item {{
        padding: 15px 20px;
        border-radius: 0px;
    }}
    QListWidget::item:selected {{
        background-color: {PRIMARY_COLOR};
        color: white;
    }}
    QListWidget::item:hover:!selected {{
        background-color: {SIDEBAR_HOVER};
    }}
"""

FRAME_STYLE = f"""
    QFrame {{
        background-color: {CARD_COLOR};
        border: 1px solid {BORDER_COLOR};
        border-radius: 8px;
    }}
"""

DANGER_BUTTON_STYLE = f"""
    QPushButton {{
        background-color: {DANGER_COLOR};
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 6px;
        font-weight: bold;
        font-size: 14px;
    }}
    QPushButton:hover {{
        background-color: #DC2626;
    }}
    QPushButton:pressed {{
        background-color: #B91C1C;
    }}
"""