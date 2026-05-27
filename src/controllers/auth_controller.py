from models.user import User
from models.schemas import (
    UserRegisterSchema, 
    UserLoginSchema,
    PasswordResetSchema
)
from utils.security import (
    hash_password, 
    store_reset_token, 
    verify_reset_token, 
    delete_reset_token, 
    send_reset_email
)
import re

class AuthController:
    """Controlador de autenticación unificado"""
    
    def __init__(self):
        self.current_user = None
    
    # ============================================================
    # REGISTRO
    # ============================================================
    
    def register_user(self, data: dict) -> tuple[bool, str]:
        """Registra un nuevo usuario"""
        try:
            validated_data = UserRegisterSchema(**data)
            
            if User.email_exists(validated_data.email):
                return False, "El correo electrónico ya está registrado"
            
            if User.username_exists(validated_data.username):
                return False, "El nombre de usuario ya está en uso"
            
            hashed_password = hash_password(validated_data.password)
            
            user = User(
                username=validated_data.username,
                email=validated_data.email,
                password=hashed_password
            )
            
            if user.save():
                return True, "¡Usuario registrado exitosamente!"
            else:
                return False, "Error al registrar el usuario en la base de datos"
                
        except ValueError as e:
            error_messages = []
            if hasattr(e, 'errors'):
                for error in e.errors():
                    field = error.get('loc', ['unknown'])[0]
                    msg = error.get('msg', 'Error de validación')
                    error_messages.append(f"• {field}: {msg}")
                return False, "\n".join(error_messages)
            return False, str(e)
        except Exception as e:
            print(f"Error inesperado en registro: {e}")
            return False, f"Error inesperado: {str(e)}"
    
    # ============================================================
    # LOGIN
    # ============================================================
    
    def login_user(self, data: dict) -> tuple[bool, str]:
        """Inicia sesión de usuario"""
        try:
            from models.schemas import UserLoginSchema
            validated_data = UserLoginSchema(**data)
            
            user = User.find_by_email(validated_data.email)
            
            if not user:
                return False, "Credenciales inválidas"
            
            if user.verify_password(validated_data.password):
                self.current_user = user
                return True, f"¡Bienvenido de nuevo, {user.username}!"
            else:
                return False, "Credenciales inválidas"
                
        except ValueError as e:
            error_messages = []
            if hasattr(e, 'errors'):
                for error in e.errors():
                    field = error.get('loc', ['unknown'])[0]
                    msg = error.get('msg', 'Error de validación')
                    error_messages.append(f"• {field}: {msg}")
                return False, "\n".join(error_messages)
            return False, str(e)
        except Exception as e:
            print(f"Error inesperado en login: {e}")
            return False, f"Error inesperado: {str(e)}"
    
    def logout(self):
        """Cierra la sesión"""
        self.current_user = None
    
    # ============================================================
    # RECUPERACIÓN DE CONTRASEÑA (TOKEN 6 CARACTERES)
    # ============================================================
    
    def request_password_reset(self, email: str) -> tuple[bool, str]:
        """
        Paso 1: Solicita recuperación de contraseña
        
        1. Busca el usuario por email
        2. Genera token de 6 caracteres
        3. Almacena el token con expiración de 5 minutos
        4. Envía el token por email
        
        Returns:
            tuple[bool, str]: (éxito, mensaje)
        """
        try:
            # Validar email básico
            if not email or not self.validate_email(email):
                return False, "Ingresa un correo electrónico válido"
            
            # Buscar usuario
            user = User.find_by_email(email)
            
            if not user:
                # Por seguridad, no revelamos si el email existe
                return True, "Si el correo existe, recibirás un código de recuperación"
            
            # Generar y almacenar token
            token = store_reset_token(user.id_usuario, user.email)
            
            # Enviar correo con el token
            if send_reset_email(user.email, token, user.username):
                return True, "Se ha enviado un código de 6 caracteres a tu correo"
            else:
                # Si falla el envío, eliminar el token
                delete_reset_token(token)
                return False, "Error al enviar el correo. Intenta de nuevo."
                
        except Exception as e:
            print(f"Error en recuperación: {e}")
            return False, f"Error inesperado: {str(e)}"
    
    def verify_token(self, token: str) -> tuple[bool, str, dict | None]:
        """
        Paso 2: Verifica el token de 6 caracteres
        
        1. Busca el token en el almacenamiento
        2. Verifica que no haya expirado
        3. Retorna los datos del usuario si es válido
        
        Returns:
            tuple[bool, str, dict | None]: (éxito, mensaje, datos_usuario)
        """
        try:
            # Limpiar y validar formato del token
            token = token.strip().upper()
            
            if len(token) != 6:
                return False, "El código debe tener 6 caracteres", None
            
            # Verificar token
            token_data = verify_reset_token(token)
            
            if not token_data:
                return False, "Código inválido o expirado", None
            
            # Buscar usuario
            user = User.find_by_id(token_data["user_id"])
            if not user:
                return False, "Usuario no encontrado", None
            
            return True, "Código verificado correctamente", {
                "user_id": user.id_usuario,
                "email": user.email,
                "token": token  # Devolver token para usarlo en el paso 3
            }
            
        except Exception as e:
            print(f"Error verificando token: {e}")
            return False, f"Error inesperado: {str(e)}", None
    
    def reset_password_with_token(self, token: str, new_password: str) -> tuple[bool, str]:
        """
        Paso 3: Restablece la contraseña usando el token verificado
        
        1. Verifica el token nuevamente
        2. Valida la nueva contraseña
        3. Hashea la nueva contraseña
        4. Actualiza en la base de datos
        5. Elimina el token (un solo uso)
        
        Returns:
            tuple[bool, str]: (éxito, mensaje)
        """
        try:
            # Validar token
            token = token.strip().upper()
            token_data = verify_reset_token(token)
            
            if not token_data:
                return False, "Código inválido o expirado"
            
            # Validar nueva contraseña
            password_errors = self.validate_password(new_password)
            if password_errors:
                return False, "\n".join(password_errors)
            
            # Buscar usuario
            user = User.find_by_id(token_data["user_id"])
            if not user:
                return False, "Usuario no encontrado"
            
            # Hashear y actualizar contraseña
            if user.update_password(new_password):
                # Eliminar token (un solo uso)
                delete_reset_token(token)
                return True, "¡Contraseña actualizada exitosamente!"
            else:
                return False, "Error al actualizar la contraseña"
                
        except Exception as e:
            print(f"Error en reset password: {e}")
            return False, f"Error inesperado: {str(e)}"
    
    # ============================================================
    # MÉTODOS DE VALIDACIÓN
    # ============================================================
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Valida formato de email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_password(password: str) -> list:
        """
        Valida la fortaleza de la contraseña
        
        Requisitos:
        - Mínimo 6 caracteres
        - Al menos una mayúscula
        - Al menos una minúscula
        - Al menos un número
        """
        errors = []
        if len(password) < 6:
            errors.append("La contraseña debe tener al menos 6 caracteres")
        if not re.search(r'[A-Z]', password):
            errors.append("La contraseña debe contener al menos una mayúscula")
        if not re.search(r'[a-z]', password):
            errors.append("La contraseña debe contener al menos una minúscula")
        if not re.search(r'\d', password):
            errors.append("La contraseña debe contener al menos un número")
        return errors
    
    @staticmethod
    def validate_username(username: str) -> tuple[bool, str]:
        """Valida el formato del nombre de usuario"""
        if len(username) < 3:
            return False, "El nombre de usuario debe tener al menos 3 caracteres"
        if len(username) > 50:
            return False, "El nombre de usuario debe tener máximo 50 caracteres"
        if not username.replace('_', '').replace('-', '').isalnum():
            return False, "Solo letras, números, guiones y guiones bajos"
        return True, ""
    
    def is_authenticated(self) -> bool:
        """Verifica si hay un usuario autenticado"""
        return self.current_user is not None
    
    def get_current_user_dict(self) -> dict:
        """Obtiene los datos del usuario actual como diccionario"""
        if self.current_user:
            return self.current_user.to_dict()
        return {}