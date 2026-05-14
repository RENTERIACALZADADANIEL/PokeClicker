import hashlib # O usa bcrypt si las tienes encriptadas

class LoginController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def intentar_login(self, email, password):
        if not email or not password:
            return "Por favor, llena todos los campos."

        user = self.model.validar_usuario(email)
        
        if user:
            # Si en tu DB las guardas en texto plano (no recomendado):
            # if user['password'] == password:
            
            # Si las guardas con Hash (recomendado):
            # pass_hash = hashlib.sha256(password.encode()).hexdigest()
            
            if user['password'] == password: 
                return True
            else:
                return "Contraseña incorrecta."
        else:
            return "Usuario no encontrado."