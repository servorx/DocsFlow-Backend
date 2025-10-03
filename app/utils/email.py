import os
from dotenv import load_dotenv
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from fastapi_mail.schemas import MessageType
from fastapi_mail.errors import ConnectionErrors
from datetime import datetime, timedelta

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("SMTP_USER"),
    MAIL_PASSWORD=os.getenv("SMTP_PASS"),
    MAIL_FROM=os.getenv("SMTP_USER"),  # el mismo gmail
    MAIL_PORT=int(os.getenv("SMTP_PORT", 587)),
    MAIL_SERVER=os.getenv("SMTP_HOST", "smtp.gmail.com"),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

async def send_reset_email(to_email: str, token: str, base_url: str = "http://localhost:8000"):
    subject = "Recuperación de contraseña"
    expiry = datetime.utcnow() + timedelta(minutes=15)
    reset_link = f"{base_url}/reset-password?token={token}"

    body = f"""
    Hola 👋,

    Hemos recibido una solicitud para restablecer tu contraseña.
    Haz clic en el siguiente enlace:

    {reset_link}

    Este enlace expirará a las {expiry.strftime('%Y-%m-%d %H:%M:%S UTC')}.
    Si no solicitaste este cambio, ignora este mensaje.
    """

    message = MessageSchema(
        subject=subject,
        recipients=[to_email],
        body=body,
        subtype=MessageType.plain
    )

    try:
        fm = FastMail(conf)
        await fm.send_message(message)
        print(f"[DEBUG] Correo enviado exitosamente a {to_email}")
    except ConnectionErrors as e:
        print(f"[ERROR] Error de conexión al enviar correo: {e}")
    except Exception as e:
        print(f"[ERROR] No se pudo enviar el correo: {e}")
