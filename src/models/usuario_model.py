from config.database import Database
from mysql.connector import Error

class UsuarioModel:
    def __init__(self):
        self.db = Database()
    
    def obtener_usuario_por_email(self, email):
        """Busca un usuario por su correo electrónico."""
        conn = None
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = "SELECT * FROM usuarios WHERE email = %s"
            cursor.execute(query, (email,))
            return cursor.fetchone()
            
        except Error as e:
            print(f"Error MySQL al obtener usuario: {e}")
            return None
        except Exception as e:
            print(f"Error inesperado: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
    
    def registrar_usuario(self, username, email, password_hashed):
        """Inserta un nuevo usuario con la contraseña ya hasheada."""
        conn = None
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            query = """
            INSERT INTO usuarios (username, email, password) 
            VALUES (%s, %s, %s)
            """
            cursor.execute(query, (username, email, password_hashed))
            conn.commit()
            return True
            
        except Error as e:
            print(f"Error MySQL al insertar usuario: {e}")
            if conn:
                conn.rollback()
            return False
        except Exception as e:
            print(f"Error inesperado: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()