import flet as ft
from views.login_view import LoginView
from views.register_view import RegisterView
from views.reset_password_view import ResetPasswordView
from views.dashboard_view import DashboardView

class PokeClickerApp:
    def __init__(self):
        self.current_user = None
        self.registered_email = None
        self._session_data = {}
        self.page = None
    
    def main(self, page: ft.Page):
        self.page = page
        
        page.title = "Poke Clicker"
        page.window.width = 500
        page.window.height = 700
        page.theme_mode = ft.ThemeMode.LIGHT
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        
        self.container = ft.Container(expand=True)
        
        token = self.get_token_from_url(page)
        
        if token:
            self.show_reset_password(token)
        else:
            self.show_login()
        
        page.add(self.container)
    
    def get_token_from_url(self, page):
        try:
            if hasattr(page, 'query') and page.query:
                if isinstance(page.query, dict):
                    return page.query.get("token")
                elif isinstance(page.query, str) and "token=" in page.query:
                    import urllib.parse
                    params = urllib.parse.parse_qs(page.query)
                    return params.get("token", [None])[0]
            
            import sys
            for arg in sys.argv:
                if arg.startswith("--token="):
                    return arg.replace("--token=", "")
            
            return None
        except Exception as e:
            print(f"Error al obtener token (ignorado): {e}")
            return None
    
    def set_session(self, key, value):
        self._session_data[key] = value
    
    def get_session(self, key, default=None):
        return self._session_data.get(key, default)
    
    def clear_session(self):
        self._session_data.clear()
    
    def show_login(self, prefill_email=None):
        self.clear_session()
        self.current_user = None
        
        login_view = LoginView(
            page=self.page,
            on_login_success=lambda user_data: self.on_login_success(user_data),
            on_register_click=lambda e: self.show_register()
        )
        
        if prefill_email:
            login_view.email_input.value = prefill_email
            login_view.register_success_text.value = "✅ ¡Registro exitoso! Ahora inicia sesión"
        
        self.container.content = login_view.build()
        self.page.update()
    
    def show_register(self):
        register_view = RegisterView(
            page=self.page,
            on_register_success=lambda email: self.on_register_success(email),
            on_login_click=lambda e: self.show_login()
        )
        register_view.email_input.on_change = register_view.validate_email_format
        register_view.password_input.on_change = register_view.check_password_strength
        
        self.container.content = register_view.build()
        self.page.update()
    
    def show_reset_password(self, token):
        reset_view = ResetPasswordView(
            page=self.page,
            token=token,
            on_success=lambda: self.show_login(),
            on_cancel=lambda: self.show_login()
        )
        
        reset_view.new_password.on_change = reset_view.check_password_strength
        
        self.container.content = reset_view.build()
        self.page.update()
    
    def on_register_success(self, email):
        self.registered_email = email
        self.show_login(prefill_email=email)
    
    def on_login_success(self, user_data):
        self.set_session("user_id", user_data.id_usuario)
        self.set_session("username", user_data.username)
        self.set_session("email", user_data.email)
        self.current_user = user_data
        
        print(f"✅ Login exitoso: {user_data.username}")
        self.show_dashboard()
    
    def show_dashboard(self):
        """Muestra el dashboard principal del juego con las 3 pestañas"""
        username = self.get_session("username", "Entrenador")
        
        def logout(e=None):
            """Cierra sesión y vuelve al login"""
            print("Cerrando sesión...")
            self.clear_session()
            self.current_user = None
            self.page.views.clear()
            self.page.add(self.container)
            self.show_login()
        
        # Crear el dashboard
        dashboard = DashboardView(
            username=username,
            on_logout=logout
        )
        
        # Navegar al dashboard
        self.page.views.clear()
        self.page.views.append(dashboard)
        self.page.go("/dashboard")
        
        print(f"🎮 Dashboard cargado para: {username}")


if __name__ == "__main__":
    app = PokeClickerApp()
    ft.app(target=app.main)
