import flet as ft
from views.login_view import LoginView
from views.register_view import RegisterView
from views.reset_password_view import ResetPasswordView

class PokeClickerApp:
    def __init__(self):
        self.current_user = None
        self.registered_email = None
    
    def main(self, page: ft.Page):
        page.title = "Poke Clicker"
        page.window.width = 500
        page.window.height = 700
        page.theme_mode = ft.ThemeMode.LIGHT
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        
        # Contenedor principal
        self.container = ft.Container()
        
        # Verificar si hay un token en la URL (deep link desde correo)
        token = self.get_token_from_url(page)
        
        if token:
            # Mostrar vista de reset de contraseña
            self.show_reset_password(page, token)
        else:
            # Mostrar vista de login
            self.show_login(page)
        
        page.add(self.container)
    
    def get_token_from_url(self, page):
        """Obtiene el token de la URL si existe"""
        try:
            # Verificar query parameters
            if hasattr(page, 'query') and page.query:
                return page.query.get("token")
            
            # Verificar si hay argumentos de línea de comandos
            import sys
            for arg in sys.argv:
                if arg.startswith("--token="):
                    return arg.replace("--token=", "")
            
            return None
        except Exception as e:
            print(f"Error al obtener token: {e}")
            return None
    
    def show_login(self, page, prefill_email=None):
        """Muestra la vista de login"""
        login_view = LoginView(
            page=page,
            on_login_success=lambda: self.on_login_success(page),
            on_register_click=lambda e: self.show_register(page)
        )
        
        if prefill_email:
            login_view.email_input.value = prefill_email
            # Mostrar mensaje de registro exitoso
            login_view.register_success_text.value = "✅ ¡Registro exitoso! Ahora inicia sesión"
        
        self.container.content = login_view.build()
        page.update()
    
    def show_register(self, page):
        """Muestra la vista de registro"""
        register_view = RegisterView(
            page=page,
            on_register_success=lambda email: self.on_register_success(page, email),
            on_login_click=lambda e: self.show_login(page)
        )
        register_view.email_input.on_change = register_view.validate_email_format
        register_view.password_input.on_change = register_view.check_password_strength
        
        self.container.content = register_view.build()
        page.update()
    
    def show_reset_password(self, page, token):
        """Muestra la vista de restablecer contraseña"""
        reset_view = ResetPasswordView(
            page=page,
            token=token,
            on_success=lambda: self.show_login(page),
            on_cancel=lambda: self.show_login(page)
        )
        
        # Agregar validador de contraseña en tiempo real
        reset_view.new_password.on_change = reset_view.check_password_strength
        
        self.container.content = reset_view.build()
        page.update()
    
    def on_register_success(self, page, email):
        """Callback cuando el registro es exitoso"""
        self.registered_email = email
        self.show_login(page, prefill_email=email)
    
    def on_login_success(self, page):
        """Callback cuando el login es exitoso"""
        self.container.content = ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, size=60, color=ft.Colors.GREEN_400),
                ft.Text("¡Login exitoso!", size=30, weight=ft.FontWeight.BOLD),
                ft.Text("Redirigiendo al juego...", size=16),
                ft.ProgressBar(width=200, color=ft.Colors.BLUE_400)
            ], alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            alignment=ft.alignment.center,
            padding=40
        )
        page.update()

def main():
    """Función principal que inicia la aplicación"""
    app = PokeClickerApp()
    ft.app(target=app.main)

if __name__ == "__main__":
    main()