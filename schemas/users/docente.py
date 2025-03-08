from schemas.users.user import UsuarioBase, UsuarioUpdate
from typing import Optional
from pydantic import BaseModel

class DocenteBase(UsuarioBase):
    id_usuario: Optional[int] = None
    periodo: str


class DocenteUpdate(UsuarioUpdate):
    periodo: Optional[str] = None
