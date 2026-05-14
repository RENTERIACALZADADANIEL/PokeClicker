import flet as ft
from tabs.principal_tab import principal_tab
from tabs.tienda_tab import tienda_tab
from tabs.ajustes_tab import ajustes_tab

class DashboardView(ft.View):
    def __init__(self, page, on_logout):
        super().__init__(route="/dashboard")
        self.page = page
        self.on_logout = on_logout
        
        # Contenedor dinámico para el cuerpo de la página
        self.container = ft.Container(content=principal_tab(), expand=True)

        self.navigation_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationDestination(icon=ft.icons.HOME, label="Principal"),
                ft.NavigationDestination(icon=ft.icons.SHOPPING_CART, label="Tienda"),
                ft.NavigationDestination(icon=ft.icons.SETTINGS, label="Ajustes"),
            ],
            on_change=self.cambiar_tab
        )
        
        self.controls = [
            ft.AppBar(title=ft.Text(f"Poke Clicker - {self.page.session.get('username')}"), bgcolor="red", color="white"),
            self.container,
            self.navigation_bar
        ]

    def cambiar_tab(self, e):
        opcion = e.control.selected_index
        if opcion == 0:
            self.container.content = principal_tab()
        elif opcion == 1:
            self.container.content = tienda_tab()
        elif opcion == 2:
            self.container.content = ajustes_tab(self.on_logout)
        
        self.page.update()