# app/models/user_model.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    nombre: str
    apellido: str
    cedula: str
    edad: int
    usuario: EmailStr
    contrasena: str

class UserLogin(BaseModel):
    usuario: EmailStr
    contrasena: str

class UserResponse(BaseModel):
    id: int
    nombre: str
    apellido: str
    usuario: EmailStr




