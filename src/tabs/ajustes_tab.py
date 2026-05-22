import flet as ft

def ajustes_tab(on_logout):
    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Configuración", size=25, weight="bold"),
                ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                
                # Sección de cuenta
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Text("Cuenta", size=18, weight="bold"),
                                ft.Divider(),
                                ft.ListTile(
                                    leading=ft.Icon(ft.Icons.PERSON),
                                    title=ft.Text("Editar Perfil"),
                                    subtitle=ft.Text("Cambia tu nombre de usuario")
                                ),
                                ft.ListTile(
                                    leading=ft.Icon(ft.Icons.EMAIL),
                                    title=ft.Text("Cambiar Email"),
                                    subtitle=ft.Text("Actualiza tu correo electrónico")
                                ),
                                ft.ListTile(
                                    leading=ft.Icon(ft.Icons.LOCK),
                                    title=ft.Text("Cambiar Contraseña"),
                                    subtitle=ft.Text("Actualiza tu contraseña")
                                ),
                            ]
                        ),
                        padding=15
                    )
                ),
                
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                
                # Sección de juego
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Text("Juego", size=18, weight="bold"),
                                ft.Divider(),
                                ft.ListTile(
                                    leading=ft.Icon(ft.Icons.VOLUME_UP),
                                    title=ft.Text("Sonido"),
                                    subtitle=ft.Text("Activar/Desactivar efectos de sonido"),
                                    trailing=ft.Switch(value=True)
                                ),
                                ft.ListTile(
                                    leading=ft.Icon(ft.Icons.DARK_MODE),
                                    title=ft.Text("Tema Oscuro"),
                                    subtitle=ft.Text("Cambiar apariencia del juego"),
                                    trailing=ft.Switch(value=False)
                                ),
                            ]
                        ),
                        padding=15
                    )
                ),
                
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                
                # Botón de cerrar sesión
                ft.ElevatedButton(
                    "Cerrar Sesión",
                    icon=ft.Icons.LOGOUT,
                    on_click=lambda e: on_logout(),
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.RED_700,
                        color=ft.Colors.WHITE,
                        padding=15
                    )
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=5,
            scroll=ft.ScrollMode.AUTO
        ),
        alignment=ft.Alignment.TOP_CENTER,
        expand=True,
        padding=10
    )