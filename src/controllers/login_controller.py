import bcrypt
import re
import logging
from typing import Tuple, Optional, Dict, Union

logger = logging.getLogger(__name__)

class LoginController:
    def __init__(self, model):
        self.model = model
    
    def _validar_email(self, email: str) -> bool:
        """Valida el formato del email"""
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(patron, email) is not None
    
    def _validar_password_fortaleza(self, password: str) -> Tuple[bool, str]:
        """Valida la fortaleza de la contraseña"""
        if len(password) < 6:
            return False, "La contraseña debe tener al menos 6 caracteres"
        return True, ""
    
    def verificar_credenciales(self, email: str, password: str) -> Union[Dict, str]:
        """Lógica para iniciar sesión. Concuerda con el formato str de la vista."""
        # Validaciones básicas
        if not email or not password:
            return "Por favor, completa todos los campos."
        
        if not self._validar_email(email):
            return "Formato de email inválido."
        
        try:
            # Consulta a la base de datos a través del modelo
            usuario = self.model.obtener_usuario_por_email(email)
            
            if not usuario:
                logger.warning(f"Intento de login con email no registrado: {email}")
                return "El correo electrónico no está registrado."
            
            # Verificar contraseña contra el hash almacenado en la base de datos
            password_bytes = password.encode('utf-8')
            hash_bytes = usuario['password'].encode('utf-8')
            
            if bcrypt.checkpw(password_bytes, hash_bytes):
                logger.info(f"Login exitoso para: {email}")
                return usuario  # Retorna el diccionario del usuario tal como viene de la BD
            
            logger.warning(f"Contraseña incorrecta para: {email}")
            return "Contraseña incorrecta."
            
        except Exception as e:
            logger.error(f"Error en verificación de credenciales: {e}")
            return "Error del servidor. Intente nuevamente."
    
    def crear_cuenta(self, username: str, email: str, password: str) -> Union[bool, str]:
        """Lógica para registrar un nuevo usuario en la base de datos."""
        # Validaciones
        if not username or not email or not password:
            return "Todos los campos son obligatorios."
        
        if len(username) < 3:
            return "El nombre de usuario debe tener al menos 3 caracteres."
        
        if not self._validar_email(email):
            return "Formato de email inválido."
        
        es_valida, msg = self._validar_password_fortaleza(password)
        if not es_valida:
            return msg
        
        try:
            # Verificar duplicados en la base de datos
            if self.model.obtener_usuario_por_email(email):
                return "Este correo ya está en uso."
            
            # Hashear contraseña para almacenar de forma segura
            salt = bcrypt.gensalt(rounds=12)  # 12 rounds es más seguro
            password_hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
            password_hashed_str = password_hashed.decode('utf-8')
            
            # Registrar nuevo registro en la base de datos
            exito = self.model.registrar_usuario(username, email, password_hashed_str)
            
            if exito:
                logger.info(f"Nuevo usuario registrado: {email}")
                return True
            
            return "Error al registrar en la base de datos."
            
        except Exception as e:
            logger.error(f"Error en registro de usuario: {e}")
            return "Error inesperado del servidor."