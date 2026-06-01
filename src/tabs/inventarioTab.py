import flet as ft

def inventario_tab(inventory_items=None, on_use_boost=None):
    """
    Pestaña de Inventario
    
    Args:
        inventory_items: Lista de items del inventario
        on_use_boost: Función para usar un boost
    """
    if inventory_items is None:
        inventory_items = []
    
    # Separar items por tipo
    pokemons = [item for item in inventory_items if item.tipo == 'pokemon']
    boosts = [item for item in inventory_items if item.tipo == 'boost']
    
    items_list = []
    
    # Sección de Pokémon
    if pokemons:
        items_list.append(
            ft.Text(f" Tus Pokémon ({len(pokemons)})", size=18, weight=ft.FontWeight.BOLD)
        )
        for pkm in pokemons:
            items_list.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Row(
                            [
                                ft.Image(
                                    src=f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pkm.item_id}.png",
                                    width=60,
                                    height=60
                                ),
                                ft.Column(
                                    [
                                        ft.Text(pkm.nombre, weight=ft.FontWeight.BOLD),
                                        ft.Text(f"Cantidad: {pkm.cantidad}", size=12, color=ft.Colors.GREY_600),
                                    ],
                                    spacing=2
                                ),
                            ],
                            spacing=15
                        ),
                        padding=10
                    )
                )
            )
    
    # Sección de Boosts
    if boosts:
        if pokemons:
            items_list.append(ft.Divider(height=10, color=ft.Colors.TRANSPARENT))
        
        items_list.append(
            ft.Text(f"⚡ Tus Boosts ({sum(b.cantidad for b in boosts)})", size=18, weight=ft.FontWeight.BOLD)
        )
        
        for boost in boosts:
            items_list.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Row(
                            [
                                ft.Icon(ft.Icons.BOLT, color=ft.Colors.ORANGE_700, size=40),
                                ft.Column(
                                    [
                                        ft.Text(boost.nombre, weight=ft.FontWeight.BOLD),
                                        ft.Text(f"Cantidad: {boost.cantidad}", size=12, color=ft.Colors.GREY_600),
                                    ],
                                    spacing=2,
                                    expand=True
                                ),
                                ft.TextButton(
                                    " Usar",
                                    on_click=lambda e: on_use_boost() if on_use_boost else None,
                                    style=ft.ButtonStyle(
                                        bgcolor=ft.Colors.ORANGE_700,
                                        color=ft.Colors.WHITE
                                    )
                                )
                            ],
                            spacing=10,
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        padding=10
                    )
                )
            )
    
    # Si no hay items
    if not items_list:
        items_list.append(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.INVENTORY_2_OUTLINED, size=60, color=ft.Colors.GREY_400),
                        ft.Text("Tu inventario está vacío", size=16, color=ft.Colors.GREY_600),
                        ft.Text("Compra items en la tienda", size=14, color=ft.Colors.GREY_500),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                alignment=ft.Alignment.CENTER,
                expand=True
            )
        )
    
    return ft.Container(
        content=ft.Column(
            items_list,
            spacing=10,
            scroll=ft.ScrollMode.AUTO
        ),
        padding=15,
        expand=True)