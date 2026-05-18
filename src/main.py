import flet as ft
from views.login_view import LoginView
from views.register_view import RegisterView

class PokeClickerApp:
    def __init__(self):
        self.current_user = None
        self.registered_email = None  # Para guardar el email del registro
    
    def main(self, page: ft.Page):
        page.title = "Poke Clicker - Login"
        page.window.width = 500
        page.window.height = 700
        page.theme_mode = ft.ThemeMode.LIGHT
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        
        # Contenedor principal
        self.container = ft.Container()
        
        # Mostrar vista de login inicialmente
        self.show_login(page)
        
        page.add(self.container)
    
    def show_login(self, page, prefill_email=None):
        """Muestra la vista de login, opcionalmente con email pre-rellenado"""
        login_view = LoginView(
            page=page,
            on_login_success=lambda: self.on_login_success(page),
            on_register_click=lambda e: self.show_register(page)
        )
        
        # Si viene de un registro exitoso, pre-rellenar el email
        if prefill_email:
            login_view.email_input.value = prefill_email
        
        self.container.content = login_view.build()
        page.update()
    
    def show_register(self, page):
        """Muestra la vista de registro"""
        register_view = RegisterView(
            page=page,
            on_register_success=lambda email: self.on_register_success(page, email),
            on_login_click=lambda e: self.show_login(page)
        )
        # Agregar validadores en tiempo real
        register_view.email_input.on_change = register_view.validate_email_format
        register_view.password_input.on_change = register_view.check_password_strength
        
        self.container.content = register_view.build()
        page.update()
    
    def on_register_success(self, page, email):
        """Callback cuando el registro es exitoso"""
        # Guardar el email y redirigir al login
        self.registered_email = email
        self.show_login(page, prefill_email=email)
    
    def on_login_success(self, page):
        """Callback cuando el login es exitoso"""
        # Aquí iría la lógica para mostrar el juego principal
        self.container.content = ft.Container(
            content=ft.Column([
                ft.Text("¡Login exitoso!", size=30, weight=ft.FontWeight.BOLD),
                ft.Text("Redirigiendo al juego...", size=16)
            ], alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            alignment=ft.alignment.center
        )
        page.update()

# Función principal
def main():
    """Función principal que inicia la aplicación"""
    app = PokeClickerApp()
    ft.app(target=app.main)

if __name__ == "__main__":
    main()