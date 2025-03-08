from schemas.users.user import UsuarioBase, UsuarioUpdate
from typing import Optional
from pydantic import BaseModel


class AdministradorBase(UsuarioBase):
    id_usuario: Optional[int] = None
    puesto_admin: str


class AdministradorUpdate(UsuarioUpdate):
    puesto_admin: Optional[str] = None
