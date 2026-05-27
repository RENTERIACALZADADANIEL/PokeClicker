import flet as ft
from views.login_view import LoginView
from views.register_view import RegisterView
from tabs.principal_tab import principal_tab
from tabs.tienda_tab import tienda_tab
from tabs.inventario_tab import inventario_tab
from models.game_progress import GameProgress
from controllers.shop_controller import ShopController
import threading
import time

class PokeClickerApp:
    """Aplicación principal PokeClicker"""
    
    def __init__(self):
        self.current_user = None
        self.registered_email = None
        self._session_data = {}
        self.page = None
        self.game_progress = None
        self.shop_controller = None
        self.boost_timer = None
        self.main_container = None
        self.contenido_pagina = None
        self.appbar = None
        self.navigation_bar = None
    
    # ============================================================
    # PUNTO DE ENTRADA
    # ============================================================
    
    def main(self, page: ft.Page):
        self.page = page
        
        page.title = "Poke Clicker"
        page.window.width = 420
        page.window.height = 750
        page.theme_mode = ft.ThemeMode.LIGHT
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        
        self.main_container = ft.Container(expand=True)
        page.add(self.main_container)
        
        self.show_login()
    
    # ============================================================
    # UTILIDADES DE SESIÓN
    # ============================================================
    
    def set_session(self, key, value):
        self._session_data[key] = value
    
    def get_session(self, key, default=None):
        return self._session_data.get(key, default)
    
    def clear_session(self):
        self._session_data.clear()
        if self.boost_timer:
            self.boost_timer = None
    
    # ============================================================
    # DIÁLOGOS
    # ============================================================
    
    def mostrar_dialogo(self, dialog):
        """Muestra un diálogo eliminando cualquier diálogo previo"""
        for control in self.page.overlay[:]:
            if isinstance(control, ft.AlertDialog):
                self.page.overlay.remove(control)
        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()
    
    def cerrar_dialogo(self):
        """Cierra y elimina todos los diálogos"""
        for control in self.page.overlay[:]:
            if isinstance(control, ft.AlertDialog):
                self.page.overlay.remove(control)
        self.page.update()
    
    def mostrar_error(self, message):
        """Muestra un diálogo de error"""
        dialog = ft.AlertDialog(
            title=ft.Text("❌ Error"),
            content=ft.Text(message),
            actions=[ft.TextButton("OK", on_click=lambda e: self.cerrar_dialogo())]
        )
        self.mostrar_dialogo(dialog)
    
    def mostrar_exito(self, message):
        """Muestra un diálogo de éxito"""
        dialog = ft.AlertDialog(
            title=ft.Text("✅ Éxito"),
            content=ft.Text(message),
            actions=[ft.TextButton("OK", on_click=lambda e: self.cerrar_dialogo())]
        )
        self.mostrar_dialogo(dialog)
    
    # ============================================================
    # NAVEGACIÓN
    # ============================================================
    
    def show_login(self, prefill_email=None):
        """Muestra la pantalla de inicio de sesión"""
        self.clear_session()
        self.current_user = None
        self.game_progress = None
        self.shop_controller = None
        self.cerrar_dialogo()
        
        login_view = LoginView(
            page=self.page,
            on_login_success=lambda user_data: self.on_login_success(user_data),
            on_register_click=lambda e: self.show_register()
        )
        
        if prefill_email:
            login_view.email_input.value = prefill_email
            login_view.register_success_text.value = "✅ ¡Registro exitoso! Ahora inicia sesión"
        
        self.main_container.content = login_view.build()
        self.main_container.alignment = ft.Alignment.CENTER
        self.page.update()
    
    def show_register(self):
        """Muestra la pantalla de registro"""
        register_view = RegisterView(
            page=self.page,
            on_register_success=lambda email: self.on_register_success(email),
            on_login_click=lambda e: self.show_login()
        )
        
        register_view.email_input.on_change = register_view.validate_email_format
        register_view.password_input.on_change = register_view.check_password_strength
        
        self.main_container.content = register_view.build()
        self.main_container.alignment = ft.Alignment.CENTER
        self.page.update()
    
    # ============================================================
    # CALLBACKS DE AUTENTICACIÓN
    # ============================================================
    
    def on_register_success(self, email):
        self.registered_email = email
        self.show_login(prefill_email=email)
    
    def on_login_success(self, user_data):
        self.set_session("user_id", user_data.id_usuario)
        self.set_session("username", user_data.username)
        self.set_session("email", user_data.email)
        self.current_user = user_data
        
        self.game_progress = GameProgress.get_by_user_id(user_data.id_usuario)
        self.shop_controller = ShopController(user_data.id_usuario)
        
        print(f"✅ Login exitoso: {user_data.username}")
        self.show_dashboard()
    
    # ============================================================
    # LÓGICA DEL JUEGO
    # ============================================================
    
    def do_click(self):
        if not self.game_progress:
            return
        
        clicks_ganados = self.game_progress.click()
        self.game_progress.save()
        
        print(f"⚡ Click! +{clicks_ganados} (Actuales: {self.game_progress.clicks_actuales})")
        self.update_dashboard_view()
    
    def do_rebirth(self):
        """
        Realiza un rebirth SIN diálogo.
        1. Verifica que tenga suficientes clicks
        2. Gasta clicks, reinicia contador
        3. Activa boost x1.25 por 5 minutos
        4. Aumenta costo del siguiente rebirth
        """
        if not self.game_progress:
            return
        
        if not self.game_progress.can_rebirth():
            return
        
        rebirth_num = self.game_progress.cantidad_rebirths + 1
        costo = self.game_progress.costo_siguiente_rebirth
        
        if self.game_progress.do_rebirth():
            # Solo mostrar en consola
            print(f"🔄 Rebirth #{rebirth_num}! Boost x1.25 por 5 minutos")
            print(f"   Costo: {costo:,} clicks")
            print(f"   Próximo rebirth: {self.game_progress.costo_siguiente_rebirth:,} clicks")
            
            # Actualizar vista e iniciar timer del boost
            self.update_dashboard_view()
            self.start_boost_timer()
    
    def start_boost_timer(self):
        def update_loop():
            while self.game_progress and self.game_progress.get_boost_time_remaining() > 0:
                time.sleep(1)
                try:
                    self.update_dashboard_view()
                except Exception:
                    break
            
            try:
                self.update_dashboard_view()
            except Exception:
                pass
        
        timer = threading.Thread(target=update_loop, daemon=True)
        timer.start()
    
    def update_dashboard_view(self):
        if not self.game_progress or not hasattr(self, 'contenido_pagina'):
            return
        
        try:
            stats = self.game_progress.get_stats()
            
            self.contenido_pagina.content = principal_tab(
                clicks_actuales=stats["clicks_actuales"],
                clicks_totales=stats["clicks_totales"],
                cantidad_rebirths=stats["cantidad_rebirths"],
                costo_rebirth=stats["costo_siguiente_rebirth"],
                multiplicador=stats["multiplicador_activo"],
                puede_rebirth=stats["puede_rebirth"],
                boost_activo=stats["boost_activo"],
                boost_tiempo_restante=stats["boost_tiempo_restante"],
                on_click=self.do_click,
                on_rebirth=self.do_rebirth
            )
            
            self.page.update()
        except Exception as e:
            print(f"Error actualizando dashboard: {e}")
    
    # ============================================================
    # COMPRAS EN TIENDA
    # ============================================================
    
    def buy_pokemon(self):
        """Compra un pokémon aleatorio"""
        if not self.shop_controller:
            return
        
        success, message, pokemon_data = self.shop_controller.buy_random_pokemon()
        
        if success and pokemon_data:
            dialog = ft.AlertDialog(
                title=ft.Text("🎉 ¡Nuevo Pokémon!"),
                content=ft.Column(
                    [
                        ft.Image(
                            src=pokemon_data['sprite'],
                            width=150,
                            height=150,
                            fit=ft.ImageFit.CONTAIN
                        ),
                        ft.Text(
                            f"¡Has obtenido a {pokemon_data['name']}!",
                            size=18,
                            weight=ft.FontWeight.BOLD
                        ),
                        ft.Text(
                            f"Tipos: {', '.join(pokemon_data['types'])}",
                            size=14,
                            color=ft.Colors.GREY_600
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10
                ),
                actions=[
                    ft.TextButton(
                        "¡Genial!",
                        on_click=lambda e: self._close_and_refresh_tienda()
                    )
                ],
                actions_alignment=ft.MainAxisAlignment.CENTER
            )
            self.mostrar_dialogo(dialog)
        else:
            self.mostrar_error(message)
    
    def buy_boost(self):
        """Compra un boost x2"""
        if not self.shop_controller:
            return
        
        success, message = self.shop_controller.buy_boost()
        
        if success:
            self.mostrar_exito(message)
            self.update_dashboard_view()
        else:
            self.mostrar_error(message)
    
    def use_boost_from_inventory(self):
        """Usa un boost del inventario"""
        if not self.shop_controller:
            return
        
        success, message = self.shop_controller.use_boost()
        
        if success:
            self.mostrar_exito(message)
            self.update_dashboard_view()
            self.start_boost_timer()
        else:
            self.mostrar_error(message)
    
    def _close_and_refresh_tienda(self):
        """Cierra diálogo y refresca la vista de tienda"""
        self.cerrar_dialogo()
        self.update_dashboard_view()
        self.cargar_tienda()
    
    def cargar_tienda(self):
        """Carga la pestaña de tienda"""
        if not self.game_progress:
            return
        
        rebirths = self.game_progress.cantidad_rebirths
        
        self.contenido_pagina.content = tienda_tab(
            rebirths=rebirths,
            on_buy_pokemon=self.buy_pokemon,
            on_buy_boost=self.buy_boost
        )
        self.appbar.bgcolor = ft.Colors.BLUE_700
        self.appbar.title = ft.Text("Tienda Pokémon", weight=ft.FontWeight.BOLD)
        self.page.update()
    
    def cargar_inventario(self):
        """Carga la pestaña de inventario"""
        if not self.current_user:
            return
        
        inventory = self.shop_controller.get_inventory(self.current_user.id_usuario) if self.shop_controller else []
        
        self.contenido_pagina.content = inventario_tab(
            inventory_items=inventory,
            on_use_boost=self.use_boost_from_inventory
        )
        self.appbar.bgcolor = ft.Colors.GREEN_700
        self.appbar.title = ft.Text("Inventario", weight=ft.FontWeight.BOLD)
        self.page.update()
    
    # ============================================================
    # DASHBOARD
    # ============================================================
    
    def show_dashboard(self):
        username = self.get_session("username", "Entrenador")
        
        stats = self.game_progress.get_stats() if self.game_progress else {
            "clicks_actuales": 0,
            "clicks_totales": 0,
            "cantidad_rebirths": 0,
            "costo_siguiente_rebirth": 100,
            "multiplicador_activo": 1.0,
            "puede_rebirth": False,
            "boost_activo": False,
            "boost_tiempo_restante": 0
        }
        
        # ============================================================
        # FUNCIÓN DE LOGOUT DIRECTO
        # ============================================================
        def logout(e=None):
            print("Cerrando sesión...")
            self.cerrar_dialogo()
            self.clear_session()
            self.current_user = None
            self.game_progress = None
            self.shop_controller = None
            self.show_login()
        
        # ============================================================
        # CONTENEDOR DE CONTENIDO DINÁMICO
        # ============================================================
        self.contenido_pagina = ft.Container(
            content=principal_tab(
                clicks_actuales=stats["clicks_actuales"],
                clicks_totales=stats["clicks_totales"],
                cantidad_rebirths=stats["cantidad_rebirths"],
                costo_rebirth=stats["costo_siguiente_rebirth"],
                multiplicador=stats["multiplicador_activo"],
                puede_rebirth=stats["puede_rebirth"],
                boost_activo=stats["boost_activo"],
                boost_tiempo_restante=stats["boost_tiempo_restante"],
                on_click=self.do_click,
                on_rebirth=self.do_rebirth
            ),
            expand=True
        )
        
        # ============================================================
        # CAMBIO DE PESTAÑAS
        # ============================================================
        def cambiar_tab(e):
            opcion = e.control.selected_index
            
            if opcion == 0:
                if self.game_progress:
                    s = self.game_progress.get_stats()
                    self.contenido_pagina.content = principal_tab(
                        clicks_actuales=s["clicks_actuales"],
                        clicks_totales=s["clicks_totales"],
                        cantidad_rebirths=s["cantidad_rebirths"],
                        costo_rebirth=s["costo_siguiente_rebirth"],
                        multiplicador=s["multiplicador_activo"],
                        puede_rebirth=s["puede_rebirth"],
                        boost_activo=s["boost_activo"],
                        boost_tiempo_restante=s["boost_tiempo_restante"],
                        on_click=self.do_click,
                        on_rebirth=self.do_rebirth
                    )
                self.appbar.bgcolor = ft.Colors.RED_700
                self.appbar.title = ft.Text(f"Poke Clicker - {username}", weight=ft.FontWeight.BOLD)
                
            elif opcion == 1:
                self.cargar_tienda()
                
            elif opcion == 2:
                self.cargar_inventario()
            
            self.page.update()
        
        # ============================================================
        # NAVIGATION BAR
        # ============================================================
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
                    icon=ft.Icons.INVENTORY_2_OUTLINED,
                    selected_icon=ft.Icons.INVENTORY_2,
                    label="Inventario"
                ),
            ],
            on_change=cambiar_tab,
            bgcolor=ft.Colors.WHITE,
            indicator_color=ft.Colors.RED_100
        )
        
        # ============================================================
        # APPBAR CON LOGOUT DIRECTO
        # ============================================================
        self.appbar = ft.AppBar(
            leading=ft.Icon(ft.Icons.CATCHING_POKEMON),
            leading_width=40,
            title=ft.Text(f"Poke Clicker - {username}", weight=ft.FontWeight.BOLD),
            center_title=False,
            bgcolor=ft.Colors.RED_700,
            color=ft.Colors.WHITE,
            actions=[
                ft.IconButton(
                    icon=ft.Icons.LOGOUT,
                    tooltip="Cerrar sesión",
                    on_click=logout
                )
            ]
        )
        
        # ============================================================
        # ENSAMBLAR DASHBOARD
        # ============================================================
        dashboard = ft.Column(
            controls=[
                self.appbar,
                self.contenido_pagina,
                self.navigation_bar
            ],
            expand=True,
            spacing=0,
            alignment=ft.MainAxisAlignment.START
        )
        
        self.main_container.content = dashboard
        self.main_container.alignment = ft.Alignment.TOP_CENTER
        self.page.update()
        
        if stats["boost_activo"]:
            self.start_boost_timer()
        
        print(f"🎮 Dashboard cargado para: {username}")


if __name__ == "__main__":
    app = PokeClickerApp()
    ft.app(target=app.main)