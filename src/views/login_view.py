import flet as ft
from controllers.auth_controller import AuthController

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
        # Guardar referencia al contenedor para poder usarlo después
        self.login_container = ft.Container(
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
                        on_click=lambda e: self.mostrar_recuperar(),
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
        return self.login_container
    
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
            self.page.update()
    
    def mostrar_recuperar(self):
        """Muestra la vista de recuperación de contraseña"""
        from views.recuperar_view import RecuperarView
        
        def volver_al_login():
            # Restaurar el login
            self.page.controls.clear()
            self.page.add(self.build())
            self.page.update()
        
        recuperar_view = RecuperarView(
            page=self.page,
            auth_controller=self.auth_controller,
            on_volver=volver_al_login
        )
        
        # Limpiar la página y mostrar la vista de recuperación
        self.page.controls.clear()
        self.page.add(recuperar_view.build())
        self.page.update()