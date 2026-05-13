import flet as ft

def RegistroView(page: ft.Page, auth_controller):
    # Campos de texto
    nombre = ft.TextField(label="Nombre Completo", prefix_icon=ft.Icons.PERSON, width=350)
    correo = ft.TextField(label="Correo electrónico", prefix_icon=ft.Icons.EMAIL, width=350)
    password = ft.TextField(
        label="Contraseña", 
        prefix_icon=ft.Icons.LOCK, 
        password=True, 
        can_reveal_password=True, 
        width=350
    )
    
    mensaje = ft.Text("", weight="bold")

    def registrar_click(e):
        if not nombre.value or not correo.value or not password.value:
            mensaje.value = "Todos los campos son obligatorios"
            mensaje.color = "red"
            page.update()
            return

        success, msg = auth_controller.registrar_usuario(nombre.value, correo.value, password.value)
        if success:
            page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor="green")
            page.snack_bar.open = True
            page.go("/") 
        else:
            mensaje.value = msg
            mensaje.color = "red"
            page.update()

   
    content = ft.Column(
        [
            ft.Icon(ft.Icons.PERSON_ADD_ROUNDED, size=50, color=ft.Colors.BLUE_600),
            ft.Text("Registro de Usuario", size=24, weight="bold"),
            nombre,
            correo,
            password,
            mensaje,
            ft.ElevatedButton(
                "Registrarme", 
                on_click=registrar_click, 
                width=250, 
                bgcolor=ft.Colors.BLUE_600, 
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
        controls=[
            ft.AppBar(
                title=ft.Text("Crear Cuenta"), 
                bgcolor=ft.Colors.BLACK, 
                color=ft.Colors.WHITE
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