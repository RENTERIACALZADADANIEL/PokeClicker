import flet as ft
from views.login_view import LoginView
from views.register_view import RegisterView
from tabs.principal_tab import principal_tab
from tabs.tienda_tab import tienda_tab
from tabs.ajustes_tab import ajustes_tab
from models.game_progress import GameProgress
import threading
import time

class PokeClickerApp:
    """
    Aplicación principal PokeClicker
    
    Patrón: Navegación por contenido dinámico
    - Usa un solo contenedor (self.main_container)
    - Cambia el contenido para navegar entre pantallas
    """
    
    def __init__(self):
        self.current_user = None
        self.registered_email = None
        self._session_data = {}
        self.page = None
        self.game_progress = None
        self.boost_timer = None
        self.main_container = None
        self.contenido_pagina = None
        self.appbar = None
        self.navigation_bar = None
    
    # ============================================================
    # PUNTO DE ENTRADA
    # ============================================================
    
    def main(self, page: ft.Page):
        """Punto de entrada de la aplicación Flet"""
        self.page = page
        
        # Configuración de la ventana
        page.title = "Poke Clicker"
        page.window.width = 420
        page.window.height = 750
        page.theme_mode = ft.ThemeMode.LIGHT
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        
        # Contenedor principal (único para toda la app)
        self.main_container = ft.Container(expand=True)
        page.add(self.main_container)
        
        # Mostrar pantalla de login directamente
        self.show_login()
    
    # ============================================================
    # UTILIDADES DE SESIÓN
    # ============================================================
    
    def set_session(self, key, value):
        """Guarda un valor en la sesión"""
        self._session_data[key] = value
    
    def get_session(self, key, default=None):
        """Obtiene un valor de la sesión"""
        return self._session_data.get(key, default)
    
    def clear_session(self):
        """Limpia todos los datos de sesión"""
        self._session_data.clear()
        if self.boost_timer:
            self.boost_timer = None
    
    # ============================================================
    # DIÁLOGOS
    # ============================================================
    
    def mostrar_dialogo(self, dialog):
        """Muestra un diálogo"""
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
    
    def cerrar_dialogo(self):
        """Cierra el diálogo actual"""
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.dialog = None
            self.page.update()
    
    # ============================================================
    # NAVEGACIÓN ENTRE PANTALLAS
    # ============================================================
    
    def show_login(self, prefill_email=None):
        """Muestra la pantalla de inicio de sesión"""
        self.clear_session()
        self.current_user = None
        self.game_progress = None
        
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
    
    
    # CALLBACKS DE AUTENTICACION
    
    
    def on_register_success(self, email):
        """Callback cuando el registro es exitoso"""
        self.registered_email = email
        self.show_login(prefill_email=email)
    
    def on_login_success(self, user_data):
        """Callback cuando el login es exitoso"""
        self.set_session("user_id", user_data.id_usuario)
        self.set_session("username", user_data.username)
        self.set_session("email", user_data.email)
        self.current_user = user_data
        
        # Cargar progreso del juego
        self.game_progress = GameProgress.get_by_user_id(user_data.id_usuario)
        
        print(f"✅ Login exitoso: {user_data.username}")
        self.show_dashboard()
    
    # ============================================================
    # LÓGICA DEL JUEGO
    # ============================================================
    
    def do_click(self):
        """Realiza un click en el juego"""
        if not self.game_progress:
            return
        
        clicks_ganados = self.game_progress.click()
        self.game_progress.save()
        
        print(f"⚡ Click! +{clicks_ganados}")
        self.update_dashboard_view()
    
    def do_rebirth(self):
        """Realiza un rebirth con boost temporal"""
        if not self.game_progress:
            return
        
        if not self.game_progress.can_rebirth():
            return
        
        rebirth_num = self.game_progress.cantidad_rebirths + 1
        costo = self.game_progress.costo_siguiente_rebirth
        
        if self.game_progress.do_rebirth():
            print(f"🔄 Rebirth #{rebirth_num}! Boost x1.25 por 5 minutos")
            
            def close_dialog(e):
                self.cerrar_dialogo()
                self.update_dashboard_view()
                self.start_boost_timer()
            
            dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("🌟 ¡Rebirth Exitoso!"),
                content=ft.Text(
                    f"🎉 ¡Felicidades!\n\n"
                    f"Rebirth: #{rebirth_num}\n"
                    f"Costo: {costo:,} clicks\n\n"
                    f"⚡ Boost: x1.25 por 5 minutos\n"
                    f"💎 Próximo: {self.game_progress.costo_siguiente_rebirth:,} clicks"
                ),
                actions=[
                    ft.TextButton(
                        "¡A farmear! ⚡",
                        on_click=close_dialog,
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.PURPLE_700,
                            color=ft.Colors.WHITE
                        )
                    )
                ],
                actions_alignment=ft.MainAxisAlignment.END
            )
            
            self.mostrar_dialogo(dialog)
    
    def start_boost_timer(self):
        """Inicia un timer para actualizar la UI durante el boost"""
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
        """Actualiza la vista del dashboard con los datos actuales"""
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
    # DASHBOARD
    # ============================================================
    
    def show_dashboard(self):
        """Construye y muestra el dashboard principal del juego"""
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
        
        def logout(e=None):
            print("Cerrando sesión...")
            self.clear_session()
            self.current_user = None
            self.game_progress = None
            self.show_login()
        
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
                self.contenido_pagina.content = tienda_tab()
                self.appbar.bgcolor = ft.Colors.BLUE_700
                self.appbar.title = ft.Text("Tienda Pokémon", weight=ft.FontWeight.BOLD)
            elif opcion == 2:
                self.contenido_pagina.content = ajustes_tab(logout)
                self.appbar.bgcolor = ft.Colors.GREEN_700
                self.appbar.title = ft.Text("Ajustes", weight=ft.FontWeight.BOLD)
            
            self.page.update()
        
        def confirmar_logout(e):
            def cerrar_sesion(e):
                self.cerrar_dialogo()
                logout()
            
            def cancelar(e):
                self.cerrar_dialogo()
            
            dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Cerrar Sesión"),
                content=ft.Text("¿Estás seguro de que deseas cerrar sesión?"),
                actions=[
                    ft.TextButton("Cancelar", on_click=cancelar),
                    ft.TextButton(
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
            
            self.mostrar_dialogo(dialog)
        
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
            on_change=cambiar_tab,
            bgcolor=ft.Colors.WHITE,
            indicator_color=ft.Colors.RED_100
        )
        
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
                    on_click=confirmar_logout
                )
            ]
        )
        
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