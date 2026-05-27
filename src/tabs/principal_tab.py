import flet as ft

def principal_tab(clicks_actuales=0, clicks_totales=0, cantidad_rebirths=0, 
                  costo_rebirth=100, multiplicador=1.0, puede_rebirth=False,
                  boost_activo=False, boost_tiempo_restante=0, boost_info=None,
                  on_click=None, on_rebirth=None):
    """
    Pestaña principal del juego
    
    Args:
        clicks_actuales: Clicks actuales del jugador
        clicks_totales: Total de clicks históricos
        cantidad_rebirths: Número de rebirths realizados
        costo_rebirth: Costo del siguiente rebirth
        multiplicador: Multiplicador activo total
        puede_rebirth: Si puede hacer rebirth ahora
        boost_activo: Si hay algún boost activo
        boost_tiempo_restante: Tiempo restante del boost más largo
        boost_info: Info detallada de boosts {"rebirth_boost_active", "rebirth_boost_time", "tienda_boost_active", "tienda_boost_time", "total_multiplier"}
        on_click: Función a llamar al hacer click
        on_rebirth: Función a llamar al hacer rebirth
    """
    
    if boost_info is None:
        boost_info = {}
    
    # Formatear números grandes
    def format_number(num):
        if num >= 1_000_000:
            return f"{num/1_000_000:.1f}M"
        elif num >= 1_000:
            return f"{num/1_000:.1f}K"
        return f"{num:,}"
    
    # Formatear tiempo
    def format_time(seconds):
        if seconds <= 0:
            return "0:00"
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes}:{secs:02d}"
    
    # Color del botón según boost
    btn_color = ft.Colors.ORANGE_700 if boost_activo else ft.Colors.YELLOW_700
    clicks_por_click = int(1 * multiplicador)
    
    # Construir elementos de la UI
    stats_elements = [
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
    ]
    
    # Mostrar multiplicador si es mayor a 1
    if multiplicador > 1.0:
        stats_elements.append(
            ft.Text(
                f"x{multiplicador:.2f}",
                size=14,
                color=ft.Colors.GREEN_700,
                weight=ft.FontWeight.BOLD
            )
        )
    
    # Información de boosts activos
    rebirth_active = boost_info.get('rebirth_boost_active', False)
    tienda_active = boost_info.get('tienda_boost_active', False)
    
    if rebirth_active or tienda_active:
        boost_details = []
        
        if rebirth_active:
            rb_time = boost_info.get('rebirth_boost_time', 0)
            boost_details.append(
                ft.Row(
                    [
                        ft.Text("🔄", size=14),
                        ft.Text(f"Rebirth x1.25", size=12, color=ft.Colors.ORANGE_700),
                        ft.Text(f"{format_time(rb_time)}", size=12, color=ft.Colors.ORANGE_500),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=5
                )
            )
        
        if tienda_active:
            td_time = boost_info.get('tienda_boost_time', 0)
            boost_details.append(
                ft.Row(
                    [
                        ft.Text("⚡", size=14),
                        ft.Text(f"Tienda x2", size=12, color=ft.Colors.ORANGE_700),
                        ft.Text(f"{format_time(td_time)}", size=12, color=ft.Colors.ORANGE_500),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=5
                )
            )
        
        stats_elements.append(
            ft.Container(
                content=ft.Column(boost_details, spacing=3, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=ft.padding.only(top=5)
            )
        )
        
        # Barra de progreso del boost más largo
        if boost_tiempo_restante > 0:
            max_time = max(boost_info.get('rebirth_boost_time', 0), boost_info.get('tienda_boost_time', 0))
            stats_elements.append(
                ft.ProgressBar(
                    value=min(1.0, boost_tiempo_restante / 600),  # 10 minutos máximo
                    width=250,
                    color=ft.Colors.ORANGE_400,
                    bgcolor=ft.Colors.ORANGE_100
                )
            )
    
    # Info de rebirths
    stats_elements.append(
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
        )
    )
    
    # Mensaje de rebirth disponible
    if puede_rebirth:
        stats_elements.append(
            ft.Text(
                "🌟 ¡Rebirth disponible!",
                size=13,
                color=ft.Colors.ORANGE_700,
                weight=ft.FontWeight.BOLD
            )
        )
    
    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Área de Entrenamiento", size=20, weight="bold"),
                
                # Tarjeta de estadísticas
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            stats_elements,
                            spacing=5,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        padding=10
                    ),
                    width=350
                ),
                
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                
                # Pokémon
                ft.Image(
                    src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png",
                    width=120,
                    height=120
                ),
                
                # Botón de click
                ft.TextButton(
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
                
                ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
                
                # Botón de rebirth
                ft.TextButton(
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
            scroll=ft.ScrollMode.AUTO
        ),
        alignment=ft.Alignment.CENTER,
        expand=True
    )