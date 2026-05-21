import flet as ft
from controllers.auth_controller import AuthController

class RegisterView:
    def __init__(self, page: ft.Page, on_register_success, on_login_click):
        self.page = page
        self.on_register_success = on_register_success
        self.on_login_click = on_login_click
        self.auth_controller = AuthController()
        
        self.username_input = ft.TextField(
            label="Nombre de usuario",
            hint_text="Elige un nombre de usuario",
            width=300,
            border_color=ft.Colors.BLUE_400,
            focused_border_color=ft.Colors.BLUE_700
        )
        
        self.email_input = ft.TextField(
            label="Email",
            hint_text="tu@email.com",
            width=300,
            border_color=ft.Colors.BLUE_400,
            focused_border_color=ft.Colors.BLUE_700,
            keyboard_type=ft.KeyboardType.EMAIL
        )
        
        self.password_input = ft.TextField(
            label="Contraseña",
            password=True,
            can_reveal_password=True,
            width=300,
            border_color=ft.Colors.BLUE_400,
            focused_border_color=ft.Colors.BLUE_700
        )
        
        self.confirm_password_input = ft.TextField(
            label="Confirmar Contraseña",
            password=True,
            can_reveal_password=True,
            width=300,
            border_color=ft.Colors.BLUE_400,
            focused_border_color=ft.Colors.BLUE_700
        )
        
        self.message_text = ft.Text("", color=ft.Colors.RED_400, size=14)
        self.success_text = ft.Text("", color=ft.Colors.GREEN_400, size=14)
        self.email_valid = ft.Icon(ft.Icons.CIRCLE_OUTLINED, size=10, color=ft.Colors.GREY_400)
        self.password_strength = ft.Text("", size=12)
        
    def build(self):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Crear Cuenta", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
                    ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                    self.username_input,
                    ft.Row([self.email_input, self.email_valid], alignment=ft.MainAxisAlignment.CENTER),
                    self.password_input,
                    self.password_strength,
                    self.confirm_password_input,
                    ft.Row([self.message_text, self.success_text], alignment=ft.MainAxisAlignment.CENTER),
                    ft.ElevatedButton(
                        "Registrarse",
                        on_click=self.register_click,
                        width=300,
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.BLUE_700,
                            color=ft.Colors.WHITE,
                            padding=15
                        )
                    ),
                    ft.TextButton(
                        "¿Ya tienes cuenta? Inicia Sesión",
                        on_click=self.on_login_click,
                        style=ft.ButtonStyle(color=ft.Colors.BLUE_700)
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=30,
            border_radius=10,
            bgcolor=ft.Colors.WHITE,
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.GREY_400)
        )
    
    def register_click(self, e):
        self.message_text.value = ""
        self.success_text.value = ""
        
        if not all([
            self.username_input.value,
            self.email_input.value,
            self.password_input.value,
            self.confirm_password_input.value
        ]):
            self.message_text.value = "Por favor, completa todos los campos"
            self.page.update()
            return
        
        password_errors = self.auth_controller.validate_password(self.password_input.value)
        if password_errors:
            self.message_text.value = "\n".join(password_errors)
            self.page.update()
            return
        
        data = {
            "username": self.username_input.value,
            "email": self.email_input.value,
            "password": self.password_input.value,
            "confirm_password": self.confirm_password_input.value
        }
        
        success, message = self.auth_controller.register_user(data)
        
        if success:
            self.success_text.value = message
            saved_email = self.email_input.value
            self.page.update()
            
            # Limpiar campos
            self.username_input.value = ""
            self.email_input.value = ""
            self.password_input.value = ""
            self.confirm_password_input.value = ""
            self.password_strength.value = ""
            self.email_valid.name = ft.Icons.CIRCLE_OUTLINED
            self.email_valid.color = ft.Colors.GREY_400
            
            # Navegar directamente al login
            self.on_register_success(saved_email)
        else:
            self.message_text.value = message
            self.page.update()
    
    def validate_email_format(self, e):
        if self.email_input.value:
            if self.auth_controller.validate_email(self.email_input.value):
                self.email_valid.name = ft.Icons.CHECK_CIRCLE_OUTLINE
                self.email_valid.color = ft.Colors.GREEN
            else:
                self.email_valid.name = ft.Icons.ERROR_OUTLINE
                self.email_valid.color = ft.Colors.RED
        else:
            self.email_valid.name = ft.Icons.CIRCLE_OUTLINED
            self.email_valid.color = ft.Colors.GREY_400
        
        self.page.update()
    
    def check_password_strength(self, e):
        errors = self.auth_controller.validate_password(self.password_input.value)
        
        if not self.password_input.value:
            self.password_strength.value = ""
            self.password_strength.color = ft.Colors.GREY
        elif len(errors) == 0:
            self.password_strength.value = "Contraseña fuerte"
            self.password_strength.color = ft.Colors.GREEN
        elif len(errors) <= 2:
            self.password_strength.value = "Contraseña media"
            self.password_strength.color = ft.Colors.ORANGE
        else:
            self.password_strength.value = "Contraseña débil"
            self.password_strength.color = ft.Colors.RED
        
        self.page.update()
