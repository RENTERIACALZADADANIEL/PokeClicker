import flet as ft

def principal_tab(clicks_actuales=0, clicks_totales=0, cantidad_rebirths=0, 
                  costo_rebirth=100, multiplicador=1.0, puede_rebirth=False,
                  boost_activo=False, boost_tiempo_restante=0,
                  on_click=None, on_rebirth=None):
    
    # Formatear números grandes
    def format_number(num):
        if num >= 1_000_000:
            return f"{num/1_000_000:.1f}M"
        elif num >= 1_000:
            return f"{num/1_000:.1f}K"
        return f"{num:,}"
    
    # Formatear tiempo del boost
    def format_time(seconds):
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes}:{secs:02d}"
    
    # Color del botón según boost
    btn_color = ft.Colors.ORANGE_700 if boost_activo else ft.Colors.YELLOW_700
    clicks_por_click = int(1 * multiplicador)
    
    return ft.Container(
        content=ft.Column(
            [
                # Título compacto
                ft.Text("Área de Entrenamiento", size=20, weight="bold"),
                
                # Tarjeta de estadísticas (compacta)
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                # Fila de clicks
                                ft.Row(
                                    [
                                        ft.Text(
                                            f"⚡ {format_number(clicks_actuales)}",
                                            size=18,
                                            weight=ft.FontWeight.BOLD
                                        ),
                                        ft.Text(
                                            f"| Total: {format_number(clicks_totales)}",
                                            size=12,
                                            color=ft.Colors.GREY_600
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=10
                                ),
                                
                                # Multiplicador
                                ft.Text(
                                    f"x{multiplicador:.2f}" if multiplicador > 1.0 else "",
                                    size=14,
                                    color=ft.Colors.GREEN_700,
                                    weight=ft.FontWeight.BOLD
                                ),
                                
                                # Boost activo
                                ft.Column(
                                    [
                                        ft.ProgressBar(
                                            value=boost_tiempo_restante / 300,
                                            width=250,
                                            color=ft.Colors.ORANGE_400,
                                            bgcolor=ft.Colors.ORANGE_100
                                        ),
                                        ft.Text(
                                            f"🔥 Boost: {format_time(boost_tiempo_restante)}",
                                            size=12,
                                            color=ft.Colors.ORANGE_700
                                        ),
                                    ],
                                    spacing=2,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    visible=boost_activo
                                ),
                                
                                # Rebirth info
                                ft.Row(
                                    [
                                        ft.Text(
                                            f"💎 Rebirths: {cantidad_rebirths}",
                                            size=12,
                                            color=ft.Colors.GREY_700
                                        ),
                                        ft.Text(
                                            f"| Costo: {format_number(costo_rebirth)}",
                                            size=12,
                                            color=ft.Colors.GREY_700
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=10
                                ),
                                
                                # Rebirth disponible
                                ft.Text(
                                    "🌟 ¡Rebirth disponible!",
                                    size=13,
                                    color=ft.Colors.ORANGE_700,
                                    weight=ft.FontWeight.BOLD,
                                    visible=puede_rebirth
                                ),
                            ],
                            spacing=5,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        padding=10
                    ),
                    width=350
                ),
                
                # Espacio pequeño
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                
                # Pokémon (más pequeño)
                ft.Image(
                    src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png",
                    width=120,
                    height=120
                ),
                
                # Botón de click (GRANDE y visible)
                ft.ElevatedButton(
                    f"⚡ ¡Click! (+{clicks_por_click}) ⚡",
                    on_click=lambda e: on_click() if on_click else None,
                    style=ft.ButtonStyle(
                        bgcolor=btn_color,
                        color=ft.Colors.BLACK,
                        padding=15,
                        shape=ft.RoundedRectangleBorder(radius=10),
                        text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD)
                    ),
                    width=250,
                    height=50
                ),
                
                # Espacio pequeño
                ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
                
                # Botón de rebirth
                ft.ElevatedButton(
                    "🔄 Rebirth",
                    on_click=lambda e: on_rebirth() if on_rebirth else None,
                    disabled=not puede_rebirth,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.PURPLE_700 if puede_rebirth else ft.Colors.GREY_400,
                        color=ft.Colors.WHITE,
                        padding=10,
                        shape=ft.RoundedRectangleBorder(radius=8)
                    ),
                    width=180,
                    height=40
                ),
                
                # Texto explicativo
                ft.Text(
                    "Gasta clicks → Boost x1.25 (5 min)",
                    size=11,
                    color=ft.Colors.GREY_500,
                    text_align=ft.TextAlign.CENTER
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
            scroll=ft.ScrollMode.AUTO  # Scroll por si no cabe
        ),
        alignment=ft.Alignment.CENTER,
        expand=True
    )