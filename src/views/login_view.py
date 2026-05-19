import flet as ft
from controllers.auth_controller import AuthController
from models.user import User
from utils.security import generate_token, send_reset_email
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
                    self.register_success_text,
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
            threading.Thread(target=self._delayed_redirect, daemon=True).start()
        else:
            self.message_text.value = message
        
        self.page.update()
    
    def show_forgot_password(self, e):
        """Muestra el diálogo de recuperación de contraseña con envío real"""
        email_field = ft.TextField(
            label="Email",
            hint_text="Ingresa tu correo electrónico",
            width=300,
            border_color=ft.Colors.BLUE_400
        )
        
        status_text = ft.Text("", size=14)
        progress_bar = ft.ProgressBar(width=300, visible=False)
        
        def send_reset_email_action(e):
            email = email_field.value
            
            if not email:
                status_text.value = "❌ Por favor, ingresa tu correo electrónico"
                status_text.color = ft.Colors.RED_400
                self.page.update()
                return
            
            # Mostrar progreso
            progress_bar.visible = True
            status_text.value = "Enviando correo..."
            status_text.color = ft.Colors.BLUE_400
            self.page.update()
            
            # Buscar usuario en la base de datos
            user = User.find_by_email(email)
            
            if user:
                # Generar token para el usuario
                token = generate_token(user.id_usuario, user.email)
                
                # Enviar correo real
                email_sent = send_reset_email(user.email, token, user.username)
                
                if email_sent:
                    status_text.value = f"✅ Correo enviado a {email}"
                    status_text.color = ft.Colors.GREEN_400
                else:
                    # Si falla el envío, mostrar el token para desarrollo
                    status_text.value = f"⚠️ Error al enviar. Token: {token[:20]}..."
                    status_text.color = ft.Colors.ORANGE_400
            else:
                # Por seguridad, mostrar el mismo mensaje
                status_text.value = f"✅ Si el correo existe, recibirás un enlace"
                status_text.color = ft.Colors.GREEN_400
            
            progress_bar.visible = False
            self.page.update()
        
        def close_dialog(e):
            """Cierra el diálogo y redirige al login"""
            self.page.close(dialog)
            # Redirigir a iniciar sesión (ya estamos ahí, solo actualizar)
            self.message_text.value = ""
            self.success_text.value = ""
            self.register_success_text.value = "Revisa tu correo y sigue las instrucciones"
            self.register_success_text.color = ft.Colors.BLUE_600
            self.page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Recuperar Contraseña", weight=ft.FontWeight.BOLD),
            content=ft.Column([
                ft.Text(
                    "Ingresa tu correo electrónico y te enviaremos un enlace para restablecer tu contraseña.",
                    size=14
                ),
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                email_field,
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                progress_bar,
                status_text
            ], tight=True, spacing=10),
            actions=[
                ft.TextButton("Cancelar", on_click=close_dialog),
                ft.ElevatedButton(
                    "Enviar correo",
                    on_click=send_reset_email_action,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.BLUE_700,
                        color=ft.Colors.WHITE
                    )
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=close_dialog  # Cuando se cierra de cualquier forma
        )
        
        self.page.show_dialog(dialog)