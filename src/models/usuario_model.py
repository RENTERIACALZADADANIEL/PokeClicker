from config.database import Database

class UsuarioModel:
    def obtener_usuario_por_email(self, email):
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()