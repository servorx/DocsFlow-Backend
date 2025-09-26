from app.utils.email import send_reset_email

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models import User
from app.models.reset_password_tokens import ResetPasswordToken
from app.models.forgot_password import ForgotPasswordRequest
from app.core.database import get_session

router = APIRouter()
@router.post("/auth/forgot-password")
def forgot_password(data: ForgotPasswordRequest, session: Session = Depends(get_session)):
    statement = select(User).where(User.email == data.email)
    user = session.exec(statement).first()

    generic_response = {
        "message": "Si el correo está registrado, recibirás un enlace para restablecer la contraseña."
    }

    if not user:
        return generic_response

    token_obj = ResetPasswordToken.generate_token(user_id=user.id)
    session.add(token_obj)
    session.commit()
    session.refresh(token_obj)

    reset_link = f"http://localhost:8000/reset-password?token={token_obj.token}"

    # 🚀 Enviar el correo real
    send_reset_email(user.email, reset_link)

    return generic_response
