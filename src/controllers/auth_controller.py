from models.user import User
from models.schemas import (
    UserRegisterSchema, 
    UserLoginSchema, 
    PasswordResetRequestSchema, 
    PasswordResetSchema
)
from utils.security import hash_password, generate_token, verify_token, send_reset_email
import re

class AuthController:
    """Controlador de autenticación unificado con Pydantic + JWT"""
    
    def __init__(self):
        self.current_user = None
    
    # ===== MÉTODOS DE AUTENTICACIÓN =====
    
    def register_user(self, data: dict) -> tuple[bool, str]:
        """
        Registra un nuevo usuario con validación Pydantic
        Returns: (success, message)
        """
        try:
            # Validar datos con Pydantic
            validated_data = UserRegisterSchema(**data)
            
            # Verificar si el email ya existe
            if User.email_exists(validated_data.email):
                return False, "El correo electrónico ya está registrado"
            
            # Verificar si el username ya existe
            if User.username_exists(validated_data.username):
                return False, "El nombre de usuario ya está en uso"
            
            # Hashear contraseña
            hashed_password = hash_password(validated_data.password)
            
            # Crear nuevo usuario
            user = User(
                username=validated_data.username,
                email=validated_data.email,
                password=hashed_password
            )
            
            # Guardar en base de datos
            if user.save():
                return True, "¡Usuario registrado exitosamente!"
            else:
                return False, "Error al registrar el usuario en la base de datos"
                
        except ValueError as e:
            # Errores de validación de Pydantic
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
    
    def login_user(self, data: dict) -> tuple[bool, str]:
        """
        Inicia sesión de usuario con validación Pydantic
        Returns: (success, message)
        """
        try:
            # Validar datos con Pydantic
            validated_data = UserLoginSchema(**data)
            
            # Buscar usuario por email
            user = User.find_by_email(validated_data.email)
            
            if not user:
                return False, "Credenciales inválidas"
            
            # Verificar contraseña
            if user.verify_password(validated_data.password):
                self.current_user = user
                return True, f"¡Bienvenido de nuevo, {user.username}!"
            else:
                return False, "Credenciales inválidas"
                
        except ValueError as e:
            # Errores de validación de Pydantic
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
        """Cierra la sesión del usuario actual"""
        self.current_user = None
    
    # ===== MÉTODOS DE RECUPERACIÓN DE CONTRASEÑA =====
    
    def request_password_reset(self, email: str) -> tuple[bool, str]:
        """
        Solicita restablecimiento de contraseña con validación Pydantic
        Returns: (success, message)
        """
        try:
            # Validar email con Pydantic
            validated = PasswordResetRequestSchema(email=email)
            
            # Buscar usuario
            user = User.find_by_email(validated.email)
            
            if not user:
                # Por seguridad, no revelamos si el email existe o no
                return True, "Si el correo existe, recibirás un enlace de recuperación"
            
            # Generar token JWT
            token = generate_token(user.id_usuario, user.email)
            
            # Enviar correo
            if send_reset_email(user.email, token, user.username):
                return True, "Se ha enviado un enlace de recuperación a tu correo"
            else:
                return False, "Error al enviar el correo de recuperación"
                
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            print(f"Error en recuperación: {e}")
            return False, f"Error inesperado: {str(e)}"
    
    def reset_password(self, data: dict) -> tuple[bool, str]:
        """
        Restablece la contraseña usando un token JWT
        Returns: (success, message)
        """
        try:
            # Validar datos con Pydantic
            validated = PasswordResetSchema(**data)
            
            # Verificar token JWT
            payload = verify_token(validated.token)
            if not payload:
                return False, "El enlace de recuperación es inválido o ha expirado"
            
            # Buscar usuario por ID del token
            user = User.find_by_id(payload['user_id'])
            if not user:
                return False, "Usuario no encontrado"
            
            # Verificar que el email del token coincida
            if user.email != payload.get('email'):
                return False, "Token inválido para este usuario"
            
            # Actualizar contraseña
            if user.update_password(validated.new_password):
                return True, "¡Contraseña actualizada exitosamente!"
            else:
                return False, "Error al actualizar la contraseña"
                
        except ValueError as e:
            # Errores de validación de Pydantic
            error_messages = []
            if hasattr(e, 'errors'):
                for error in e.errors():
                    field = error.get('loc', ['unknown'])[0]
                    msg = error.get('msg', 'Error de validación')
                    error_messages.append(f"• {field}: {msg}")
                return False, "\n".join(error_messages)
            return False, str(e)
        except Exception as e:
            print(f"Error en reset password: {e}")
            return False, f"Error inesperado: {str(e)}"
    
    # ===== MÉTODOS DE VALIDACIÓN =====
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Valida formato de email con regex"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_password(password: str) -> list:
        """
        Valida la fortaleza de la contraseña
        Returns: lista de errores (vacía si es válida)
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
            return False, "El username solo puede contener letras, números, guiones y guiones bajos"
        return True, ""
    
    # ===== MÉTODOS DE SESIÓN =====
    
    def is_authenticated(self) -> bool:
        """Verifica si hay un usuario autenticado"""
        return self.current_user is not None
    
    def get_current_user_dict(self) -> dict:
        """Obtiene los datos del usuario actual como diccionario"""
        if self.current_user:
            return self.current_user.to_dict()
        return {}
