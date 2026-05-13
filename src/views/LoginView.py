import flet as ft

def LoginView(page: ft.Page, auth_controller=None):
    usuario_valido = "admin@gmail.com"
    password_valido = "1234"
    
    correo = ft.TextField(
        label="Correo electrónico",
        prefix_icon=ft.Icons.PERSON,
        width=400,
        border_radius=10,
        keyboard_type=ft.KeyboardType.EMAIL
    )

    contraseña = ft.TextField(
        label="Contraseña",
        prefix_icon=ft.Icons.KEY,
        password=True,
        can_reveal_password=True,
        width=400,
        border_radius=10
    )
    
    mensaje = ft.Text("", color="red")

    def mostrar_snackbar(mensaje_texto, color=ft.Colors.GREEN):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(mensaje_texto),
            bgcolor=color,
            duration=2000,
        )
        page.snack_bar.open = True
        page.update()

    def login_click(e):
        if not correo.value or not contraseña.value:
            mensaje.value = "Por favor, llene todos los campos"
            mensaje.color = "red"
            page.update()
            return
        
        if auth_controller:
            user, msg = auth_controller.login(correo.value, contraseña.value)
            if user:
                # GUARDADO DINÁMICO: Tu método personal
                page.user_data = user
                mostrar_snackbar("¡Sesión iniciada correctamente!", ft.Colors.GREEN)
                page.go("/dashboard")
            else:
                mensaje.value = msg
                mensaje.color = "red"
                page.update()
        else:
            if correo.value == usuario_valido and contraseña.value == password_valido:
                page.user_data = {
                    "email": correo.value,
                    "nombre": "Administrador",
                    "id_usuario": 1
                }
                mostrar_snackbar("¡Sesión iniciada correctamente!", ft.Colors.GREEN)
                page.go("/dashboard")
            else:
                mensaje.value = "Correo o contraseña incorrectos"
                mensaje.color = "red"
                page.update()

    iniciar_sesion = ft.ElevatedButton(
        "Iniciar sesión",
        width=250,
        on_click=login_click,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.GREEN_400,
            color=ft.Colors.WHITE,
            padding=20,
            shape=ft.RoundedRectangleBorder(radius=12),
        ),
    )

    registro = ft.ElevatedButton(
        "Registrarme",
        width=200,
        on_click=lambda _: page.go("/registro"),
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.BLUE_600,
            color=ft.Colors.WHITE,
            padding=20,
            shape=ft.RoundedRectangleBorder(radius=12),
        ),
    )
    
    contraseña.on_submit = login_click

    return ft.View(
        route="/",
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        appbar=ft.AppBar(
            title=ft.Text("SIGE - Login"),
            bgcolor=ft.Colors.BLACK,
            color=ft.Colors.WHITE
        ),
        controls=[
            ft.Column(
                [
                    ft.Text("Acceso al Sistema", size=24, weight="bold"),
                    ft.Container(height=10),
                    correo,
                    ft.Container(height=10),
                    contraseña,
                    ft.Container(height=10),
                    mensaje,
                    ft.Container(height=10),
                    ft.TextButton(
                        "¿Olvidaste tu contraseña?",
                        on_click=lambda _: page.go("/recuperar")
                    ),
                    ft.Row(
                        [iniciar_sesion, registro],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                tight=True,
                spacing=15
            )
        ]
    )