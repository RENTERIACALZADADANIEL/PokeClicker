import flet as ft

def tienda_tab():
    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Tienda Pokémon", size=25, weight="bold"),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.ListTile(
                                    leading=ft.Icon(ft.Icons.BOLT),
                                    title=ft.Text("Poción de Clics"),
                                    subtitle=ft.Text("Costo: 10 Rebirths")
                                ),
                                ft.Row(
                                    [ft.TextButton("Comprar")],
                                    alignment=ft.MainAxisAlignment.END
                                )
                            ]
                        ),
                        padding=10
                    )
                ),
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.ListTile(
                                    leading=ft.Icon(ft.Icons.CATCHING_POKEMON),
                                    title=ft.Text("Poké Ball"),
                                    subtitle=ft.Text("Costo: 5 Rebirths")
                                ),
                                ft.Row(
                                    [ft.TextButton("Comprar")],
                                    alignment=ft.MainAxisAlignment.END
                                )
                            ]
                        ),
                        padding=10
                    )
                ),
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.ListTile(
                                    leading=ft.Icon(ft.Icons.STAR),
                                    title=ft.Text("Piedra Evolutiva"),
                                    subtitle=ft.Text("Costo: 20 Rebirths")
                                ),
                                ft.Row(
                                    [ft.TextButton("Comprar")],
                                    alignment=ft.MainAxisAlignment.END
                                )
                            ]
                        ),
                        padding=10
                    )
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
            scroll=ft.ScrollMode.AUTO
        ),
        alignment=ft.Alignment.TOP_CENTER,
        expand=True
    )