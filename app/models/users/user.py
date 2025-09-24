from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import BaseModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    email: str
    contrasenia_hash: str
    rol: str = "user"  

class UserCreate(SQLModel):
    nombre: str
    email: str
    password: str 
    rol: str = "user"

class UserRead(SQLModel):
    nombre: str
    email: str
    rol: str 

