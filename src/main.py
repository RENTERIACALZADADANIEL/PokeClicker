import flet as ft
import traceback

try:
    from controllers.UserController import AuthController
    from controllers.ProgresoController import ProgresoController
    from models.PokemonModel import PokemonModel
    from views.LoginView import LoginView
    from views.HomeView import HomeView   
    from views.RegistroView import RegistroView
    print("✅ Todas las importaciones OK")
except Exception as e:
    print(f" Error en importaciones: {e}")
    traceback.print_exc()

def start(page: ft.Page):
    print(" start() ejecutándose ")
    page.title = "Pokémon Clicker"
    page.window_width = 450
    page.window_height = 700
    page.bgcolor = ft.Colors.RED_50
    
    try:
        auth_ctrl = AuthController()
        progreso_ctrl = ProgresoController()
        pokemon_ctrl = PokemonModel()
        print("✅ Controladores creados")
    except Exception as e:
        print(f" Error creando controladores: {e}")
        traceback.print_exc()
        page.add(ft.Text(f"Error: {e}", color=ft.Colors.RED))
        page.update()
        return

    def route_change(e):
        print(f" route_change: {page.route}")
        try:
            page.views.clear()
            
            if page.route == "/":
                print("  ➜ Creando LoginView")
                vista = LoginView(page, auth_ctrl)
                page.views.append(vista)
                
            elif page.route == "/registro":
                print("  ➜ Creando RegistroView")
                vista = RegistroView(page, auth_ctrl)
                page.views.append(vista)
                
            elif page.route == "/home":
                print("  ➜ Creando HomeView")
                vista = HomeView(page, progreso_ctrl, pokemon_ctrl)
                page.views.append(vista)
                
            else:
                print(f"  ➜ Ruta desconocida: {page.route}")
                page.go("/")
                return
            
            print(f"  ➜ Vista agregada. Total vistas: {len(page.views)}")
            page.update()
            print("  ➜ page.update() completado")
            
        except Exception as e:
            print(f" ERROR en route_change: {e}")
            traceback.print_exc()
            page.clean()
            page.add(ft.Text(f"Error: {e}", color=ft.Colors.RED))
            page.update()
    
    def view_pop(e):
        print(" view_pop")
        if len(page.views) > 1:
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)
    
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    print("Navegando a /")
    
   
    print("Creando vista inicial manualmente...")
    try:
        vista_inicial = LoginView(page, auth_ctrl)
        page.views.append(vista_inicial)
        page.update()
        print(" Vista inicial creada manualmente")
    except Exception as e:
        print(f" Error creando vista inicial: {e}")
        traceback.print_exc()
        page.add(ft.Text(f"Error: {e}", color=ft.Colors.RED))
        page.update()

def main():
    print("=== main() iniciado ===")
    ft.app(target=start)

if __name__ == "__main__":
    print(" Script iniciado")
    main()