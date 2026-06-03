from pydantic import BaseModel, EmailStr, Field, field_validator

_TLDS_VALIDOS = {
    "com", "org", "net", "edu", "gov", "mx", "es", "io", "co",
    "info", "biz", "us", "uk", "ca", "de", "fr", "jp", "br", "ar"
}

_TLDS_COMPUESTOS = {"edu.mx", "com.mx"}

class UsuarioSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

    @field_validator("email")
    @classmethod
    def email_dominio_valido(cls, v):
        dominio = v.split("@")[-1].lower()
        # Verificar TLD compuesto primero
        for tld_c in _TLDS_COMPUESTOS:
            if dominio.endswith(tld_c):
                return v
        tld = dominio.split(".")[-1]
        if tld not in _TLDS_VALIDOS:
            raise ValueError("TLD inválido")
        return v

class RegistroSchema(UsuarioSchema):
    nombre: str = Field(min_length=3, max_length=100)
