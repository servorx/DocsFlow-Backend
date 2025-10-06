from fastapi import APIRouter, Depends, HTTPException

from app.models.users.user import User, UserCreate
from ..verification.verificar_administracion import admin_required
from sqlmodel  import Session
from ...core.database import get_session
from ...controllers.user.users_controllers import get_all_users_controller, delete_user_by_id_controller, create_user_controller, update_user_by_id_controller, get_me_controller, get_user_by_id_controller, get_users_by_department_controller
from ...auth.dependencias import get_current_user

router = APIRouter(tags=["Users"])

# obtener usuario actual
@router.get("/me")
def read_me(
    db: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=400, detail="ID de usuario no encontrado en el token")
    user = get_me_controller(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

# obtener todos los usuarios
@router.get("/all", dependencies=[Depends(admin_required)])
def read_users(db: Session = Depends(get_session)):
    return get_all_users_controller(db)

# obtener usuario por id 
@router.get("/{user_id}")
def read_user_by_id(user_id: int, db: Session = Depends(get_session)):
    return get_user_by_id_controller(db, user_id)

# obtener usuarios por departamento
@router.get("/department/{department_id}")
def read_users_by_department(department_id: int, db: Session = Depends(get_session)):
    return get_users_by_department_controller(db, department_id)

# crear usuario
@router.post("/create", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_session)):
    return create_user_controller(db, user)

# actualizar usuario por id
@router.put("/{user_id}")
def update_user_by_id(user_id: int, user: dict, db: Session = Depends(get_session)):
    return update_user_by_id_controller(db, user_id, user)

# borrar usuario por id
@router.delete("/{user_id}")
def remove_user(user_id: int, db: Session = Depends(get_session)):
    return delete_user_by_id_controller(db, user_id)

# TODO: acordarme de volverles a colocar la dependencia de admin_required a las rutas de arriba menos a la de create 
