import flet as ft

class RegistroView(ft.View):
    def __init__(self, al_intentar_registro, ir_a_login):
        super().__init__(route="/registro")
        self.al_intentar_registro = al_intentar_registro
        
        self.txt_user = ft.TextField(label="Nombre de Usuario", width=350)
        self.txt_email = ft.TextField(label="Correo Electrónico", width=350)
        self.txt_pass = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=350)
        self.lbl_msg = ft.Text()
        
        self.controls = [
            ft.AppBar(title=ft.Text("Crear Cuenta"), bgcolor="blue", color="white"),
            ft.Column(
                [
                    ft.Text("Únete a la aventura", size=25, weight="bold"),
                    self.txt_user,
                    self.txt_email,
                    self.txt_pass,
                    ft.ElevatedButton("Registrarse", on_click=self.registro_click, width=200),
                    ft.TextButton("¿Ya tienes cuenta? Inicia sesión", on_click=ir_a_login),
                    self.lbl_msg
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True
            )
        ]

    def registro_click(self, e):
        self.al_intentar_registro(self.txt_user.value, self.txt_email.value, self.txt_pass.value)