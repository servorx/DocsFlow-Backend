import enum
from sqlalchemy import Column
from sqlalchemy import Enum as SAEnum
from sqlmodel import SQLModel, Field

class RoleEnum(str, enum.Enum):
    admin = "admin"
    operador = "operador"

class Usuario(SQLModel, table=True):
    __tablename__ = "usuarios"

    id: int = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, nullable=False)
    email: str = Field(index=True, nullable=False, unique=True)

    # Campo de rol (Enum) con default en aplicación
    rol: RoleEnum = Field(
        default=RoleEnum.operador,
        sa_column=Column(SAEnum(RoleEnum, name="role_enum", native_enum=False), nullable=False)
    )