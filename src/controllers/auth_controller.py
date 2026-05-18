from models.user import User
from models.schemas import UserRegisterSchema, UserLoginSchema, PasswordResetRequestSchema, PasswordResetSchema
from utils.security import hash_password, generate_token, verify_token, send_reset_email
import re

class AuthController:
    def __init__(self):
        self.current_user = None
    
    def register_user(self, data: dict) -> tuple[bool, str]:
        """
        Registra un nuevo usuario
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
            
            # Crear nuevo usuario
            user = User(
                username=validated_data.username,
                email=validated_data.email,
                password=hash_password(validated_data.password)
            )
            
            # Guardar en base de datos
            if user.save():
                return True, "¡Usuario registrado exitosamente!"
            else:
                return False, "Error al registrar el usuario"
                
        except ValueError as e:
            # Errores de validación de Pydantic
            return False, str(e)
        except Exception as e:
            return False, f"Error inesperado: {str(e)}"
    
    def login_user(self, data: dict) -> tuple[bool, str]:
        """
        Inicia sesión de usuario
        Returns: (success, message)
        """
        try:
            # Validar datos
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
            return False, str(e)
        except Exception as e:
            return False, f"Error inesperado: {str(e)}"
    
    def request_password_reset(self, email: str) -> tuple[bool, str]:
        """
        Solicita restablecimiento de contraseña
        Returns: (success, message)
        """
        try:
            # Validar email
            validated = PasswordResetRequestSchema(email=email)
            
            # Buscar usuario
            user = User.find_by_email(validated.email)
            
            if not user:
                # Por seguridad, no revelamos si el email existe o no
                return True, "Si el correo existe, recibirás un enlace de recuperación"
            
            # Generar token
            token = generate_token(user.id_usuario, user.email)
            
            # Enviar correo
            if send_reset_email(user.email, token, user.username):
                return True, "Se ha enviado un enlace de recuperación a tu correo"
            else:
                return False, "Error al enviar el correo de recuperación"
                
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Error inesperado: {str(e)}"
    
    def reset_password(self, data: dict) -> tuple[bool, str]:
        """
        Restablece la contraseña usando un token
        Returns: (success, message)
        """
        try:
            # Validar datos
            validated = PasswordResetSchema(**data)
            
            # Verificar token
            payload = verify_token(validated.token)
            if not payload:
                return False, "El enlace de recuperación es inválido o ha expirado"
            
            # Buscar usuario
            user = User.find_by_id(payload['user_id'])
            if not user:
                return False, "Usuario no encontrado"
            
            # Actualizar contraseña
            if user.update_password(validated.new_password):
                return True, "¡Contraseña actualizada exitosamente!"
            else:
                return False, "Error al actualizar la contraseña"
                
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Error inesperado: {str(e)}"
    
    def validate_email(self, email: str) -> bool:
        """Valida formato de email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def validate_password(self, password: str) -> list:
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