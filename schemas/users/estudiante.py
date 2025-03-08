from schemas.users.user import UsuarioBase, UsuarioUpdate
from typing import Optional
from pydantic import BaseModel

class EstudianteBase(UsuarioBase):
    id_usuario: Optional[int] = None
    semestre: int
    carrera: str


class EstudianteClase(BaseModel):
    num_control: str
    nombre: str
    apellido_pat: str
    apellido_mat: str


class EstudianteUpdate(UsuarioUpdate):
    semestre: Optional[int] = None
    carrera: Optional[str] = None

