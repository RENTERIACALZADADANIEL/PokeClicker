import flet as ft

class LoginView(ft.View):
    def __init__(self, al_intentar_login):
        super().__init__(route="/login")
        self.al_intentar_login = al_intentar_login
        
        self.txt_email = ft.TextField(label="Correo Electrónico", width=350)
        self.txt_pass = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=350)
        self.lbl_error = ft.Text(color="red", weight="bold")
        
        self.controls = [
            ft.AppBar(title=ft.Text("Poke Clicker - Login"), bgcolor="red", color="white"),
            ft.Column(
                [
                    ft.Image(src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/poke-ball.png", width=100),
                    ft.Text("¡Inicia tu aventura!", size=25, weight="bold"),
                    self.txt_email,
                    self.txt_pass,
                    ft.ElevatedButton("Ingresar", on_click=self.login_click, width=200),
                    self.lbl_error
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True
            )
        ]

    def login_click(self, e):
        self.al_intentar_login(self.txt_email.value, self.txt_pass.value)