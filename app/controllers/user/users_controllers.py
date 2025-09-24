from sqlmodel import Session
from fastapi import HTTPException
from ...models.users import User

def create_users(db: Session, user: User):
    if not all([user.usuario_id, user.room_id, user.fecha,
            user.hora_inicio, user.hora_fin, user.estado]):
        raise HTTPException(
            status_code=400,
            detail="Todos los campos son obligatorios y no pueden ser nulos."
            )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(db: Session):
    return db.query(User).all()

def get_user_by_id(db: Session, user_id:int):
    return db.query(User).filter(User.id == user_id).first()

def delete_user_by_id(db: Session, user_id:int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user
