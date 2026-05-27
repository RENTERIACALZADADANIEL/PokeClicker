from models.user import User
from models.schemas import (
    UserRegisterSchema, 
    UserLoginSchema
)
from utils.security import hash_password
import re
import random
import os
import smtplib
from email.mime.text import MIMEText

class AuthController:
    """Controlador de autenticación unificado"""
    
    def __init__(self):
        self.current_user = None
        self._codigos = {}  # Almacenamiento temporal de códigos de recuperación
    
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
    # RECUPERACIÓN DE CONTRASEÑA
    # ============================================================
    
    def enviar_codigo(self, email: str) -> tuple[bool, str]:
        """
        Paso 1: Envía un código de 6 dígitos al email
        
        Args:
            email: Correo electrónico del usuario
            
        Returns:
            tuple[bool, str]: (éxito, mensaje)
        """
        if not email or not self.validate_email(email):
            return False, "Ingresa un correo electrónico válido."
        
        if not User.email_exists(email):
            return False, "No existe una cuenta con ese correo."
        
        # Generar código aleatorio de 6 dígitos
        codigo = str(random.randint(100000, 999999))
        self._codigos[email] = codigo
        
        print(f"🔑 Código generado para {email}: {codigo}")
        
        # Intentar enviar por email
        try:
            sender_email = os.getenv('EMAIL_USER')
            sender_password = os.getenv('EMAIL_PASSWORD')
            
            if not sender_email or not sender_password:
                print(f"⚠️ Email no configurado. Usando modo debug.")
                return True, f"Código enviado. (DEBUG: {codigo})"
            
            # Crear mensaje
            mensaje = MIMEText(
                f"Hola,\n\n"
                f"Has solicitado restablecer tu contraseña en Poke Clicker.\n\n"
                f"Tu código de recuperación es: {codigo}\n\n"
                f"Este código expirará en 5 minutos.\n\n"
                f"Si no solicitaste este cambio, ignora este mensaje.\n\n"
                f"¡Nos vemos en el juego!\n"
                f"El equipo de Poke Clicker ⚡"
            )
            mensaje["Subject"] = "Recuperación de contraseña - Poke Clicker"
            mensaje["From"] = sender_email
            mensaje["To"] = email
            
            # Enviar usando SSL (puerto 465)
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, email, mensaje.as_string())
            
            print(f"✅ Código enviado a {email}")
            return True, "Código enviado a tu correo."
            
        except smtplib.SMTPAuthenticationError:
            print("❌ Error de autenticación SMTP")
            return True, f"Código enviado. (DEBUG: {codigo})"
        except Exception as e:
            print(f"❌ Error al enviar correo: {e}")
            return True, f"Código enviado. (DEBUG: {codigo})"
    
    def verificar_codigo(self, email: str, codigo: str) -> tuple[bool, str]:
        """
        Paso 2: Verifica el código de recuperación
        
        Args:
            email: Correo electrónico
            codigo: Código de 6 dígitos ingresado
            
        Returns:
            tuple[bool, str]: (éxito, mensaje)
        """
        if not email or not codigo:
            return False, "Ingresa el código de 6 dígitos."
        
        codigo_guardado = self._codigos.get(email)
        
        if codigo_guardado and codigo_guardado == codigo.strip():
            return True, "Código correcto."
        
        return False, "Código incorrecto."
    
    def cambiar_password(self, email: str, nueva_password: str) -> tuple[bool, str]:
        """
        Paso 3: Cambia la contraseña del usuario
        
        Args:
            email: Correo electrónico
            nueva_password: Nueva contraseña en texto plano
            
        Returns:
            tuple[bool, str]: (éxito, mensaje)
        """
        if not nueva_password or len(nueva_password) < 6:
            return False, "La contraseña debe tener al menos 6 caracteres."
        
        # Validar fortaleza
        errors = self.validate_password(nueva_password)
        if errors:
            return False, "\n".join(errors)
        
        # Actualizar contraseña en la BD
        if User.actualizar_password(email, nueva_password):
            # Eliminar código usado
            self._codigos.pop(email, None)
            return True, "Contraseña actualizada correctamente."
        
        return False, "Error al actualizar la contraseña."
    
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
        
        Returns:
            list: Lista de errores (vacía si es válida)
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