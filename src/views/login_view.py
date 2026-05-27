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
            keyboard_type=ft.KeyboardType.EMAIL,
            autofocus=True
        )
        
        self.password_input = ft.TextField(
            label="Contraseña",
            password=True,
            can_reveal_password=True,
            width=300,
            border_color=ft.Colors.BLUE_400,
            focused_border_color=ft.Colors.BLUE_700,
            on_submit=self.login_click
        )
        
        # Textos de mensajes
        self.message_text = ft.Text("", color=ft.Colors.RED_400, size=14)
        self.success_text = ft.Text("", color=ft.Colors.GREEN_400, size=14)
        self.register_success_text = ft.Text("", color=ft.Colors.GREEN_600, size=16, weight=ft.FontWeight.BOLD)
        self.loading_indicator = ft.ProgressBar(width=300, visible=False, color=ft.Colors.BLUE_400)
        
    def build(self):
        """Construye la vista de login"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.CATCHING_POKEMON, size=60, color=ft.Colors.BLUE_700),
                    ft.Text("Iniciar Sesión", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
                    self.register_success_text,
                    ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                    self.email_input,
                    self.password_input,
                    self.loading_indicator,
                    ft.Row(
                        [self.message_text, self.success_text],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    ft.FilledButton(
                        "Iniciar Sesión",
                        on_click=self.login_click,
                        width=300,
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.BLUE_700,
                            color=ft.Colors.WHITE,
                            padding=15,
                            shape=ft.RoundedRectangleBorder(radius=8)
                        )
                    ),
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    ft.TextButton(
                        "¿No tienes cuenta? Regístrate",
                        on_click=self.on_register_click,
                        style=ft.ButtonStyle(color=ft.Colors.BLUE_700)
                    ),
                    ft.TextButton(
                        "¿Olvidaste tu contraseña?",
                        on_click=lambda e: self.mostrar_paso1(),
                        style=ft.ButtonStyle(color=ft.Colors.BLUE_400)
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
    
    def login_click(self, e=None):
        """Maneja el clic en el botón de inicio de sesión"""
        self.message_text.value = ""
        self.success_text.value = ""
        self.register_success_text.value = ""
        
        if not self.email_input.value or not self.password_input.value:
            self.message_text.value = "Por favor, completa todos los campos"
            self.page.update()
            return
        
        if not self.auth_controller.validate_email(self.email_input.value):
            self.message_text.value = "Formato de email inválido"
            self.page.update()
            return
        
        self.loading_indicator.visible = True
        self.message_text.value = "Iniciando sesión..."
        self.message_text.color = ft.Colors.BLUE_400
        self.page.update()
        
        data = {
            "email": self.email_input.value,
            "password": self.password_input.value
        }
        
        success, message = self.auth_controller.login_user(data)
        
        self.loading_indicator.visible = False
        
        if success:
            self.success_text.value = message
            self.message_text.value = ""
            self.page.update()
            
            if self.auth_controller.current_user:
                self.on_login_success(self.auth_controller.current_user)
        else:
            self.message_text.value = message
            self.message_text.color = ft.Colors.RED_400
            self.password_input.value = ""
            self.password_input.focus()
            self.page.update()
    
    # ============================================================
    # FLUJO DE RECUPERACIÓN DE CONTRASEÑA (3 PASOS)
    # ============================================================
    
    def _mostrar_dialogo(self, dialog):
        """Muestra un diálogo usando overlay (más compatible)"""
        # Cerrar diálogo anterior si existe
        self._cerrar_dialogo()
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()
    
    def _cerrar_dialogo(self):
        """Cierra todos los diálogos"""
        for control in self.page.overlay[:]:
            if isinstance(control, ft.AlertDialog):
                control.open = False
                self.page.overlay.remove(control)
        self.page.update()
    
    # ============================================================
    # PASO 1: SOLICITAR TOKEN
    # ============================================================
    
    def mostrar_paso1(self):
        """Paso 1: Ingresar email para recibir el token"""
        print("🔑 Abriendo Paso 1 - Recuperación de contraseña")
        
        email_field = ft.TextField(
            label="Email",
            hint_text="Ingresa tu correo electrónico",
            width=300,
            border_color=ft.Colors.BLUE_400,
            keyboard_type=ft.KeyboardType.EMAIL,
            autofocus=True
        )
        
        status_text = ft.Text("", size=14)
        progress_bar = ft.ProgressBar(width=300, visible=False, color=ft.Colors.BLUE_400)
        
        def enviar_token(e):
            print("📧 Enviando token...")
            email = email_field.value
            
            if not email:
                status_text.value = "❌ Ingresa tu correo electrónico"
                status_text.color = ft.Colors.RED_400
                self.page.update()
                return
            
            progress_bar.visible = True
            status_text.value = "⏳ Enviando código..."
            status_text.color = ft.Colors.BLUE_400
            self.page.update()
            
            success, message = self.auth_controller.request_password_reset(email)
            
            progress_bar.visible = False
            
            if success:
                status_text.value = f"✅ {message}"
                status_text.color = ft.Colors.GREEN_400
                self.page.update()
                
                # Pasar al paso 2 después de 1.5 segundos
                def ir_paso2():
                    time.sleep(1.5)
                    self._cerrar_dialogo()
                    self.mostrar_paso2(email)
                
                threading.Thread(target=ir_paso2, daemon=True).start()
            else:
                status_text.value = f"❌ {message}"
                status_text.color = ft.Colors.RED_400
                self.page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Recuperar Contraseña - Paso 1/3", weight=ft.FontWeight.BOLD),
            content=ft.Column([
                ft.Text("Ingresa tu correo y te enviaremos un código de 6 caracteres.", size=14),
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                email_field,
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                progress_bar,
                status_text
            ], tight=True, spacing=10, width=350),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self._cerrar_dialogo()),
                ft.FilledButton(
                    "Enviar código",
                    on_click=enviar_token,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.BLUE_700,
                        color=ft.Colors.WHITE
                    )
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        self._mostrar_dialogo(dialog)
        print("✅ Diálogo Paso 1 mostrado")
    
    # ============================================================
    # PASO 2: VERIFICAR TOKEN
    # ============================================================
    
    def mostrar_paso2(self, email):
        """Paso 2: Ingresar el token de 6 caracteres"""
        print("🔑 Abriendo Paso 2 - Verificar token")
        
        token_field = ft.TextField(
            label="Código de 6 caracteres",
            hint_text="Ej: A7B2X9",
            width=300,
            border_color=ft.Colors.BLUE_400,
            text_align=ft.TextAlign.CENTER,
            max_length=6,
            capitalization=ft.TextCapitalization.CHARACTERS,
            autofocus=True
        )
        
        status_text = ft.Text(
            f"Se envió un código a {email}",
            size=14,
            color=ft.Colors.GREY_600
        )
        error_text = ft.Text("", size=14, color=ft.Colors.RED_400)
        
        def verificar_token(e):
            print("🔍 Verificando token...")
            token = token_field.value.strip().upper()
            
            if len(token) != 6:
                error_text.value = "❌ El código debe tener 6 caracteres"
                self.page.update()
                return
            
            success, message, user_data = self.auth_controller.verify_token(token)
            
            if success:
                self._cerrar_dialogo()
                self.mostrar_paso3(user_data["token"])
            else:
                error_text.value = f"❌ {message}"
                self.page.update()
        
        def reenviar_token(e):
            print("📧 Reenviando token...")
            success, message = self.auth_controller.request_password_reset(email)
            if success:
                status_text.value = f"✅ Nuevo código enviado a {email}"
                status_text.color = ft.Colors.GREEN_400
            else:
                status_text.value = f"❌ {message}"
                status_text.color = ft.Colors.RED_400
            self.page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Verificar Código - Paso 2/3", weight=ft.FontWeight.BOLD),
            content=ft.Column([
                status_text,
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                ft.Text("Ingresa el código de 6 caracteres que enviamos a tu correo.", size=14),
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                token_field,
                ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
                error_text
            ], tight=True, spacing=10, width=350),
            actions=[
                ft.TextButton("Reenviar código", on_click=reenviar_token),
                ft.TextButton("Cancelar", on_click=lambda e: self._cerrar_dialogo()),
                ft.FilledButton(
                    "Verificar",
                    on_click=verificar_token,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.BLUE_700,
                        color=ft.Colors.WHITE
                    )
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        self._mostrar_dialogo(dialog)
        print("✅ Diálogo Paso 2 mostrado")
    
    # ============================================================
    # PASO 3: NUEVA CONTRASEÑA
    # ============================================================
    
    def mostrar_paso3(self, token):
        """Paso 3: Ingresar nueva contraseña"""
        print("🔑 Abriendo Paso 3 - Nueva contraseña")
        
        new_password = ft.TextField(
            label="Nueva contraseña",
            password=True,
            can_reveal_password=True,
            width=300,
            border_color=ft.Colors.BLUE_400,
            autofocus=True
        )
        
        confirm_password = ft.TextField(
            label="Confirmar contraseña",
            password=True,
            can_reveal_password=True,
            width=300,
            border_color=ft.Colors.BLUE_400
        )
        
        error_text = ft.Text("", size=14, color=ft.Colors.RED_400)
        success_text = ft.Text("", size=14, color=ft.Colors.GREEN_400)
        password_strength = ft.Text("", size=12)
        
        def check_strength(e):
            errors = self.auth_controller.validate_password(new_password.value)
            
            if not new_password.value:
                password_strength.value = ""
                password_strength.color = ft.Colors.GREY
            elif len(errors) == 0:
                password_strength.value = "✅ Contraseña fuerte"
                password_strength.color = ft.Colors.GREEN
            elif len(errors) <= 2:
                password_strength.value = "⚠️ Contraseña media"
                password_strength.color = ft.Colors.ORANGE
            else:
                password_strength.value = "❌ Contraseña débil"
                password_strength.color = ft.Colors.RED
            
            self.page.update()
        
        new_password.on_change = check_strength
        
        def cambiar_password(e):
            print("🔒 Cambiando contraseña...")
            error_text.value = ""
            success_text.value = ""
            
            if not new_password.value or not confirm_password.value:
                error_text.value = "❌ Completa todos los campos"
                self.page.update()
                return
            
            if new_password.value != confirm_password.value:
                error_text.value = "❌ Las contraseñas no coinciden"
                self.page.update()
                return
            
            errors = self.auth_controller.validate_password(new_password.value)
            if errors:
                error_text.value = "❌ " + "\n".join(errors)
                self.page.update()
                return
            
            success, message = self.auth_controller.reset_password_with_token(
                token, new_password.value
            )
            
            if success:
                success_text.value = f"✅ {message}"
                self.page.update()
                
                def cerrar():
                    time.sleep(2)
                    self._cerrar_dialogo()
                    self.register_success_text.value = "✅ Contraseña actualizada. Inicia sesión."
                    self.register_success_text.color = ft.Colors.GREEN_600
                    self.page.update()
                
                threading.Thread(target=cerrar, daemon=True).start()
            else:
                error_text.value = f"❌ {message}"
                self.page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Nueva Contraseña - Paso 3/3", weight=ft.FontWeight.BOLD),
            content=ft.Column([
                ft.Text("Ingresa tu nueva contraseña:", size=14),
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                new_password,
                password_strength,
                ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
                confirm_password,
                ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
                error_text,
                success_text
            ], tight=True, spacing=10, width=350),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self._cerrar_dialogo()),
                ft.FilledButton(
                    "Cambiar contraseña",
                    on_click=cambiar_password,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.GREEN_700,
                        color=ft.Colors.WHITE
                    )
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        self._mostrar_dialogo(dialog)
        print("✅ Diálogo Paso 3 mostrado")