import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")

def send_reset_email(to_email: str, reset_link: str):
    subject = "Restablece tu contraseña"
    body = f"""
    Hola 👋,

    Hemos recibido una solicitud para restablecer tu contraseña.
    Haz clic en el siguiente enlace para continuar:

    {reset_link}

    Este enlace expirará en 15 minutos.

    Si no solicitaste este cambio, ignora este correo.
    """

    msg = MIMEMultipart()
    msg["From"] = SMTP_USER
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()  # Seguridad
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, to_email, msg.as_string())
        print(f"[DEBUG] Correo enviado a {to_email}")
    except Exception as e:
        print(f"[ERROR] No se pudo enviar el correo: {e}")
