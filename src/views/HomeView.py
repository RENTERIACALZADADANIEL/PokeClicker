import flet as ft
import threading
import time

from tabs.principalTab import principal_tab
from tabs.tiendaTab import tienda_tab
from tabs.inventarioTab import inventario_tab
from utils.pokeapi import PokeAPI


def HomeView(page: ft.Page, progreso_ctrl, pokemon_ctrl):
    user = getattr(page, "user_data", None)
    if not user:
        page.go("/")
        return ft.View(route="/home", controls=[ft.Text("Redirigiendo...")])

    id_usuario = user["id_usuario"]

    # Estado reactivo
    estado = progreso_ctrl.obtener_progreso(id_usuario)
    inventario = progreso_ctrl.obtener_inventario(id_usuario)

    # Pokémon aleatorio inicial 
    _pokemon_inicial = PokeAPI.get_random_pokemon()
    pokemon_sprite = [
        _pokemon_inicial["sprite"] if _pokemon_inicial else
        "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/0.png"
    ]

    tab_index = [0]
    contenido = ft.Container(expand=True)

    def render():
        nonlocal estado, inventario
        idx = tab_index[0]
        if idx == 0:
            contenido.content = principal_tab(
                clicks_actuales=estado["clicks_actuales"],
                clicks_totales=estado["clicks_totales"],
                cantidad_rebirths=estado["cantidad_rebirths"],
                costo_rebirth=estado["costo_siguiente_rebirth"],
                multiplicador=estado["multiplicador_activo"],
                puede_rebirth=estado["puede_rebirth"],
                boost_activo=estado["boost_activo"],
                boost_tiempo_restante=estado["boost_tiempo_restante"],
                boost_info=estado["boost_info"],
                pokemon_sprite=pokemon_sprite[0],
                on_click=on_click,
                on_rebirth=on_rebirth,
            )
        elif idx == 1:
            contenido.content = tienda_tab(
                rebirths=estado["cantidad_rebirths"],
                on_buy_pokemon=on_buy_pokemon,
                on_buy_boost=on_buy_boost,
            )
        elif idx == 2:
            contenido.content = inventario_tab(
                inventory_items=inventario,
            )
        page.update()

    def on_click():
        progreso_ctrl.agregar_clicks(id_usuario)
        nonlocal estado
        estado = progreso_ctrl.obtener_progreso(id_usuario)
        render()

    def on_rebirth():
        nonlocal estado
        ok, msg = progreso_ctrl.realizar_rebirth(id_usuario)
        estado = progreso_ctrl.obtener_progreso(id_usuario)
        page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor=ft.Colors.PURPLE_700 if ok else ft.Colors.RED_700)
        page.snack_bar.open = True
        render()

    def on_buy_pokemon():
        nonlocal estado, inventario
        ok, msg, _ = progreso_ctrl.comprar_pokemon(id_usuario)
        estado = progreso_ctrl.obtener_progreso(id_usuario)
        inventario = progreso_ctrl.obtener_inventario(id_usuario)
        page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor=ft.Colors.RED_700 if ok else ft.Colors.GREY_700)
        page.snack_bar.open = True
        render()

    def on_buy_boost():
        nonlocal estado
        ok, msg = progreso_ctrl.comprar_boost_tienda(id_usuario)
        estado = progreso_ctrl.obtener_progreso(id_usuario)
        page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor=ft.Colors.ORANGE_700 if ok else ft.Colors.GREY_700)
        page.snack_bar.open = True
        render()

    def on_tab_change(e):
        tab_index[0] = e.control.selected_index
        nonlocal estado, inventario
        estado = progreso_ctrl.obtener_progreso(id_usuario)
        inventario = progreso_ctrl.obtener_inventario(id_usuario)
        render()

    # Timer para actualizar boost
    def boost_timer():
        while True:
            time.sleep(5)
            try:
                nonlocal estado
                if estado["boost_activo"]:
                    estado = progreso_ctrl.obtener_progreso(id_usuario)
                    if tab_index[0] == 0:
                        render()
            except Exception:
                break

    t = threading.Thread(target=boost_timer, daemon=True)
    t.start()

    nav_bar = ft.NavigationBar(
        selected_index=0,
        on_change=on_tab_change,
        bgcolor=ft.Colors.RED_100,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.CATCHING_POKEMON, label="Jugar"),
            ft.NavigationBarDestination(icon=ft.Icons.STORE, label="Tienda"),
            ft.NavigationBarDestination(icon=ft.Icons.INVENTORY_2, label="Inventario"),
        ],
    )

    render()

    return ft.View(
        route="/home",
        bgcolor=ft.Colors.RED_50,
        navigation_bar=nav_bar,
        appbar=ft.AppBar(
            title=ft.Text("Pokémon Clicker", color=ft.Colors.WHITE),
            bgcolor=ft.Colors.RED_800,
            center_title=True,
            actions=[
                ft.IconButton(
                    ft.Icons.LOGOUT,
                    icon_color=ft.Colors.WHITE,
                    on_click=lambda _: page.go("/")
                )
            ]
        ),
        controls=[contenido],
    )
