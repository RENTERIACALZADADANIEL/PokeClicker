import flet as ft
from models.usuario_model import UsuarioModel
from controllers.login_controller import LoginController
from views.login_view import LoginView
from views.dashboard_view import DashboardView 

def main(page: ft.Page):
    page.title = "Poke Clicker"
    
    modelo = UsuarioModel()
    controlador = LoginController(modelo)

    def logout_handler(e):
        page.session.clear()
        page.views.clear()
        page.views.append(LoginView(login_handler))
        page.update()

    def login_handler(email, password):
        usuario, error = controlador.verificar_credenciales(email, password)
        
        if error:
            page.views[-1].lbl_error.value = error
            page.update()
        else:
            # Guardar sesión
            page.session.set("user_id", usuario['id_usuario'])
            page.session.set("username", usuario['username'])
            
            # Navegar al Dashboard
            page.views.clear()
            page.views.append(DashboardView(page, logout_handler))
            page.update()

    # Iniciar con el Login
    page.views.append(LoginView(login_handler))
    page.update()

ft.app(target=main)