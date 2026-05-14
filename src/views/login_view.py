import flet as ft

class LoginView(ft.Column):
    def __init__(self, on_login_click):
        super().__init__()
        self.on_login_click = on_login_click # Función que viene del controlador
        
        self.txt_email = ft.TextField(label="Email", width=300)
        self.txt_password = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)
        self.lbl_error = ft.Text(color="red")
        
        self.controls = [
            ft.Text("Poke Clicker - Login", size=30, weight="bold"),
            self.txt_email,
            self.txt_password,
            ft.ElevatedButton("Iniciar Sesión", on_click=self.login_submit, bgcolor="red", color="white"),
            self.lbl_error
        ]
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def login_submit(self, e):
        # Llamamos a la lógica pasándole los datos
        self.on_login_click(self.txt_email.value, self.txt_password.value)