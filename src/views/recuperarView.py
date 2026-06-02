import flet as ft
import time

class RecuperarView:
    """Vista de recuperación de contraseña en 3 pasos"""
    
    def __init__(self, page: ft.Page, auth_controller, on_volver):
        self.page = page
        self.auth_controller = auth_controller
        self.on_volver = on_volver
        self.email_guardado = ""
        
        # Campos
        self.email_input = ft.TextField(
            label="Correo electrónico",
            width=350,
            prefix_icon=ft.Icons.EMAIL,
            border_radius=10,
            keyboard_type=ft.KeyboardType.EMAIL
        )
        
        self.codigo_input = ft.TextField(
            label="Código de 6 dígitos",
            width=350,
            prefix_icon=ft.Icons.KEY,
            border_radius=10,
            keyboard_type=ft.KeyboardType.NUMBER,
            max_length=6
        )
        
        self.nueva_pass = ft.TextField(
            label="Nueva contraseña",
            width=350,
            password=True,
            can_reveal_password=True,
            prefix_icon=ft.Icons.LOCK,
            border_radius=10
        )
        
        self.confirmar_pass = ft.TextField(
            label="Confirmar contraseña",
            width=350,
            password=True,
            can_reveal_password=True,
            prefix_icon=ft.Icons.LOCK,
            border_radius=10
        )
        
        self.msg = ft.Text("", size=13)
        
        # PASO 1: Ingresar email
        self.paso1 = ft.Column(
            visible=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
            controls=[
                ft.Icon(ft.Icons.LOCK_RESET, size=50, color=ft.Colors.BLUE_400),
                ft.Text("Recuperar contraseña", size=22, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Ingresa tu correo y te enviaremos un código de 6 dígitos.",
                    size=13,
                    color=ft.Colors.GREY_400,
                    text_align=ft.TextAlign.CENTER
                ),
                self.email_input,
                self.msg,
                ft.FilledButton(
                    "Enviar código",
                    width=250,
                    on_click=lambda e: self.enviar(e),
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.BLUE_400,
                        color=ft.Colors.WHITE,
                        padding=15
                    )
                ),
                ft.TextButton(
                    "Volver al inicio de sesión",
                    on_click=lambda e: on_volver()
                ),
            ]
        )
        
        # PASO 2: Verificar código
        self.paso2 = ft.Column(
            visible=False,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
            controls=[
                ft.Icon(ft.Icons.KEY, size=50, color=ft.Colors.BLUE_400),
                ft.Text("Verificar código", size=22, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Revisa tu correo e ingresa el código de 6 dígitos.",
                    size=13,
                    color=ft.Colors.GREY_400,
                    text_align=ft.TextAlign.CENTER
                ),
                self.codigo_input,
                self.msg,
                ft.FilledButton(
                    "Verificar",
                    width=250,
                    on_click=lambda e: self.verificar(e),
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.BLUE_400,
                        color=ft.Colors.WHITE,
                        padding=15
                    )
                ),
                ft.TextButton(
                    "¿No recibiste el código? Reenviar",
                    on_click=lambda e: self.reenviar(e),
                    style=ft.ButtonStyle(color=ft.Colors.BLUE_300)
                ),
            ]
        )
        
        # PASO 3: Nueva contraseña
        self.paso3 = ft.Column(
            visible=False,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
            controls=[
                ft.Icon(ft.Icons.LOCK, size=50, color=ft.Colors.GREEN_400),
                ft.Text("Nueva contraseña", size=22, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Ingresa tu nueva contraseña.",
                    size=13,
                    color=ft.Colors.GREY_400
                ),
                self.nueva_pass,
                self.confirmar_pass,
                self.msg,
                ft.FilledButton(
                    "Guardar contraseña",
                    width=250,
                    on_click=lambda e: self.guardar(e),
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.GREEN_400,
                        color=ft.Colors.WHITE,
                        padding=15
                    )
                ),
            ]
        )
    
    def set_msg(self, texto, color=ft.Colors.RED_400):
        """Muestra un mensaje"""
        self.msg.value = texto
        self.msg.color = color
        self.page.update()
    
    def enviar(self, e):
        """Paso 1: Enviar código al email"""
        self.set_msg("")
        email = self.email_input.value.strip()
        
        if not email:
            self.set_msg("Ingresa un correo electrónico.")
            return
        
        ok, texto = self.auth_controller.enviar_codigo(email)
        if ok:
            self.email_guardado = email
            self.paso1.visible = False
            self.paso2.visible = True
            self.codigo_input.value = ""
            self.set_msg(texto, ft.Colors.GREEN_400)
        else:
            self.set_msg(texto)
    
    def reenviar(self, e):
        """Reenvía el código al mismo email"""
        self.set_msg("Reenviando código...", ft.Colors.BLUE_300)
        ok, texto = self.auth_controller.enviar_codigo(self.email_guardado)
        if ok:
            self.codigo_input.value = ""
            self.set_msg(f"Nuevo código enviado a {self.email_guardado}", ft.Colors.GREEN_400)
        else:
            self.set_msg(texto)

    def verificar(self, e):
        """Paso 2: Verificar código"""
        self.set_msg("")
        codigo = self.codigo_input.value.strip()
        
        if not codigo:
            self.set_msg("Ingresa el código de 6 dígitos.")
            return
        
        if len(codigo) != 6:
            self.set_msg("El código debe tener 6 dígitos.")
            return
        
        ok, texto = self.auth_controller.verificar_codigo(self.email_guardado, codigo)
        if ok:
            self.paso2.visible = False
            self.paso3.visible = True
            self.nueva_pass.value = ""
            self.confirmar_pass.value = ""
            self.set_msg(texto, ft.Colors.GREEN_400)
        else:
            self.set_msg(texto)
    
    def guardar(self, e):
        """Paso 3: Guardar nueva contraseña"""
        self.set_msg("", ft.Colors.RED_400)
        
        if not self.nueva_pass.value or not self.confirmar_pass.value:
            self.set_msg("Completa todos los campos.")
            return
        
        if self.nueva_pass.value != self.confirmar_pass.value:
            self.set_msg("Las contraseñas no coinciden.")
            return
        
        ok, texto = self.auth_controller.cambiar_password(
            self.email_guardado,
            self.nueva_pass.value.strip()
        )
        
        if ok:
            self.set_msg(texto, ft.Colors.GREEN_400)
            self.page.update()
            time.sleep(1.5)
            self.on_volver()
        else:
            self.set_msg(texto)
    
    def build(self):
        """Construye la vista completa"""
        return ft.Container(
            content=ft.Column(
                controls=[self.paso1, self.paso2, self.paso3],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            alignment=ft.Alignment.CENTER,
            expand=True,
            padding=30,
            border_radius=10,
            bgcolor=ft.Colors.WHITE,
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.GREY_400)
        )