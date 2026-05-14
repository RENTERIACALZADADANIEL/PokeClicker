import bcrypt

class LoginController:
    def __init__(self, model):
        self.model = model

    def verificar_credenciales(self, email, password):
        """Lógica para iniciar sesión."""
        if not email or not password:
            return None, "Por favor, completa todos los campos."

        usuario = self.model.obtener_usuario_por_email(email)

        if usuario:
            # Verificamos si la contraseña coincide con el hash de la DB
            # password.encode() convierte el string del input en bytes para bcrypt
            password_bytes = password.encode('utf-8')
            hash_bytes = usuario['password'].encode('utf-8')

            if bcrypt.checkpw(password_bytes, hash_bytes):
                return usuario, None # Éxito
            else:
                return None, "Contraseña incorrecta."
        
        return None, "El correo electrónico no está registrado."

    def crear_cuenta(self, username, email, password):
        """Lógica para registrar un nuevo usuario."""
        # 1. Validaciones básicas de campos vacíos
        if not username or not email or not password:
            return "Todos los campos son obligatorios."

        # 2. Verificar si el usuario ya existe para evitar duplicados
        if self.model.obtener_usuario_por_email(email):
            return "Este correo ya está en uso."

        try:
            # 3. Hashear la contraseña (Seguridad)
            # Generamos un 'salt' y creamos el hash
            salt = bcrypt.gensalt()
            password_hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
            
            # Convertimos el hash de bytes a string para guardarlo en MariaDB (VARCHAR)
            password_hashed_str = password_hashed.decode('utf-8')

            # 4. Mandar al modelo para guardar
            exito = self.model.registrar_usuario(username, email, password_hashed_str)
            
            if exito:
                return True
            else:
                return "Hubo un problema con la base de datos."
        except Exception as e:
            return f"Error inesperado: {str(e)}"