import flet as ft
from controllers.auth_controller import AuthController
import threading
import time

class LoginView:
    def __init__(self, page: ft.Page, on_login_success, on_register_click):
        self.page = page
        self.on_login_success = on_login_success
        self.on_register_click = on_register_click
        self.auth_controller = AuthController()
        
        # Campos de entrada
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
        
        self.message_text = ft.Text("", color=ft.Colors.RED_400, size=14)
        self.success_text = ft.Text("", color=ft.Colors.GREEN_400, size=14)
        
        # Mensaje de bienvenida para usuarios recién registrados
        self.register_success_text = ft.Text("", color=ft.Colors.GREEN_600, size=16, weight=ft.FontWeight.BOLD)
        
    def build(self):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Iniciar Sesión",
                        size=30,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE_700
                    ),
                    self.register_success_text,  # Mensaje de registro exitoso
                    ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                    self.email_input,
                    self.password_input,
                    ft.Row(
                        [self.message_text, self.success_text],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.ElevatedButton(
                        "Iniciar Sesión",
                        on_click=self.login_click,
                        width=300,
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.BLUE_700,
                            color=ft.Colors.WHITE,
                            padding=15
                        )
                    ),
                    ft.TextButton(
                        "¿No tienes cuenta? Regístrate",
                        on_click=self.on_register_click,
                        style=ft.ButtonStyle(color=ft.Colors.BLUE_700)
                    ),
                    ft.TextButton(
                        "¿Olvidaste tu contraseña?",
                        on_click=self.show_forgot_password,
                        style=ft.ButtonStyle(color=ft.Colors.BLUE_400)
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=30,
            border_radius=10,
            bgcolor=ft.Colors.WHITE,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.Colors.GREY_400
            )
        )
    
    def _delayed_redirect(self):
        """Espera y redirige después del login exitoso"""
        time.sleep(1)
        self.on_login_success()
    
    def login_click(self, e):
        # Limpiar mensajes
        self.message_text.value = ""
        self.success_text.value = ""
        self.register_success_text.value = ""
        
        # Validar campos
        if not self.email_input.value or not self.password_input.value:
            self.message_text.value = "Por favor, completa todos los campos"
            self.page.update()
            return
        
        # Intentar login
        data = {
            "email": self.email_input.value,
            "password": self.password_input.value
        }
        
        success, message = self.auth_controller.login_user(data)
        
        if success:
            self.success_text.value = message
            self.page.update()
            # Redirigir usando threading
            threading.Thread(target=self._delayed_redirect, daemon=True).start()
        else:
            self.message_text.value = message
        
        self.page.update()
    
    def show_forgot_password(self, e):
        """Muestra el diálogo de recuperación de contraseña"""
        email_field = ft.TextField(
            label="Email",
            hint_text="Ingresa tu correo electrónico",
            width=300
        )
        
        def send_reset(e):
            if email_field.value:
                success, message = self.auth_controller.request_password_reset(email_field.value)
                
                # Mostrar mensaje
                dialog.content = ft.Column([
                    ft.Text(message, size=16, text_align=ft.TextAlign.CENTER),
                    ft.ElevatedButton("Cerrar", on_click=lambda e: self.page.close(dialog))
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                self.page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Recuperar Contraseña"),
            content=ft.Column([
                ft.Text("Ingresa tu correo para recibir un enlace de recuperación:", size=14),
                email_field,
                ft.ElevatedButton("Enviar", on_click=send_reset)
            ], tight=True),
        )
        
        self.page.show_dialog(dialog)