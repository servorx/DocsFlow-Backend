from sqlmodel import Session
from fastapi import HTTPException
from ...models.users.user import User, UserCreate

# obtener usuario actual
def get_me_controller(db: Session, user_id:int):
    return db.query(User).filter(User.id_user == user_id).first()

# obtener todos los usuarios
def get_all_users_controller(db: Session):
    return db.query(User).all()

# obtener usuario por id
def get_user_by_id_controller(db: Session, user_id:int):
    return db.query(User).filter(User.id_user == user_id).first()

# obtener usuarios por departamento
def get_users_by_department_controller(db: Session, department_id:int):
    return db.query(User).filter(User.id_department == department_id).all()

# crear usuario
def create_user_controller(db: Session, user: UserCreate):
    if not all([user.name, user.email, user.password, user.role, user.id_department]):
        raise HTTPException(
            status_code=400,
            detail="Todos los campos son obligatorios y no pueden ser nulos."
        )

    # Crear instancia del modelo mapeado a tabla
    new_user = User(
        name=user.name,
        email=user.email,
        password=user.password,
        role=user.role,
        id_department=user.id_department,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# actualizar usuario
def update_user_by_id_controller(db: Session, user_id: int, new_data: dict):
    user = db.query(User).filter(User.id_user == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    for key, value in new_data.items():
        if hasattr(user, key) and value is not None:
            setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user



# borrar usuario
def delete_user_by_id_controller(db: Session, user_id:int):
    user = db.query(User).filter(User.id_user == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user