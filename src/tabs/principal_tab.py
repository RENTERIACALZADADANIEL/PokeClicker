import flet as ft

def principal_tab(clicks_actuales=0, clicks_totales=0, cantidad_rebirths=0, 
                  costo_rebirth=100, multiplicador=1.0, puede_rebirth=False,
                  on_click=None, on_rebirth=None):
    """
    Pestaña principal del juego
    
    Args:
        clicks_actuales: Clicks actuales del jugador
        clicks_totales: Total de clicks históricos
        cantidad_rebirths: Número de rebirths realizados
        costo_rebirth: Costo del siguiente rebirth
        multiplicador: Multiplicador activo
        puede_rebirth: Si puede hacer rebirth ahora
        on_click: Función a llamar al hacer click
        on_rebirth: Función a llamar al hacer rebirth
    """
    
    # Formatear números grandes
    def format_number(num):
        if num >= 1_000_000:
            return f"{num/1_000_000:.1f}M"
        elif num >= 1_000:
            return f"{num/1_000:.1f}K"
        return str(num)
    
    # Texto de estadísticas
    stats_text = ft.Text(
        f"Clicks: {format_number(clicks_actuales)} | "
        f"Totales: {format_number(clicks_totales)} | "
        f"x{multiplicador:.1f}",
        size=16,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER
    )
    
    rebirth_text = ft.Text(
        f"Rebirths: {cantidad_rebirths} | "
        f"Costo rebirth: {format_number(costo_rebirth)}",
        size=14,
        color=ft.Colors.GREY_700,
        text_align=ft.TextAlign.CENTER
    )
    
    # Mensaje de rebirth disponible
    rebirth_available = ft.Text(
        "🌟 ¡Rebirth disponible!",
        size=16,
        color=ft.Colors.ORANGE_700,
        weight=ft.FontWeight.BOLD,
        visible=puede_rebirth
    )
    
    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Área de Entrenamiento", size=25, weight="bold"),
                
                # Estadísticas
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                stats_text,
                                rebirth_text,
                                rebirth_available,
                            ],
                            spacing=5,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        padding=15
                    ),
                    width=350
                ),
                
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                
                # Pokémon y botón de click
                ft.Image(
                    src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png",
                    width=200,
                    height=200
                ),
                
                ft.Text(
                    "¡Haz click en Pikachu!",
                    size=14,
                    color=ft.Colors.GREY_600,
                    italic=True
                ),
                
                ft.ElevatedButton(
                    "⚡ ¡Click! ⚡",
                    on_click=lambda e: on_click() if on_click else None,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.YELLOW_700,
                        color=ft.Colors.BLACK,
                        padding=20,
                        shape=ft.RoundedRectangleBorder(radius=10),
                        text_style=ft.TextStyle(size=20, weight=ft.FontWeight.BOLD)
                    ),
                    width=200,
                    height=60
                ),
                
                ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                
                # Botón de rebirth
                ft.ElevatedButton(
                    "🔄 Rebirth",
                    on_click=lambda e: on_rebirth() if on_rebirth else None,
                    disabled=not puede_rebirth,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.PURPLE_700 if puede_rebirth else ft.Colors.GREY_400,
                        color=ft.Colors.WHITE,
                        padding=15,
                        shape=ft.RoundedRectangleBorder(radius=8)
                    ),
                    width=200
                ),
                
                ft.Text(
                    f"Reinicia tus clicks pero ganas x{(multiplicador + 0.1):.1f} multiplicador",
                    size=12,
                    color=ft.Colors.GREY_500,
                    text_align=ft.TextAlign.CENTER,
                    visible=puede_rebirth
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        ),
        alignment=ft.Alignment.CENTER,
        expand=True
    )