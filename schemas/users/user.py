
from pydantic import BaseModel, EmailStr
from typing import Optional

class UsuarioBase(BaseModel):
    num_control: str = None
    nombre: str
    apellido_pat: str
    apellido_mat: str
    telefono: str
    direccion: str
    email: EmailStr
    password: str
    foto: Optional[str] = None
    periodo: Optional[str] = None
    puesto_admin: Optional[str] = None
    semestre: Optional[int] = None
    carrera: Optional[str] = None


class userAuth(BaseModel):
    id_usuario: Optional[int] = None
    num_control: str
    password: str


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido_pat: Optional[str] = None
    apellido_mat: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    email: Optional[EmailStr] = None
    foto: Optional[str] = None
    password: Optional[str] = None
    periodo: Optional[str] = None
    puesto_admin: Optional[str] = None
    semestre: Optional[int] = None
    carrera: Optional[str] = None
