import flet as ft
from views.login_view import LoginView
from views.register_view import RegisterView
from views.reset_password_view import ResetPasswordView
from tabs.principal_tab import principal_tab
from tabs.tienda_tab import tienda_tab
from tabs.ajustes_tab import ajustes_tab
from models.game_progress import GameProgress
import threading
import time

class PokeClickerApp:
    def __init__(self):
        self.current_user = None
        self.registered_email = None
        self._session_data = {}
        self.page = None
        self.game_progress = None
        self.boost_timer = None
    
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
        
        token = self.get_token_from_url(page)
        
        if token:
            self.show_reset_password(token)
        else:
            self.show_login()
    
    def get_token_from_url(self, page):
        try:
            if hasattr(page, 'query') and page.query:
                if isinstance(page.query, dict):
                    return page.query.get("token")
                elif isinstance(page.query, str) and "token=" in page.query:
                    import urllib.parse
                    params = urllib.parse.parse_qs(page.query)
                    return params.get("token", [None])[0]
            
            import sys
            for arg in sys.argv:
                if arg.startswith("--token="):
                    return arg.replace("--token=", "")
            
            return None
        except Exception as e:
            print(f"Error al obtener token (ignorado): {e}")
            return None
    
    def set_session(self, key, value):
        self._session_data[key] = value
    
    def get_session(self, key, default=None):
        return self._session_data.get(key, default)
    
    def clear_session(self):
        self._session_data.clear()
        if self.boost_timer:
            self.boost_timer = None
    
    # ===== MÉTODO AUXILIAR PARA DIÁLOGOS =====
    
    def mostrar_dialogo(self, dialog):
        """Muestra un diálogo de forma compatible"""
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
    
    def cerrar_dialogo(self):
        """Cierra el diálogo actual"""
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.dialog = None
            self.page.update()
    
    # ===== NAVEGACIÓN =====
    
    def show_login(self, prefill_email=None):
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
    
    def show_reset_password(self, token):
        reset_view = ResetPasswordView(
            page=self.page,
            token=token,
            on_success=lambda: self.show_login(),
            on_cancel=lambda: self.show_login()
        )
        
        reset_view.new_password.on_change = reset_view.check_password_strength
        
        self.main_container.content = reset_view.build()
        self.main_container.alignment = ft.alignment.center
        self.page.update()
    
    def on_register_success(self, email):
        self.registered_email = email
        self.show_login(prefill_email=email)
    
    def on_login_success(self, user_data):
        self.set_session("user_id", user_data.id_usuario)
        self.set_session("username", user_data.username)
        self.set_session("email", user_data.email)
        self.current_user = user_data
        
        self.game_progress = GameProgress.get_by_user_id(user_data.id_usuario)
        
        print(f"✅ Login exitoso: {user_data.username}")
        self.show_dashboard()
    
    # ===== LÓGICA DEL JUEGO =====
    
    def do_click(self):
        if not self.game_progress:
            return
        
        clicks_ganados = self.game_progress.click()
        self.game_progress.save()
        
        print(f"⚡ Click! +{clicks_ganados}")
        self.update_dashboard_view()
    
    def do_rebirth(self):
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
    
    # ===== DASHBOARD =====
    
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
                appbar.bgcolor = ft.Colors.RED_700
                appbar.title = ft.Text(f"Poke Clicker - {username}", weight=ft.FontWeight.BOLD)
            elif opcion == 1:
                self.contenido_pagina.content = tienda_tab()
                appbar.bgcolor = ft.Colors.BLUE_700
                appbar.title = ft.Text("Tienda Pokémon", weight=ft.FontWeight.BOLD)
            elif opcion == 2:
                self.contenido_pagina.content = ajustes_tab(logout)
                appbar.bgcolor = ft.Colors.GREEN_700
                appbar.title = ft.Text("Ajustes", weight=ft.FontWeight.BOLD)
            
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
        
        navigation_bar = ft.NavigationBar(
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
        
        appbar = ft.AppBar(
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
                appbar,
                self.contenido_pagina,
                navigation_bar
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