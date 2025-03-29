from pydantic import BaseModel
from typing import Optional
from datetime import time

class HorarioBase(BaseModel):
    id_clase: int
    dia: str
    hora_inicio: time
    hora_fin: time


class HorarioCreate(HorarioBase):
    pass

class HorarioResponse(HorarioBase):
    id: int

class HorarioUser(BaseModel):
    id_usuario: int
    id_clase: int


class HorarioClase(BaseModel):
    id: int
    dia: str
    hora_inicio: time
    hora_fin: time
    nombre_clase: str
    clave_clase: str
    nombre_aula: str


class HorarioUpdate(BaseModel):
    dia: Optional[str] = None
    hora_inicio: Optional[time] = None
    hora_fin: Optional[time] = None
    id_clase: Optional[int] = None