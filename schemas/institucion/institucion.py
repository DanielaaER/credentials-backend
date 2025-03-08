
from pydantic import BaseModel, EmailStr
from typing import Optional

class InstitucionBase(BaseModel):
    nombre_institucion: str
    telefono_institucion: str
    ubicacion_institucion: str


class InstitucionUpdate(BaseModel):
    nombre_institucion: Optional[str] = None
    telefono_institucion: Optional[str] = None
    ubicacion_institucion: Optional[str] = None

