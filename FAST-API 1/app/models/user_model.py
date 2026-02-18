from pydantic import BaseModel

class UserLogin(BaseModel):
    usuario: str
    contrasena: str
