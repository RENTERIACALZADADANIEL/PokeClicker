import bcrypt
import random
import smtplib
import os
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from models.databaseModel import db

# Almacén temporal de códigos: {email: {"codigo": str, "expira": datetime}}
_codigos_pendientes = {}


class AuthController:

    def login(self, email, password):
        cursor = db.get_cursor()
        if not cursor:
            return None, "Error de conexión a la base de datos"
        try:
            cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            user = cursor.fetchone()
            if not user:
                return None, "Correo o contraseña incorrectos"
            if bcrypt.checkpw(password.encode(), user["password"].encode()):
                return user, "Login exitoso"
            return None, "Correo o contraseña incorrectos"
        except Exception as e:
            print(f"Error en login: {e}")
            return None, "Error interno"
        finally:
            cursor.close()

    def registrar_usuario(self, username, email, password):
        cursor = db.get_cursor()
        if not cursor:
            return False, "Error de conexión a la base de datos"
        try:
            cursor.execute("SELECT id_usuario FROM usuarios WHERE email = %s", (email,))
            if cursor.fetchone():
                return False, "El correo ya está registrado"
        except Exception as e:
            print(f"Error en registro: {e}")
            return False, "Error al registrar usuario"
        finally:
            cursor.close()

        cursor2 = db.get_cursor()
        if not cursor2:
            return False, "Error de conexión a la base de datos"
        try:
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12)).decode()
            cursor2.execute(
                "INSERT INTO usuarios (username, email, password) VALUES (%s, %s, %s)",
                (username, email, hashed)
            )
            user_id = cursor2.lastrowid
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"Error en registro: {e}")
            return False, "Error al registrar usuario"
        finally:
            cursor2.close()

        cursor3 = db.get_cursor()
        if not cursor3:
            return True, "¡Registro exitoso!"
        try:
            cursor3.execute("INSERT INTO progreso_juego (id_usuario) VALUES (%s)", (user_id,))
            db.commit()
        except Exception:
            db.rollback()
        finally:
            cursor3.close()
        return True, "¡Registro exitoso!"

    def enviar_codigo(self, email):
        """Paso 1: verifica que el email existe y envía código de 6 dígitos."""
        cursor = db.get_cursor()
        if not cursor:
            return False, "Error de conexión"
        try:
            cursor.execute("SELECT id_usuario FROM usuarios WHERE email = %s", (email,))
            existe = cursor.fetchone()
        except Exception as e:
            return False, "Error al verificar correo"
        finally:
            cursor.close()

        if not existe:
            return False, "No existe una cuenta con ese correo"

        codigo = str(random.randint(100000, 999999))
        _codigos_pendientes[email] = {
            "codigo": codigo,
            "expira": datetime.now() + timedelta(minutes=10)
        }

        ok, msg = self._enviar_email(email, codigo)
        if ok:
            return True, f"Código enviado a {email}"
        return False, msg

    def verificar_codigo(self, email, codigo):
        """Paso 2: verifica que el código sea correcto y no haya expirado."""
        entrada = _codigos_pendientes.get(email)
        if not entrada:
            return False, "No hay código pendiente para este correo"
        if datetime.now() > entrada["expira"]:
            _codigos_pendientes.pop(email, None)
            return False, "El código ha expirado, solicita uno nuevo"
        if entrada["codigo"] != codigo:
            return False, "Código incorrecto"
        return True, "Código verificado correctamente"

    def cambiar_password(self, email, nueva_password):
        """Paso 3: guarda la nueva contraseña hasheada."""
        if email not in _codigos_pendientes:
            return False, "Sesión de recuperación inválida"

        cursor = db.get_cursor()
        if not cursor:
            return False, "Error de conexión"
        try:
            hashed = bcrypt.hashpw(nueva_password.encode(), bcrypt.gensalt(rounds=12)).decode()
            cursor.execute(
                "UPDATE usuarios SET password = %s WHERE email = %s",
                (hashed, email)
            )
            db.commit()
            _codigos_pendientes.pop(email, None)
            return True, "¡Contraseña actualizada correctamente!"
        except Exception as e:
            db.rollback()
            print(f"Error cambiando password: {e}")
            return False, "Error al guardar la contraseña"
        finally:
            cursor.close()

    def _enviar_email(self, destinatario, codigo):
        smtp_email = os.getenv("EMAIL_USER", "")
        smtp_password = os.getenv("EMAIL_PASSWORD", "")
        smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", 587))
        if not smtp_email or not smtp_password:
            print(f"[DEV] Código para {destinatario}: {codigo}")
            return True, "Código generado (ver consola en modo dev)"
        try:
            msg = MIMEText(
                f"Tu código de recuperación de Pokémon Clicker es:\n\n"
                f"  {codigo}\n\n"
                f"Expira en 10 minutos."
            )
            msg["Subject"] = "Código de recuperación - Pokémon Clicker"
            msg["From"] = smtp_email
            msg["To"] = destinatario
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.ehlo()
                server.starttls()
                server.login(smtp_email, smtp_password)
                server.sendmail(smtp_email, destinatario, msg.as_string())
            return True, "Email enviado"
        except Exception as e:
            print(f"Error enviando email: {e}")
            return False, f"No se pudo enviar el correo: {e}"
