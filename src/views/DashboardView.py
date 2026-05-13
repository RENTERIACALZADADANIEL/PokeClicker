import flet as ft

def DashboardView(page: ft.Page, tarea_controller):
    user = getattr(page, "user_data", None)
    lista_tareas = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True)

    def borrar_tarea_click(id_tarea):
        success, msg = tarea_controller.eliminar_tarea(id_tarea)
        if success:
            refresh_tareas()

    def refresh_tareas():
        if user and 'id_usuario' in user:
            lista_tareas.controls.clear()
            tareas = tarea_controller.obtener_lista(user['id_usuario'])
            for t in tareas:
                lista_tareas.controls.append(
                    ft.Card(
                        content=ft.Container(
                            content=ft.ListTile(
                                title=ft.Text(t['titulo'], weight="bold"),
                                subtitle=ft.Text(
                                    f"{t['descripcion']}\nPrioridad: {t['prioridad']} | Límite: {t['fecha_limite']}"
                                ),
                                trailing=ft.IconButton(
                                    icon=ft.Icons.DELETE_OUTLINE,
                                    icon_color="red",
                                    on_click=lambda e, id=t['id_tarea']: borrar_tarea_click(id)
                                )
                            ),
                            padding=10
                        )
                    )
                )
            page.update()

   
    txt_titulo = ft.TextField(label="Título", expand=True)
    txt_desc = ft.TextField(label="Descripción", multiline=True, max_lines=2)
    dd_prio = ft.Dropdown(
        label="Prioridad",
        value="media",
        options=[ft.dropdown.Option("baja"), ft.dropdown.Option("media"), ft.dropdown.Option("alta")],
        width=120
    )
    txt_fecha = ft.TextField(label="Fecha (AAAA-MM-DD)", width=180)

    def add_task(e):
        if user and 'id_usuario' in user:
            success, msg = tarea_controller.guardar_nueva(
                user['id_usuario'], txt_titulo.value, txt_desc.value, 
                dd_prio.value, "personal", txt_fecha.value
            )
            if success:
                txt_titulo.value = ""; txt_desc.value = ""; txt_fecha.value = ""
                refresh_tareas()

   
    vista_inicio = ft.Column([
        ft.Text("Nueva Tarea", size=16, weight="bold"),
        ft.Row([txt_titulo, dd_prio]),
        txt_desc,
        ft.Row([txt_fecha, ft.ElevatedButton("Añadir", icon=ft.Icons.ADD, on_click=add_task)]),
        ft.Divider(),
        ft.Text("Mis Tareas", size=20, weight="bold"),
        lista_tareas
    ], expand=True, visible=True)

   
    vista_explorar = ft.Column([
        ft.Container(content=ft.Text("Sección de exploración próximamente", color="grey"), alignment=ft.Alignment.CENTER, expand=True)
    ], expand=True, visible=False)

   
    vista_perfil = ft.Column([
        ft.Container(
            content=ft.Column([
                ft.CircleAvatar(content=ft.Icon(ft.Icons.PERSON), radius=40),
                ft.Text(user['nombre'] if user else "Usuario", size=24, weight="bold"),
                ft.Text(user['email'] if user else "", size=16, color="grey"),
                ft.Text(f"Último acceso: {user.get('ultimo_acceso', 'N/A')}", size=13, italic=True, color="bluegrey400"),
                ft.Divider(),
                ft.ListTile(leading=ft.Icon(ft.Icons.LOGOUT, color="red"), title=ft.Text("Cerrar Sesión", color="red"), on_click=lambda _: page.go("/"))
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20
        )
    ], expand=True, visible=False)

    def cambiar_pestana(e):
        idx = e.control.selected_index
        vista_inicio.visible = (idx == 0)
        vista_explorar.visible = (idx == 1)
        vista_perfil.visible = (idx == 2)
        if idx == 0: refresh_tareas()
        page.update()

    nav_bar = ft.NavigationBar(
        selected_index=0,
        on_change=cambiar_pestana,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Inicio"),
            ft.NavigationBarDestination(icon=ft.Icons.EXPLORE, label="Explorar"),
            ft.NavigationBarDestination(icon=ft.Icons.PERSON, label="Perfil"),
        ],
    )

    return ft.View(
        route="/dashboard",
        navigation_bar=nav_bar,
        controls=[
            ft.AppBar(title=ft.Text("SIGE"), bgcolor=ft.Colors.BLACK, color="white"),
            ft.Container(content=ft.Stack([vista_inicio, vista_explorar, vista_perfil]), padding=20, expand=True)
        ]
    )  