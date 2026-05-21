import flet as ft
from controllers.auth_controller import AuthController
from utils.security import verify_token
import threading
import time

class ResetPasswordView:
    def __init__(self, page: ft.Page, token: str, on_success, on_cancel):
        self.page = page
        self.token = token
        self.on_success = on_success
        self.on_cancel = on_cancel
        self.auth_controller = AuthController()
        
        # Verificar token al iniciar
        self.token_valid = False
        self.token_email = ""
        payload = verify_token(token)
        if payload:
            self.token_valid = True
            self.token_email = payload.get('email', '')
        
        # Campos
        self.new_password = ft.TextField(
            label="Nueva contraseña",
            password=True,
            can_reveal_password=True,
            width=300,
            border_color=ft.Colors.BLUE_400,
            focused_border_color=ft.Colors.BLUE_700
        )
        
        self.confirm_password = ft.TextField(
            label="Confirmar contraseña",
            password=True,
            can_reveal_password=True,
            width=300,
            border_color=ft.Colors.BLUE_400,
            focused_border_color=ft.Colors.BLUE_700
        )
        
        self.message_text = ft.Text("", color=ft.Colors.RED_400, size=14)
        self.success_text = ft.Text("", color=ft.Colors.GREEN_400, size=14)
        self.password_strength = ft.Text("", size=12)
        
    def build(self):
        # Vista para token inválido
        if not self.token_valid:
            return ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.ERROR_OUTLINE, size=60, color=ft.Colors.RED_400),
                        ft.Text(
                            "Enlace inválido o expirado",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.RED_700
                        ),
                        ft.Text(
                            "El enlace de recuperación no es válido o ha expirado.\nPor favor, solicita uno nuevo desde la aplicación.",
                            size=14,
                            text_align=ft.TextAlign.CENTER,
                            color=ft.Colors.GREY_700
                        ),
                        ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                        ft.ElevatedButton(
                            "Volver al inicio de sesión",
                            on_click=lambda e: self.on_cancel(),
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.BLUE_700,
                                color=ft.Colors.WHITE,
                                padding=15
                            )
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=40,
                border_radius=10,
                bgcolor=ft.Colors.WHITE,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=10,
                    color=ft.Colors.GREY_400
                )
            )
        
        # Vista para token válido
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.LOCK_RESET, size=50, color=ft.Colors.BLUE_400),
                    ft.Text(
                        "Restablecer Contraseña",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE_700
                    ),
                    ft.Text(
                        f"Para: {self.token_email}",
                        size=14,
                        color=ft.Colors.GREY_600
                    ),
                    ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                    self.new_password,
                    self.password_strength,
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    self.confirm_password,
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    ft.Row(
                        [self.message_text, self.success_text],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "Restablecer contraseña",
                                on_click=self.reset_click,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.Colors.BLUE_700,
                                    color=ft.Colors.WHITE,
                                    padding=15
                                )
                            ),
                            ft.TextButton(
                                "Cancelar",
                                on_click=lambda e: self.on_cancel(),
                                style=ft.ButtonStyle(color=ft.Colors.GREY_600)
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=40,
            border_radius=10,
            bgcolor=ft.Colors.WHITE,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.Colors.GREY_400
            )
        )
    
    def reset_click(self, e):
        """Maneja el clic en restablecer contraseña"""
        self.message_text.value = ""
        self.success_text.value = ""
        
        # Validar campos
        if not self.new_password.value or not self.confirm_password.value:
            self.message_text.value = "Por favor, completa todos los campos"
            self.page.update()
            return
        
        # Validar que coincidan
        if self.new_password.value != self.confirm_password.value:
            self.message_text.value = "Las contraseñas no coinciden"
            self.page.update()
            return
        
        # Validar fortaleza
        errors = self.auth_controller.validate_password(self.new_password.value)
        if errors:
            self.message_text.value = "\n".join(errors)
            self.page.update()
            return
        
        # Restablecer contraseña
        data = {
            "token": self.token,
            "new_password": self.new_password.value,
            "confirm_password": self.confirm_password.value
        }
        
        success, message = self.auth_controller.reset_password(data)
        
        if success:
            self.success_text.value = "✅ " + message
            self.new_password.value = ""
            self.confirm_password.value = ""
            self.password_strength.value = ""
            self.page.update()
            
            # Redirigir al login después de 2 segundos
            def redirect():
                time.sleep(2)
                self.on_success()
            threading.Thread(target=redirect, daemon=True).start()
        else:
            self.message_text.value = message
        
        self.page.update()
    
    def check_password_strength(self, e):
        """Muestra la fortaleza de la contraseña en tiempo real"""
        errors = self.auth_controller.validate_password(self.new_password.value)
        
        if not self.new_password.value:
            self.password_strength.value = ""
            self.password_strength.color = ft.Colors.GREY
        elif len(errors) == 0:
            self.password_strength.value = "✅ Contraseña fuerte"
            self.password_strength.color = ft.Colors.GREEN
        elif len(errors) <= 2:
            self.password_strength.value = "⚠️ Contraseña media"
            self.password_strength.color = ft.Colors.ORANGE
        else:
            self.password_strength.value = "❌ Contraseña débil"
            self.password_strength.color = ft.Colors.RED
        
        self.page.update()
