from pydantic import BaseModel, EmailStr


class User(BaseModel):
    nombre: str
    apellido: str
    cedula: str
    edad: int
    email: EmailStr
    contrasena: str


class UserLogin(BaseModel):
    usuario: EmailStr
    contrasena: str



