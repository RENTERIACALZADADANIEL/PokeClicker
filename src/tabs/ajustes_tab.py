import flet as ft

def ajustes_tab(on_logout):
    return ft.Column([
        ft.Text("Configuración", size=25, weight="bold"),
        ft.ElevatedButton("Cerrar Sesión", icon=ft.icons.LOGOUT, on_click=on_logout, color="red")
    ])