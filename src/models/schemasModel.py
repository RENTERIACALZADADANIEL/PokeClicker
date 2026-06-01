


from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UsuarioSchema(BaseModel):
   
    email: EmailStr
    password: str = Field(min_length=8)

class RegistroSchema(UsuarioSchema):
    
    nombre: str = Field(min_length=3, max_length=100)

class TareaSchema(BaseModel):
    titulo: str = Field(min_length=1, max_length=200)
    descripcion: Optional[str] = None
    prioridad: str = "media"
    clasificacion: str = "personal"