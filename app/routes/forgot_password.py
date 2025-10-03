import os
from datetime import datetime

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Form
from pydantic import BaseModel, EmailStr
from sqlmodel import Session, select

from app.utils.email import send_reset_email
from app.models import User
from app.models.forgot_password import ResetPasswordToken
from app.core.database import get_session
from app.auth.validar_password import hash_password

# ================================
# Configuración
# ================================
load_dotenv()
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

router = APIRouter()


# ================================
# Esquemas de entrada
# ================================
class ForgotPasswordRequest(BaseModel):
    email: EmailStr


# ================================
# Rutas
# ================================
@router.post("/forgot-password")
async def forgot_password(
    request: ForgotPasswordRequest,
    session: Session = Depends(get_session)
):
    """Solicitar restablecimiento de contraseña"""
    email = request.email

    # Respuesta genérica (para no revelar si existe o no el usuario)
    generic_response = {
        "message": "Si el correo está registrado, recibirás un enlace para restablecer la contraseña."
    }

    # Buscar usuario
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    if not user or not user.id_user:
        print(f"[DEBUG] Usuario no encontrado para email: {email}")
        return generic_response

    print(f"[DEBUG] Usuario encontrado: {user.email}, generando token")

    # Generar token único
    token_obj = ResetPasswordToken.generate_token(user_id=user.id_user)
    session.add(token_obj)
    session.commit()
    session.refresh(token_obj)

    # Enviar correo
    try:
        await send_reset_email(user.email, token_obj.token, BASE_URL)
        print(f"[DEBUG] Correo enviado a {user.email}")
    except Exception as e:
        print(f"[ERROR] Error enviando correo: {e}")
        raise HTTPException(status_code=500, detail="Error al enviar el correo de recuperación.")

    return generic_response


@router.post("/reset-password")
def reset_password(
    token: str = Form(...),
    new_password: str = Form(...),
    session: Session = Depends(get_session)
):
    """Restablecer contraseña usando token"""
    # Buscar token en la base de datos
    statement = select(ResetPasswordToken).where(ResetPasswordToken.token == token)
    token_obj = session.exec(statement).first()

    if not token_obj:
        raise HTTPException(status_code=400, detail="Token inválido")

    # Buscar usuario asociado
    user_statement = select(User).where(User.id_user == token_obj.user_id)
    user = session.exec(user_statement).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Actualizar contraseña y eliminar token
    user.password = hash_password(new_password)
    session.add(user)
    session.delete(token_obj)
    session.commit()

    return {"msg": "Contraseña actualizada correctamente"}
