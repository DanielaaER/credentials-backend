
from pydantic import BaseModel
from typing import Optional


class AulaBase(BaseModel):
    id_edificio: int
    nombre_aula: str

class AulaUpdate(BaseModel):
    nombre_aula: Optional[str] = None
