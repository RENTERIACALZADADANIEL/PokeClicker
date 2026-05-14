from config.database import Database

class UsuarioModel:
    def __init__(self):
        self.db = Database()

    def validar_usuario(self, email):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        # Buscamos al usuario por email
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()
        return usuario