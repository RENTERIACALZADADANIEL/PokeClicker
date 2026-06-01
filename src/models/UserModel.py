from models.databaseModel import db
from datetime import datetime
import bcrypt

class User:
    """Modelo de usuario unificado - Único punto de acceso a la tabla usuarios"""
    
    def __init__(self, id_usuario=None, username=None, email=None, password=None, fecha_registro=None):
        self.id_usuario = id_usuario
        self.username = username
        self.email = email
        self.password = password
        self.fecha_registro = fecha_registro or datetime.now()
    
    def to_dict(self):
        """Convierte el objeto a diccionario (sin contraseña)"""
        return {
            "id_usuario": self.id_usuario,
            "username": self.username,
            "email": self.email,
            "fecha_registro": self.fecha_registro
        }
    
    def save(self):
        """Guarda un nuevo usuario en la base de datos"""
        cursor = db.get_cursor()
        if not cursor:
            return False
        
        try:
            query = """
                INSERT INTO usuarios (username, email, password) 
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (self.username, self.email, self.password))
            db.commit()
            self.id_usuario = cursor.lastrowid
            return True
        except Exception as e:
            print(f"Error saving user: {e}")
            db.rollback()
            return False
        finally:
            cursor.close()
    
    def update_password(self, new_password):
        """Actualiza la contraseña del usuario (usa bcrypt internamente)"""
        cursor = db.get_cursor()
        if not cursor:
            return False
        
        try:
            hashed = bcrypt.hashpw(
                new_password.encode('utf-8'), 
                bcrypt.gensalt(rounds=12)
            )
            query = "UPDATE usuarios SET password = %s WHERE id_usuario = %s"
            cursor.execute(query, (hashed.decode('utf-8'), self.id_usuario))
            db.commit()
            return True
        except Exception as e:
            print(f"Error updating password: {e}")
            db.rollback()
            return False
        finally:
            cursor.close()
    
    def verify_password(self, password):
        """Verifica si la contraseña coincide con el hash almacenado"""
        try:
            return bcrypt.checkpw(
                password.encode('utf-8'), 
                self.password.encode('utf-8')
            )
        except Exception as e:
            print(f"Error verifying password: {e}")
            return False
    
    # ===== MÉTODOS ESTÁTICOS =====
    
    @staticmethod
    def find_by_email(email):
        """Busca un usuario por email"""
        cursor = db.get_cursor()
        if not cursor:
            return None
        
        try:
            query = "SELECT * FROM usuarios WHERE email = %s"
            cursor.execute(query, (email,))
            user_data = cursor.fetchone()
            if user_data:
                return User(**user_data)
            return None
        except Exception as e:
            print(f"Error finding user by email: {e}")
            return None
        finally:
            cursor.close()
    
    @staticmethod
    def find_by_id(user_id):
        """Busca un usuario por ID"""
        cursor = db.get_cursor()
        if not cursor:
            return None
        
        try:
            query = "SELECT * FROM usuarios WHERE id_usuario = %s"
            cursor.execute(query, (user_id,))
            user_data = cursor.fetchone()
            if user_data:
                return User(**user_data)
            return None
        except Exception as e:
            print(f"Error finding user by id: {e}")
            return None
        finally:
            cursor.close()
    
    @staticmethod
    def find_by_username(username):
        """Busca un usuario por nombre de usuario"""
        cursor = db.get_cursor()
        if not cursor:
            return None
        
        try:
            query = "SELECT * FROM usuarios WHERE username = %s"
            cursor.execute(query, (username,))
            user_data = cursor.fetchone()
            if user_data:
                return User(**user_data)
            return None
        except Exception as e:
            print(f"Error finding user by username: {e}")
            return None
        finally:
            cursor.close()
    
    @staticmethod
    def email_exists(email):
        """Verifica si un email ya está registrado"""
        return User.find_by_email(email) is not None
    
    @staticmethod
    def username_exists(username):
        """Verifica si un username ya está en uso"""
        return User.find_by_username(username) is not None
    
    @staticmethod
    def actualizar_password(email, nueva_password):
        """
        Actualiza la contraseña de un usuario por email.
        Hashea la contraseña antes de guardar.
        
        Args:
            email: Email del usuario
            nueva_password: Nueva contraseña en texto plano
            
        Returns:
            bool: True si se actualizó correctamente
        """
        cursor = db.get_cursor()
        if not cursor:
            return False
        
        try:
            hashed = bcrypt.hashpw(
                nueva_password.encode('utf-8'), 
                bcrypt.gensalt(rounds=12)
            )
            query = "UPDATE usuarios SET password = %s WHERE email = %s"
            cursor.execute(query, (hashed.decode('utf-8'), email))
            db.commit()
            
            if cursor.rowcount > 0:
                print(f"✅ Contraseña actualizada para {email}")
                return True
            else:
                print(f"❌ No se encontró usuario con email {email}")
                return False
        except Exception as e:
            print(f"Error actualizando password: {e}")
            db.rollback()
            return False
        finally:
            cursor.close()
    
    @staticmethod
    def get_total_users():
        """Obtiene el total de usuarios registrados"""
        cursor = db.get_cursor()
        if not cursor:
            return 0
        
        try:
            query = "SELECT COUNT(*) as total FROM usuarios"
            cursor.execute(query)
            result = cursor.fetchone()
            return result['total'] if result else 0
        except Exception as e:
            print(f"Error counting users: {e}")
            return 0
        finally:
            cursor.close()