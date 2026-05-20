import bcrypt
import jwt
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY', 'poke_clicker_default_secret_key_2024')
TOKEN_EXPIRATION = int(os.getenv('TOKEN_EXPIRATION_MINUTES', '5'))
ALGORITHM = "HS256"
DEBUG_MODE = os.getenv('DEBUG_MODE', 'false').lower() == 'true'

def hash_password(password: str) -> str:
    """Hashea una contraseña usando bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def generate_token(user_id: int, email: str) -> str:
    """Genera un token JWT para recuperación de contraseña"""
    payload = {
        'user_id': user_id,
        'email': email,
        'exp': datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRATION),
        'iat': datetime.now(timezone.utc),
        'type': 'password_reset'
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> dict:
    """Verifica y decodifica un token JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get('type') != 'password_reset':
            return None
        return payload
    except jwt.ExpiredSignatureError:
        print("❌ Token expirado")
        return None
    except jwt.InvalidTokenError:
        print("❌ Token inválido")
        return None

def send_reset_email(email: str, token: str, username: str) -> bool:
    """
    Envía un correo de recuperación de contraseña
    Returns: True si se envió correctamente, False si hubo error
    """
    # Enlace que abrirá la aplicación Flet
    reset_link = f"http://localhost:8550?token={token}"
    
    # Si estamos en modo debug, mostramos el token en consola
    if DEBUG_MODE:
        print(f"""
        ╔══════════════════════════════════════════════════════╗
        ║         CORREO DE RECUPERACIÓN (MODO DEBUG)         ║
        ╠══════════════════════════════════════════════════════╣
        ║  Para: {email:<44}║
        ║  Usuario: {username:<41}║
        ║  Token: {token:<45}║
        ║  Enlace: {reset_link:<43}║
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
                .header {{ text-align: center; color: #1976D2; font-size: 24px; font-weight: bold; margin-bottom: 20px; }}
                .content {{ color: #333; line-height: 1.6; }}
                .button {{ display: inline-block; background-color: #1976D2; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; font-weight: bold; }}
                .warning {{ background-color: #FFF3CD; color: #856404; padding: 15px; border-radius: 5px; margin: 20px 0; border-left: 4px solid #FFC107; }}
                .token-box {{ background: #f5f5f5; padding: 15px; border-radius: 5px; font-family: 'Courier New', monospace; font-size: 12px; word-break: break-all; margin: 20px 0; }}
                .footer {{ text-align: center; color: #999; font-size: 12px; margin-top: 30px; border-top: 1px solid #eee; padding-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">🔑 Recupera tu Contraseña</div>
                <div class="content">
                    <p>Hola <strong>{username}</strong>,</p>
                    <p>Hemos recibido una solicitud para restablecer la contraseña de tu cuenta en <strong>Poke Clicker</strong>.</p>
                    
                    <center>
                        <a href="{reset_link}" class="button">🔗 Restablecer Contraseña</a>
                    </center>
                    
                    <p>Si el botón no funciona, copia y pega este enlace en tu navegador:</p>
                    <p style="color: #1976D2; word-break: break-all; font-size: 13px;">{reset_link}</p>
                    
                    <p><strong>O también puedes usar este token directamente en la aplicación:</strong></p>
                    <div class="token-box">{token}</div>
                    
                    <div class="warning">
                        <strong>⚠️ Importante:</strong>
                        <ul style="margin: 5px 0; padding-left: 20px;">
                            <li>Este enlace expirará en <strong>{TOKEN_EXPIRATION} minutos</strong></li>
                            <li>Si no solicitaste este cambio, ignora este mensaje</li>
                            <li>Nunca compartas este enlace con nadie</li>
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
        print("❌ Error de autenticación: Verifica tu email y contraseña de aplicación")
        if DEBUG_MODE:
            print(f"🔑 Token para recuperación: {token}")
        return False
    except smtplib.SMTPException as e:
        print(f"❌ Error SMTP: {e}")
        if DEBUG_MODE:
            print(f"🔑 Token para recuperación: {token}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado al enviar correo: {e}")
        if DEBUG_MODE:
            print(f"🔑 Token para recuperación: {token}")
        return False