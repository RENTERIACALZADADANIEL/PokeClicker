import flet as ft

def principal_tab():
    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Área de Entrenamiento", size=25, weight="bold"),
                ft.Image(
                    src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png",
                    width=200,
                    height=200
                ),
                ft.ElevatedButton("¡Click!", on_click=lambda _: print("Clic!"))
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        ),
        alignment=ft.Alignment.CENTER,
        expand=True
    )