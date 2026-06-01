import flet as ft

def RegistroView(page: ft.Page, auth_controller):
    nombre = ft.TextField(
        label="Nombre de Entrenador", 
        prefix_icon=ft.Icons.PERSON, 
        width=350,
        border_color=ft.Colors.RED_400,
        focused_border_color=ft.Colors.RED_700,
        label_style=ft.TextStyle(color=ft.Colors.RED_400)
    )
    correo = ft.TextField(
        label="Correo electrónico", 
        prefix_icon=ft.Icons.EMAIL, 
        width=350,
        border_color=ft.Colors.RED_400,
        focused_border_color=ft.Colors.RED_700,
        label_style=ft.TextStyle(color=ft.Colors.RED_400)
    )
    password = ft.TextField(
        label="Contraseña", 
        prefix_icon=ft.Icons.LOCK, 
        password=True, 
        can_reveal_password=True, 
        width=350,
        border_color=ft.Colors.RED_400,
        focused_border_color=ft.Colors.RED_700,
        label_style=ft.TextStyle(color=ft.Colors.RED_400)
    )
    
    mensaje = ft.Text("", weight="bold", color=ft.Colors.RED_700)

    def registrar_click(e):
        if not nombre.value or not correo.value or not password.value:
            mensaje.value = "¡Todos los campos son obligatorios entrenador!"
            mensaje.color = ft.Colors.RED_700
            page.update()
            return

        success, msg = auth_controller.registrar_usuario(nombre.value, correo.value, password.value)
        if success:
            page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor=ft.Colors.RED_700)
            page.snack_bar.open = True
            page.go("/") 
        else:
            mensaje.value = msg
            mensaje.color = ft.Colors.RED_700
            page.update()

    content = ft.Column(
        [
            ft.Icon(ft.Icons.CATCHING_POKEMON, size=50, color=ft.Colors.RED_700),
            ft.Text("Registro de Entrenador", size=24, weight="bold", color=ft.Colors.RED_800),
            nombre,
            correo,
            password,
            mensaje,
            ft.ElevatedButton(
                "¡Registrarme!", 
                on_click=registrar_click, 
                width=250, 
                bgcolor=ft.Colors.RED_700, 
                color="white",
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
            ),
            ft.TextButton("Volver al Login", on_click=lambda _: page.go("/"))
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
    )

    return ft.View(
        route="/registro",
        bgcolor=ft.Colors.RED_50,
        controls=[
            ft.AppBar(
                title=ft.Text("Crear Cuenta de Entrenador", color=ft.Colors.WHITE), 
                bgcolor=ft.Colors.RED_800, 
                center_title=True
            ),
            ft.Container(
                content=content,
                alignment=ft.Alignment.CENTER,
                expand=True
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )