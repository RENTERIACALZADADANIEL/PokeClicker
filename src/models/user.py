from config.database import db
from datetime import datetime
import bcrypt

class User:
    def __init__(self, id_usuario=None, username=None, email=None, password=None, fecha_registro=None):
        self.id_usuario = id_usuario
        self.username = username
        self.email = email
        self.password = password
        self.fecha_registro = fecha_registro or datetime.now()
    
    def save(self):
        cursor = db.get_cursor()
        if cursor:
            try:
                query = """
                    INSERT INTO usuarios (username, email, password) 
                    VALUES (%s, %s, %s)
                """
                cursor.execute(query, (self.username, self.email, self.password))
                db.connection.commit()
                self.id_usuario = cursor.lastrowid
                return True
            except Exception as e:
                print(f"Error saving user: {e}")
                db.connection.rollback()
                return False
            finally:
                cursor.close()
        return False
    
    @staticmethod
    def find_by_email(email):
        cursor = db.get_cursor()
        if cursor:
            try:
                query = "SELECT * FROM usuarios WHERE email = %s"
                cursor.execute(query, (email,))
                user_data = cursor.fetchone()
                if user_data:
                    return User(**user_data)
                return None
            except Exception as e:
                print(f"Error finding user: {e}")
                return None
            finally:
                cursor.close()
        return None
    
    @staticmethod
    def find_by_id(user_id):
        cursor = db.get_cursor()
        if cursor:
            try:
                query = "SELECT * FROM usuarios WHERE id_usuario = %s"
                cursor.execute(query, (user_id,))
                user_data = cursor.fetchone()
                if user_data:
                    return User(**user_data)
                return None
            except Exception as e:
                print(f"Error finding user: {e}")
                return None
            finally:
                cursor.close()
        return None
    
    @staticmethod
    def email_exists(email):
        return User.find_by_email(email) is not None
    
    @staticmethod
    def username_exists(username):
        cursor = db.get_cursor()
        if cursor:
            try:
                query = "SELECT id_usuario FROM usuarios WHERE username = %s"
                cursor.execute(query, (username,))
                return cursor.fetchone() is not None
            except Exception as e:
                print(f"Error checking username: {e}")
                return False
            finally:
                cursor.close()
        return False
    
    def verify_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    
    def update_password(self, new_password):
        cursor = db.get_cursor()
        if cursor:
            try:
                hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                query = "UPDATE usuarios SET password = %s WHERE id_usuario = %s"
                cursor.execute(query, (hashed.decode('utf-8'), self.id_usuario))
                db.connection.commit()
                return True
            except Exception as e:
                print(f"Error updating password: {e}")
                db.connection.rollback()
                return False
            finally:
                cursor.close()
        return False