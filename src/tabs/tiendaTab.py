import flet as ft

def tienda_tab(rebirths=0, on_buy_pokemon=None, on_buy_boost=None):
   
    #Args:
       # rebirths: Cantidad de rebirths del usuario
        #on_buy_pokemon: Callback para comprar pokémon
       # on_buy_boost: Callback para comprar boost
  
    puede_comprar_pokemon = rebirths >= 10
    puede_comprar_boost = rebirths >= 3
    
    print(f" Cargando tienda - Rebirths: {rebirths} | Puede comprar Pokémon: {puede_comprar_pokemon} | Puede comprar Boost: {puede_comprar_boost}")
    
    def comprar_pokemon_click(e):
        print(" Click en comprar Pokémon")
        if on_buy_pokemon:
            on_buy_pokemon()
        else:
            print(" on_buy_pokemon es None")
    
    def comprar_boost_click(e):
        print(" Click en comprar Boost")
        if on_buy_boost:
            on_buy_boost()
        else:
            print(" on_buy_boost es None")
    
    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Tienda Pokémon", size=25, weight="bold"),
                
                ft.Text(f"💎 Tus Rebirths: {rebirths}", size=16, weight=ft.FontWeight.BOLD),
                
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                
                # Pokémon Aleatorio
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Icon(ft.Icons.CATCHING_POKEMON, size=40, color=ft.Colors.RED_400),
                                        ft.Column(
                                            [
                                                ft.Text("Pokémon Aleatorio", weight=ft.FontWeight.BOLD, size=16),
                                                ft.Text("¡Obtén un pokémon al azar de la PokéAPI!", size=12),
                                            ]
                                        )
                                    ],
                                    spacing=10
                                ),
                                ft.Row(
                                    [
                                        ft.Text("💎 10 Rebirths", weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_700),
                                        ft.TextButton(
                                            "Comprar",
                                            on_click=comprar_pokemon_click,  
                                            disabled=not puede_comprar_pokemon,
                                            style=ft.ButtonStyle(
                                                bgcolor=ft.Colors.RED_700 if puede_comprar_pokemon else ft.Colors.GREY_400,
                                                color=ft.Colors.WHITE
                                            )
                                        )
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                )
                            ],
                            spacing=10
                        ),
                        padding=15
                    )
                ),
                
                # Boost x2
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Icon(ft.Icons.BOLT, size=40, color=ft.Colors.ORANGE_400),
                                        ft.Column(
                                            [
                                                ft.Text("Boost x2 (5 min)", weight=ft.FontWeight.BOLD, size=16),
                                                ft.Text("Duplica tus clicks por 5 minutos", size=12),
                                            ]
                                        )
                                    ],
                                    spacing=10
                                ),
                                ft.Row(
                                    [
                                        ft.Text("💎 3 Rebirths", weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_700),
                                        ft.TextButton(
                                            "Comprar",
                                            on_click=comprar_boost_click, 
                                            disabled=not puede_comprar_boost,
                                            style=ft.ButtonStyle(
                                                bgcolor=ft.Colors.ORANGE_700 if puede_comprar_boost else ft.Colors.GREY_400,
                                                color=ft.Colors.WHITE
                                            )
                                        )
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                )
                            ],
                            spacing=10
                        ),
                        padding=15
                    )
                ),
            ],
            spacing=10,
            scroll=ft.ScrollMode.AUTO
        ),
        padding=15,
        expand=True
    )