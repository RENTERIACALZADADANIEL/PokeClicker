import flet as ft
from views.recuperarView import RecuperarView

def LoginView(page: ft.Page, auth_controller=None):
    correo = ft.TextField(
        label="Correo de Entrenador",
        prefix_icon=ft.Icons.EMAIL,
        width=400,
        border_radius=10,
        keyboard_type=ft.KeyboardType.EMAIL,
        border_color=ft.Colors.RED_400,
        focused_border_color=ft.Colors.RED_700,
        label_style=ft.TextStyle(color=ft.Colors.RED_400)
    )

    contraseña = ft.TextField(
        label="Contraseña Pokémon",
        prefix_icon=ft.Icons.LOCK,
        password=True,
        can_reveal_password=True,
        width=400,
        border_radius=10,
        border_color=ft.Colors.RED_400,
        focused_border_color=ft.Colors.RED_700,
        label_style=ft.TextStyle(color=ft.Colors.RED_400)
    )
    
    mensaje = ft.Text("", color=ft.Colors.RED_700)

    def mostrar_snackbar(mensaje_texto, color=ft.Colors.RED_700):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(mensaje_texto),
            bgcolor=color,
            duration=2000,
        )
        page.snack_bar.open = True
        page.update()

    def login_click(e):
        if not correo.value or not contraseña.value:
            mensaje.value = "¡Completa todos los campos entrenador!"
            mensaje.color = ft.Colors.RED_700
            page.update()
            return

        if not auth_controller:
            mensaje.value = "Error: no hay conexión con la base de datos"
            mensaje.color = ft.Colors.RED_700
            page.update()
            return

        user, msg = auth_controller.login(correo.value, contraseña.value)
        if user:
            page.user_data = user
            mostrar_snackbar("¡Bienvenido al mundo Pokémon!", ft.Colors.RED_700)
            page.go("/home")
        else:
            mensaje.value = msg
            mensaje.color = ft.Colors.RED_700
            page.update()

    iniciar_sesion = ft.ElevatedButton(
        "¡Iniciar Aventura!",
        width=250,
        on_click=login_click,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.RED_700,
            color=ft.Colors.WHITE,
            padding=20,
            shape=ft.RoundedRectangleBorder(radius=12),
        ),
    )

    registro = ft.ElevatedButton(
        "¡Registrar Entrenador!",
        width=200,
        on_click=lambda _: page.go("/registro"),
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.RED_900,
            color=ft.Colors.WHITE,
            padding=20,
            shape=ft.RoundedRectangleBorder(radius=12),
        ),
    )
    
    contraseña.on_submit = login_click

    # Recuperar contraseña (inline, sin nueva ruta) 
    recuperar_container = ft.Container(visible=False, expand=True)
    login_column = ft.Column(
        [
            ft.Icon(ft.Icons.CATCHING_POKEMON, size=80, color=ft.Colors.RED_700),
            ft.Text("¡Bienvenido Entrenador!", size=28, weight="bold", color=ft.Colors.RED_900),
            ft.Text("Inicia sesión para atrapar clicks", size=16, color=ft.Colors.RED_600),
            ft.Container(height=20),
            correo,
            ft.Container(height=10),
            contraseña,
            ft.Container(height=10),
            mensaje,
            ft.Container(height=10),
            ft.Row(
                [iniciar_sesion, registro],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.TextButton(
                "¿Olvidaste tu contraseña?",
                on_click=lambda _: mostrar_recuperar(),
                style=ft.ButtonStyle(color=ft.Colors.RED_400)
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        tight=True,
        spacing=15
    )

    def mostrar_recuperar():
        vista_rec = RecuperarView(
            page,
            auth_controller,
            on_volver=lambda: (
                setattr(login_column, 'visible', True),
                setattr(recuperar_container, 'visible', False),
                setattr(recuperar_container, 'content', None),
                page.update()
            )
        )
        recuperar_container.content = vista_rec.build()
        recuperar_container.visible = True
        login_column.visible = False
        page.update()

    return ft.View(
        route="/",
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=ft.Colors.RED_50,
        appbar=ft.AppBar(
            title=ft.Text("Pokémon Clicker - Liga Pokémon", color=ft.Colors.WHITE),
            bgcolor=ft.Colors.RED_800,
            center_title=True,
            automatically_imply_leading=False
        ),
        controls=[
            ft.Stack([login_column, recuperar_container], expand=True)
        ]
    )
