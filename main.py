import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont
from ui.login import LoginWindow
from ui.admin.dashboard import AdminDashboard
from ui.gym.dashboard import GymApp
def main():
    app = QApplication(sys.argv)
    
    # Aplicar fuente global
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Mostrar ventana de login
    login_window = LoginWindow()
    login_window.show()
    
    # Bucle principal para login
    app.exec()
    
    # Verificar si el login fue exitoso
    if hasattr(login_window, 'accepted') and login_window.accepted:
        # Iniciar la aplicación correspondiente según el tipo de usuario
        if login_window.user_type == "admin":
            window = AdminDashboard(login_window.user_id)
        else:  # gimnasio
            window = GymApp(login_window.user_id, login_window.user_type, login_window.gym_name)
        
        window.show()
        sys.exit(app.exec())
    
if __name__ == "__main__":
    main()