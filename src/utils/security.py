import bcrypt
import jwt
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY', 'tu_clave_secreta_muy_segura')
ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    """Hashea una contraseña usando bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def generate_token(user_id: int, email: str, expiration_hours: int = 24) -> str:
    """Genera un token JWT para recuperación de contraseña"""
    payload = {
        'user_id': user_id,
        'email': email,
        'exp': datetime.utcnow() + timedelta(hours=expiration_hours),
        'iat': datetime.utcnow(),
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
        print("Token expirado")
        return None
    except jwt.InvalidTokenError:
        print("Token inválido")
        return None

def send_reset_email(email: str, token: str, username: str) -> bool:
    """Envía un correo de recuperación de contraseña"""
    try:
        sender_email = os.getenv('EMAIL_USER', 'tu_correo@gmail.com')
        sender_password = os.getenv('EMAIL_PASSWORD', 'tu_contraseña_app')
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', 587))
        
        reset_link = f"http://localhost:8000/reset-password?token={token}"
        
        message = MIMEMultipart("alternative")
        message["Subject"] = "Recuperación de Contraseña - Poke Clicker"
        message["From"] = sender_email
        message["To"] = email
        
        html = f"""
        <html>
          <body>
            <h2>¡Recupera tu contraseña de Poke Clicker!</h2>
            <p>Hola {username},</p>
            <p>Has solicitado restablecer tu contraseña. Haz clic en el siguiente enlace:</p>
            <p><a href="{reset_link}">Restablecer Contraseña</a></p>
            <p>Este enlace expirará en 24 horas.</p>
            <p>Si no solicitaste esto, ignora este mensaje.</p>
          </body>
        </html>
        """
        
        message.attach(MIMEText(html, "html"))
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, message.as_string())
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False