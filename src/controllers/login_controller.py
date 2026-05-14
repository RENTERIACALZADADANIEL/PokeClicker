import bcrypt

class LoginController:
    def __init__(self, model):
        self.model = model

    def verificar_credenciales(self, email, password):
        if not email or not password:
            return None, "Todos los campos son obligatorios."

        usuario = self.model.obtener_usuario_por_email(email)

        if usuario:
            # Verificamos la contraseña hasheada
            # password.encode() es la contraseña en texto plano del input
            # usuario['password'].encode() es el hash de la DB
            if bcrypt.checkpw(password.encode('utf-8'), usuario['password'].encode('utf-8')):
                return usuario, None
            else:
                return None, "Contraseña incorrecta."
        
        return None, "El usuario no existe."