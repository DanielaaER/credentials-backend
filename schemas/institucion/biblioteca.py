
from pydantic import BaseModel, EmailStr
from typing import Optional

class BibliotecaBase(BaseModel):
    id_institucion: int
    nombre_biblioteca: str

class BibliotecaUpdate(BaseModel):
    nombre_biblioteca: Optional[str] = None
