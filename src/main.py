import flet as ft
from models.usuario_model import UsuarioModel
from controllers.login_controller import LoginController
from views.login_view import LoginView

def main(page: ft.Page):
    page.title = "Poke Clicker Login"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    model = UsuarioModel()
    
    # Esta función conecta la Vista con el Controlador
    def handle_login(email, password):
        resultado = controller.intentar_login(email, password)
        if resultado is True:
            page.clean()
            page.add(ft.Text(f"¡Bienvenido de nuevo! Redirigiendo al juego..."))
            # Aquí cargarías tu vista de juego
        else:
            login_ui.lbl_error.value = resultado
            page.update()

    controller = LoginController(model, None)
    login_ui = LoginView(handle_login)
    
    page.add(login_ui)

ft.app(target=main)