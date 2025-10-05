from sqlmodel import Session
from fastapi import HTTPException
from ...models.users.user import User, UserCreate

# obtener usuario actual
def get_me(db: Session, user_id:int):
    return db.query(User).filter(User.id_user == user_id).first()

# obtener todos los usuarios
def get_all_users(db: Session):
    return db.query(User).all()

# obtener usuario por id
def get_user_by_id(db: Session, user_id:int):
    return db.query(User).filter(User.id_user == user_id).first()

# obtener usuarios por departamento
def get_users_by_department(db: Session, department_id:int):
    return db.query(User).filter(User.id_department == department_id).all()

# crear usuario
def create_user(db: Session, user: User):
    if not all([user.name, user.email, user.password, user.role, user.id_department]):
        raise HTTPException(
            status_code=400,
            detail="Todos los campos son obligatorios y no pueden ser nulos."
            )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# actualizar usuario
def update_user_by_id(db: Session, user_id: int, new_data: UserCreate):
    user = db.query(User).filter(User.id_user == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    user.name = new_data.name
    user.email = new_data.email
    user.password = new_data.password
    user.role = new_data.role
    user.id_department = new_data.id_department

    db.commit()
    db.refresh(user)
    return user


# borrar usuario
def delete_user_by_id(db: Session, user_id:int):
    user = db.query(User).filter(User.id_user == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user