import flet as ft
from tabs.principal_tab import principal_tab
from tabs.tienda_tab import tienda_tab
from tabs.inventario_tab import ajustes_tab

class DashboardView(ft.View):
    def __init__(self, username: str, on_logout):
        super().__init__(route="/dashboard")
        self.username = username
        self.on_logout = on_logout
        
        # Contenedor dinámico para el cuerpo de la página
        self.contenido_pagina = ft.Container(
            content=principal_tab(), 
            expand=True,
            padding=20
        )

        # Barra de navegación inferior con 3 pestañas
        self.navigation_bar = ft.NavigationBar(
            selected_index=0,
            destinations=[
                ft.NavigationBarDestination(
                    icon=ft.Icons.HOME_OUTLINED,
                    selected_icon=ft.Icons.HOME,
                    label="Principal"
                ),
                ft.NavigationBarDestination(
                    icon=ft.Icons.SHOPPING_CART_OUTLINED,
                    selected_icon=ft.Icons.SHOPPING_CART,
                    label="Tienda"
                ),
                ft.NavigationBarDestination(
                    icon=ft.Icons.SETTINGS_OUTLINED,
                    selected_icon=ft.Icons.SETTINGS,
                    label="Ajustes"
                ),
            ],
            on_change=self.cambiar_tab,
            bgcolor=ft.Colors.WHITE,
            indicator_color=ft.Colors.RED_100
        )
        
        # AppBar con información del usuario
        self.appbar = ft.AppBar(
            leading=ft.Icon(ft.Icons.CATCHING_POKEMON),
            leading_width=40,
            title=ft.Text(
                f"Poke Clicker - {self.username}", 
                weight=ft.FontWeight.BOLD
            ),
            center_title=False,
            bgcolor=ft.Colors.RED_700,
            color=ft.Colors.WHITE,
            actions=[
                ft.IconButton(
                    icon=ft.Icons.LOGOUT,
                    tooltip="Cerrar sesión",
                    on_click=lambda e: self.confirmar_logout()
                )
            ]
        )
        
        # Estructura principal: AppBar + Contenido + NavigationBar
        self.controls = [
            self.appbar,
            self.contenido_pagina,
            self.navigation_bar
        ]
        
        # Configuración adicional de la vista
        self.padding = 0
        self.spacing = 0
        self.vertical_alignment = ft.MainAxisAlignment.START
        self.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    
    def cambiar_tab(self, e):
        """Cambia entre las 3 pestañas"""
        opcion = e.control.selected_index
        
        if opcion == 0:
            self.contenido_pagina.content = principal_tab()
            self.appbar.bgcolor = ft.Colors.RED_700
            self.appbar.title = ft.Text(
                f"Poke Clicker - {self.username}", 
                weight=ft.FontWeight.BOLD
            )
        elif opcion == 1:
            self.contenido_pagina.content = tienda_tab()
            self.appbar.bgcolor = ft.Colors.BLUE_700
            self.appbar.title = ft.Text("Tienda Pokémon", weight=ft.FontWeight.BOLD)
        elif opcion == 2:
            self.contenido_pagina.content = ajustes_tab(self.on_logout)
            self.appbar.bgcolor = ft.Colors.GREEN_700
            self.appbar.title = ft.Text("Ajustes", weight=ft.FontWeight.BOLD)
        
        self.update()
    
    def confirmar_logout(self):
        """Muestra diálogo de confirmación para cerrar sesión"""
        def cerrar_sesion(e):
            self.page.close(dialog)
            self.on_logout()
        
        def cancelar(e):
            self.page.close(dialog)
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Cerrar Sesión"),
            content=ft.Text("¿Estás seguro de que deseas cerrar sesión?"),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar),
                ft.ElevatedButton(
                    "Cerrar Sesión",
                    on_click=cerrar_sesion,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.RED_700,
                        color=ft.Colors.WHITE
                    )
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        self.page.show_dialog(dialog)