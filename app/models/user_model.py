from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    nombre: str
    apellido: str
    cedula: str
    edad: int
    email: EmailStr
    contrasena: str
    id_rol: int
    id_barrio: int

class UserUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    edad: Optional[int] = None
    email: Optional[EmailStr] = None
    id_rol: Optional[int] = None
    id_barrio: Optional[int] = None
    estado: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    contrasena: str

class UserResponse(BaseModel):
    id: int
    nombre: str
    apellido: str
    email: EmailStr
    edad: int
    estado: str