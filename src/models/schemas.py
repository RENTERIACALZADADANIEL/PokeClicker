from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional
from datetime import datetime

class UserRegisterSchema(BaseModel):
    """Schema para registro de usuarios"""
    username: str = Field(..., min_length=3, max_length=50, description="Nombre de usuario")
    email: EmailStr = Field(..., description="Correo electrónico válido")
    password: str = Field(..., min_length=6, max_length=50, description="Contraseña")
    confirm_password: str = Field(..., description="Confirmar contraseña")
    
    @validator('username')
    def username_alphanumeric(cls, v):
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('El username solo puede contener letras, números, guiones y guiones bajos')
        return v.strip()
    
    @validator('password')
    def password_strength(cls, v):
        """Valida la fortaleza de la contraseña"""
        import re
        if len(v) < 6:
            raise ValueError('La contraseña debe tener al menos 6 caracteres')
        if not re.search(r'[A-Z]', v):
            raise ValueError('La contraseña debe contener al menos una mayúscula')
        if not re.search(r'[a-z]', v):
            raise ValueError('La contraseña debe contener al menos una minúscula')
        if not re.search(r'\d', v):
            raise ValueError('La contraseña debe contener al menos un número')
        return v
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Las contraseñas no coinciden')
        return v

class UserLoginSchema(BaseModel):
    """Schema para inicio de sesión"""
    email: EmailStr = Field(..., description="Correo electrónico")
    password: str = Field(..., min_length=1, description="Contraseña")
    
    @validator('email')
    def email_not_empty(cls, v):
        if not v.strip():
            raise ValueError('El email no puede estar vacío')
        return v

class UserResponseSchema(BaseModel):
    """Schema para respuestas de usuario (sin contraseña)"""
    id_usuario: int
    username: str
    email: str
    fecha_registro: datetime
    
    class Config:
        from_attributes = True

class PasswordResetRequestSchema(BaseModel):
    """Schema para solicitar recuperación de contraseña"""
    email: EmailStr = Field(..., description="Correo electrónico para recuperación")

class PasswordResetSchema(BaseModel):
    """Schema para restablecer contraseña con token"""
    token: str = Field(..., min_length=1, description="Token de recuperación")
    new_password: str = Field(..., min_length=6, max_length=50, description="Nueva contraseña")
    confirm_password: str = Field(..., description="Confirmar nueva contraseña")
    
    @validator('new_password')
    def password_strength(cls, v):
        """Valida la fortaleza de la contraseña"""
        import re
        if len(v) < 6:
            raise ValueError('La contraseña debe tener al menos 6 caracteres')
        if not re.search(r'[A-Z]', v):
            raise ValueError('La contraseña debe contener al menos una mayúscula')
        if not re.search(r'[a-z]', v):
            raise ValueError('La contraseña debe contener al menos una minúscula')
        if not re.search(r'\d', v):
            raise ValueError('La contraseña debe contener al menos un número')
        return v
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Las contraseñas no coinciden')
        return v

class TokenPayload(BaseModel):
    """Schema para el payload del token JWT"""
    user_id: int
    email: str
    exp: datetime
    iat: datetime
    type: str = 'password_reset'
