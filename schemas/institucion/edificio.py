from pydantic import BaseModel, EmailStr
from typing import Optional

class EdificioBase(BaseModel):
    id_institucion: int
    nombre_edificio: str
    ubicacion_edificio: str

class EdificioUpdate(BaseModel):
    nombre_edificio: Optional[str] = None
    ubicacion_edificio: Optional[str] = None
