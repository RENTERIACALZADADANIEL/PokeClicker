from models.UserModel import UsuarioModel
from models.schemasModel import RegistroSchema

class AuthController:
    def __init__(self):
        self.model = UsuarioModel()

    def login(self, email, password):
        
        user = self.model.validar_login(email, password)
        if user:
            return user, "Login exitoso"
        else:
            return None, "Correo o contraseña incorrectos"

    def registrar_usuario(self, nombre, email, password):
        try:
            
            nuevo_usuario = RegistroSchema(nombre=nombre, email=email, password=password)
            
            
            if self.model.registrar(nuevo_usuario):
                return True, "Registro exitoso. Ya puedes iniciar sesión."
            else:
                return False, "El correo ya está registrado."
        except Exception as e:
            return False, f"Error de validación: {str(e)}"