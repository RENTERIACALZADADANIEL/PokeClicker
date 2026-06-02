import flet as ft

def tienda_tab(rebirths=0, productos=None, on_buy_pokemon=None, on_buy_boost=None):
    if productos is None:
        productos = []

    cards = []
    for p in productos:
        puede_comprar = rebirths >= p["costo_rebirths"]
        es_pokemon = p["categoria"] == "pokemon"

        def hacer_compra(e, categoria=p["categoria"]):
            if categoria == "pokemon" and on_buy_pokemon:
                on_buy_pokemon()
            elif categoria == "boost" and on_buy_boost:
                on_buy_boost()

        cards.append(
            ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Icon(
                                        ft.Icons.CATCHING_POKEMON if es_pokemon else ft.Icons.BOLT,
                                        size=40,
                                        color=ft.Colors.RED_400 if es_pokemon else ft.Colors.ORANGE_400
                                    ),
                                    ft.Column(
                                        [
                                            ft.Text(p["nombre_producto"], weight=ft.FontWeight.BOLD, size=16),
                                            ft.Text(p["descripcion"] or "", size=12),
                                        ]
                                    )
                                ],
                                spacing=10
                            ),
                            ft.Row(
                                [
                                    ft.Text(
                                        f"💎 {p['costo_rebirths']} Rebirths",
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.PURPLE_700
                                    ),
                                    ft.TextButton(
                                        "Comprar",
                                        on_click=hacer_compra,
                                        disabled=not puede_comprar,
                                        style=ft.ButtonStyle(
                                            bgcolor=ft.Colors.RED_700 if (puede_comprar and es_pokemon)
                                                    else ft.Colors.ORANGE_700 if (puede_comprar and not es_pokemon)
                                                    else ft.Colors.GREY_400,
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
            )
        )

    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Tienda Pokémon", size=25, weight="bold"),
                ft.Text(f"💎 Tus Rebirths: {rebirths}", size=16, weight=ft.FontWeight.BOLD),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                *cards
            ],
            spacing=10,
            scroll=ft.ScrollMode.AUTO
        ),
        padding=15,
        expand=True
    )
