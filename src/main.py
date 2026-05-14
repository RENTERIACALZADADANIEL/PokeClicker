import flet as ft
from models.usuario_model import UsuarioModel
from controllers.login_controller import LoginController
from views.login_view import LoginView
from views.registro_view import RegistroView
from views.dashboard_view import DashboardView

def main(page: ft.Page):
    # --- Configuración General ---
    page.title = "Poke Clicker"
    page.window_width = 450
    page.window_height = 800
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # Inicialización de MVC
    modelo = UsuarioModel()
    controlador = LoginController(modelo)

    # --- Handlers de Navegación ---

    def ir_a_registro(e):
        page.views.clear()
        page.views.append(RegistroView(registro_handler, ir_a_login))
        page.update()

    def ir_a_login(e=None):
        page.views.clear()
        page.views.append(LoginView(login_handler, ir_a_registro))
        page.update()

    def logout_handler(e):
        page.session.clear() # Limpia todos los datos de sesión
        ir_a_login()

    # --- Procesadores de Datos ---

    def registro_handler(username, email, password):
        resultado = controlador.crear_cuenta(username, email, password)
        
        if resultado is True:
            ir_a_login()
            page.snack_bar = ft.SnackBar(ft.Text("¡Cuenta creada con éxito!"))
            page.snack_bar.open = True
            page.update()
        else:
            # Accedemos a la última vista cargada (Registro) para mostrar el error
            page.views[-1].lbl_msg.value = resultado
            page.views[-1].lbl_msg.color = "red"
            page.update()

    def login_handler(email, password):
        usuario, error = controlador.verificar_credenciales(email, password)
        
        if error:
            page.views[-1].lbl_error.value = error
            page.update()
        else:
            # --- MANEJO DE SESIÓN CORREGIDO ---
            # Flet ahora usa la sesión como un diccionario estándar
            page.session["user_id"] = usuario['id_usuario']
            page.session["username"] = usuario['username']
            
            # Navegar al Dashboard
            page.views.clear()
            page.views.append(DashboardView(page, logout_handler))
            page.update()

    # --- Inicio de la Aplicación ---
    ir_a_login()

# --- EJECUCIÓN CORREGIDA ---
if __name__ == "__main__":
    # Usamos ft.app (o ft.run en versiones muy nuevas) 
    # pero asegurando que el target sea la función main
    ft.app(target=main)