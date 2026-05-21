import flet as ft

def tienda_tab():
    return ft.Column([
        ft.Text("Tienda Pokémon", size=25, weight="bold"),
        ft.ListTile(leading=ft.Icon(ft.Icons.BOLT), title=ft.Text("Pocion de Clics"), subtitle=ft.Text("Costo: 10 Rebirths"))
    ])
