import flet as ft

def DashboardView(page, progreso_controller):
    user = getattr(page, "user_data", None)
    
    if not user:
        page.go("/")
        return ft.View(route="/dashboard", controls=[ft.Text("Redirigiendo...")])
    
    # Obtener progreso inicial
    progreso = progreso_controller.obtener_progreso(user['id_usuario'])
    
    # Controles del juego
    txt_clicks = ft.Text(f"{progreso['clicks_actuales']:,}", size=40, weight="bold", color=ft.Colors.RED_700)
    txt_total = ft.Text(f"Total: {progreso['clicks_totales']:,}", size=16, color=ft.Colors.RED_500)
    txt_rebirths = ft.Text(f"Nivel Entrenador: {progreso['cantidad_rebirths']}", size=18, color=ft.Colors.RED_600)
    txt_costo_rebirth = ft.Text(f"Costo renacer: {progreso['costo_siguiente_rebirth']:,} clicks", size=14)
    
    def update_display():
        p = progreso_controller.obtener_progreso(user['id_usuario'])
        txt_clicks.value = f"{p['clicks_actuales']:,}"
        txt_total.value = f"Total: {p['clicks_totales']:,}"
        txt_rebirths.value = f"Nivel Entrenador: {p['cantidad_rebirths']}"
        txt_costo_rebirth.value = f"Costo renacer: {p['costo_siguiente_rebirth']:,} clicks"
        page.update()
    
    def on_click_pokemon(e):
        progreso_controller.agregar_clicks(user['id_usuario'])
        update_display()
        
        # Animación de feedback visual
        e.control.scale = 0.95
        page.update()
        import time
        time.sleep(0.05)
        e.control.scale = 1
        page.update()
    
    def on_rebirth(e):
        success, msg = progreso_controller.realizar_rebirth(user['id_usuario'])
        if success:
            page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor=ft.Colors.RED_700)
            page.snack_bar.open = True
            update_display()
        else:
            page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor=ft.Colors.RED_900)
            page.snack_bar.open = True
        page.update()
    
    # Pantalla principal de juego
    vista_juego = ft.Column([
        ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.CATCHING_POKEMON, size=60, color=ft.Colors.RED_700),
                ft.Text("¡Pokémon Clicker!", size=32, weight="bold", color=ft.Colors.RED_800),
                ft.Container(height=20),
                txt_clicks,
                txt_total,
                ft.Container(height=10),
                txt_rebirths,
                txt_costo_rebirth,
                ft.Container(height=30),
                ft.GestureDetector(
                    content=ft.Container(
                        content=ft.Icon(ft.Icons.QUESTION_ANSWER, size=100, color=ft.Colors.RED_700),
                        width=200,
                        height=200,
                        bgcolor=ft.Colors.RED_100,
                        border_radius=100,
                        alignment=ft.alignment.center
                    ),
                    on_tap=on_click_pokemon
                ),
                ft.Text("¡Toca el Pokémon!", size=16, italic=True, color=ft.Colors.RED_600),
                ft.Container(height=20),
                ft.ElevatedButton(
                    " Renacer ✨",
                    on_click=on_rebirth,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.RED_700,
                        color=ft.Colors.WHITE
                    )
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
            padding=30,
            expand=True
        )
    ], expand=True, visible=True)
    
    # Pantalla de perfil (adaptada)
    vista_perfil = ft.Column([
        ft.Container(
            content=ft.Column([
                ft.CircleAvatar(
                    content=ft.Icon(ft.Icons.CATCHING_POKEMON, size=50),
                    radius=50,
                    bgcolor=ft.Colors.RED_200
                ),
                ft.Text(user.get('username', 'Entrenador'), size=28, weight="bold", color=ft.Colors.RED_800),
                ft.Text(user.get('email', 'entrenador@pokemon.com'), size=16, color=ft.Colors.RED_600),
                ft.Divider(height=30, color=ft.Colors.RED_300),
                ft.Text("Estadísticas de Entrenador:", size=20, weight="bold", color=ft.Colors.RED_700),
                ft.Text(f"📊 Nivel: {progreso['cantidad_rebirths'] + 1}", size=16),
                ft.Text(f" Clicks totales: {progreso['clicks_totales']:,}", size=16),
                ft.Text(f" Racha actual: {progreso['clicks_actuales']:,}", size=16),
                ft.Divider(height=20),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.LOGOUT, color=ft.Colors.RED),
                    title=ft.Text("Cerrar Sesión", color=ft.Colors.RED, weight="bold"),
                    on_click=lambda _: page.go("/")
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20
        )
    ], expand=True, visible=False)
    
    def cambiar_pestana(e):
        idx = e.control.selected_index
        vista_juego.visible = (idx == 0)
        vista_perfil.visible = (idx == 1)
        
        if idx == 0:
            update_display()
        page.update()
    
    nav_bar = ft.NavigationBar(
        selected_index=0,
        on_change=cambiar_pestana,
        bgcolor=ft.Colors.RED_100,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.CATCHING_POKEMON, selected_icon=ft.Icons.CATCHING_POKEMON, label="Juego"),
            ft.NavigationBarDestination(icon=ft.Icons.PERSON, selected_icon=ft.Icons.PERSON, label="Perfil"),
        ],
    )
    
    return ft.View(
        route="/dashboard",
        navigation_bar=nav_bar,
        bgcolor=ft.Colors.RED_50,
        controls=[
            ft.AppBar(
                title=ft.Text("Pokémon Clicker", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.RED_800,
                center_title=True
            ),
            ft.Stack([
                vista_juego,
                vista_perfil
            ])
        ]
    )