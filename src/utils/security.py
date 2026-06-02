import bcrypt
import secrets
import string
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

# Configuración
TOKEN_EXPIRATION = int(os.getenv('TOKEN_EXPIRATION_MINUTES', '5'))  # 5 minutos
DEBUG_MODE = os.getenv('DEBUG_MODE', 'false').lower() == 'true'

# Almacenamiento temporal de tokens (en producción usar BD o Redis)
_reset_tokens = {}  # {token: {"user_id": 1, "email": "...", "expires": datetime}}


# FUNCIONES DE CONTRASEÑA

def hash_password(password: str) -> str:
   
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    
    try:
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    except Exception:
        return False


# FUNCIONES DE TOKEN (6 caracteres)

def generate_reset_token() -> str:
   
    alphabet = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(6))

def store_reset_token(user_id: int, email: str) -> str:
   
    # Limpiar tokens expirados primero
    clean_expired_tokens()
    
    # Generar token unico 
    token = generate_reset_token()
    while token in _reset_tokens:
        token = generate_reset_token()
    
    # Almacenar token con expiración
    _reset_tokens[token] = {
        "user_id": user_id,
        "email": email,
        "expires": datetime.now() + timedelta(minutes=TOKEN_EXPIRATION)
    }
    
    return token

def verify_reset_token(token: str) -> dict | None:
   
    # Limpiar tokens expirados
    clean_expired_tokens()
    
    # Buscar token
    token_data = _reset_tokens.get(token)
    
    if not token_data:
        return None
    
    # Verificar expiración
    if datetime.now() > token_data["expires"]:
        del _reset_tokens[token]
        return None
    
    return {
        "user_id": token_data["user_id"],
        "email": token_data["email"]
    }

def delete_reset_token(token: str):
   
    if token in _reset_tokens:
        del _reset_tokens[token]

def clean_expired_tokens():
    
    now = datetime.now()
    expired = [t for t, d in _reset_tokens.items() if now > d["expires"]]
    for token in expired:
        del _reset_tokens[token]


# FUNCIONES DE EMAIL


def send_reset_email(email: str, token: str, username: str) -> bool:
   
    # Si estamos en modo debug, mostramos el token en consola
    if DEBUG_MODE:
        print(f"""
        ╔══════════════════════════════════════════════════════╗
        ║         CORREO DE RECUPERACIÓN (MODO DEBUG)         ║
        ╠══════════════════════════════════════════════════════╣
        ║  Para: {email:<44}║
        ║  Usuario: {username:<41}║
        ║  Token: {token:<45}║
        ║  Expira en: {TOKEN_EXPIRATION} minutos{'':<35}║
        ╚══════════════════════════════════════════════════════╝
        """)
    
    try:
        sender_email = os.getenv('EMAIL_USER')
        sender_password = os.getenv('EMAIL_PASSWORD')
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', '587'))
        
        # Verificar credenciales
        if not sender_email or not sender_password:
            print("⚠️ Credenciales de email no configuradas en .env")
            if DEBUG_MODE:
                print(f"🔑 Token para recuperación: {token}")
            return False
        
        # Crear mensaje
        message = MIMEMultipart("alternative")
        message["Subject"] = "Recuperación de Contraseña - Poke Clicker"
        message["From"] = f"Poke Clicker <{sender_email}>"
        message["To"] = email
        
        # Plantilla HTML del correo
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 20px; }}
                .container {{ max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
                .header {{ text-align: center; color: #E53935; font-size: 24px; font-weight: bold; margin-bottom: 20px; }}
                .content {{ color: #333; line-height: 1.6; }}
                .token-box {{ background: #FFF3CD; border: 2px dashed #FFC107; padding: 20px; border-radius: 10px; text-align: center; margin: 20px 0; }}
                .token {{ font-family: 'Courier New', monospace; font-size: 36px; font-weight: bold; color: #E53935; letter-spacing: 8px; }}
                .warning {{ background-color: #FFF3CD; color: #856404; padding: 15px; border-radius: 5px; margin: 20px 0; border-left: 4px solid #FFC107; }}
                .footer {{ text-align: center; color: #999; font-size: 12px; margin-top: 30px; border-top: 1px solid #eee; padding-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">🔑 Recupera tu Contraseña</div>
                <div class="content">
                    <p>Hola <strong>{username}</strong>,</p>
                    <p>Has solicitado restablecer tu contraseña en <strong>Poke Clicker</strong>.</p>
                    <p>Usa el siguiente código en la aplicación:</p>
                    
                    <div class="token-box">
                        <p style="margin:0; color:#666; font-size:14px;">Tu código de recuperación:</p>
                        <div class="token">{token}</div>
                    </div>
                    
                    <div class="warning">
                        <strong>⚠️ Importante:</strong>
                        <ul style="margin: 5px 0; padding-left: 20px;">
                            <li>Este código expirará en <strong>{TOKEN_EXPIRATION} minutos</strong></li>
                            <li>Si no solicitaste este cambio, ignora este mensaje</li>
                            <li>Nunca compartas este código con nadie</li>
                        </ul>
                    </div>
                    
                    <p>¡Nos vemos en el juego!</p>
                    <p>El equipo de <strong>Poke Clicker</strong> ⚡</p>
                </div>
                <div class="footer">
                    <p>Este es un correo automático, por favor no respondas a este mensaje.</p>
                    <p>© 2024 Poke Clicker. Todos los derechos reservados.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        message.attach(MIMEText(html, "html"))
        
        # Enviar correo
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, message.as_string())
        
        print(f"✅ Correo enviado exitosamente a {email}")
        return True
        
    except smtplib.SMTPAuthenticationError:
        print(" Error de autenticación: Verifica tu email y contraseña de aplicación")
        return False
    except smtplib.SMTPException as e:
        print(f" Error SMTP: {e}")
        return False
    except Exception as e:
        print(f" Error inesperado al enviar correo: {e}")
        return False