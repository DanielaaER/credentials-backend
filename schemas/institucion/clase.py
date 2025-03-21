
from pydantic import BaseModel
from typing import Optional


class ClaseBase(BaseModel):
    id_aula: int
    clave_clase: str
    nombre_clase: str


class ClaseResponse(BaseModel):
    id: int
    id_aula: int
    clave_clase: str
    nombre_clase: str


class ClaseUpdate(BaseModel):
    clave_clase: Optional[str] = None
    nombre_clase: Optional[str] = None
    id_aula: Optional[int] = None



