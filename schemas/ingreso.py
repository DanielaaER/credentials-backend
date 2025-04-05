
from pydantic import BaseModel, EmailStr
from typing import Optional

class IngresoBase(BaseModel):
    id_ingreso: Optional[int]
    id_usuario: int
    id_institucion: int
    id_clase: int
    fecha_ingreso: date
    hora_ingreso: time
    typo_ingreso: bool

class IngresoLista(BaseModel):
    id_ingreso: int
    id_usuario: int
    id_institucion: int
    id_clase: int
    fecha_ingreso: date
    hora_ingreso: time
    typo_ingreso: bools