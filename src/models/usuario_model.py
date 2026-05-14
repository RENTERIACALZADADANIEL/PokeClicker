from config.database import Database

class UsuarioModel:
    def __init__(self):
        # No guardamos la conexión aquí para evitar que se cierre inesperadamente
        pass

    def obtener_usuario_por_email(self, email):
        """Busca un usuario por su correo electrónico."""
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM usuarios WHERE email = %s"
            cursor.execute(query, (email,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error al obtener usuario: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def registrar_usuario(self, username, email, password_hashed):
        """Inserta un nuevo usuario con la contraseña ya hasheada."""
        conn = Database.get_connection()
        cursor = conn.cursor()
        try:
            query = "INSERT INTO usuarios (username, email, password) VALUES (%s, %s, %s)"
            cursor.execute(query, (username, email, password_hashed))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al insertar usuario: {e}")
            return False
        finally:
            cursor.close()
            conn.close()