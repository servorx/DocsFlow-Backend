from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from datetime import timedelta
from jose import jwt, JWTError

from ...auth.validar_password import hash_password, verify_password
from ...models.users.user import UserCreate, User
from ...core.database import get_session
from ...auth.jwt_hand import create_access_token, SECRET_KEY, ALGORITHM

router = APIRouter(tags=["Auth"])

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_session)):
    existe = select(User).where(User.email == user.email)
    result = db.exec(existe).first()
    if result:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    password_hash = hash_password(user.password)

    new_user = User(
        name=user.name,
        email=user.email,
        password=password_hash,
        role=user.role,
        id_department=user.id_department
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"msg": "Usuario registrado con éxito", "user_id": new_user.id_user}


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    if not form_data.username or not form_data.password:
        raise HTTPException(status_code=400, detail="Username y password requeridos")
    user = db.exec(select(User).where(User.email == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    token = create_access_token(data={"sub": user.email, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/forgot-password")
def forgot_password(email: str, db: Session = Depends(get_session)):
    user = db.exec(select(User).where(User.email == email)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    reset_token = create_access_token(
        {"sub": user.email},
        expires_delta=timedelta(minutes=15)  
    )
    return {
        "msg": "Se enviaron instrucciones al correo",
        "reset_token_demo": reset_token  
    }
@router.post("/reset-password")
def reset_password(token: str, new_password: str, db: Session = Depends(get_session)):
    try:
        payload = jwt.decode(token, SECRET_KEY or "", algorithms=[ALGORITHM or "HS256"])
        email: str = payload.get("sub")
        if not email:
            raise HTTPException(status_code=400, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=400, detail="Token inválido o expirado")

    user = db.exec(select(User).where(User.email == email)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    user.password = hash_password(new_password)
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"msg": "Contraseña actualizada correctamente"}
