from fastapi import APIRouter, HTTPException, Depends
from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
from typing import List
from repositories.institucion.institucion import Institucion
from repositories.institucion.biblioteca import Biblioteca
from repositories.institucion.edificio import Edificio
from repositories.institucion.aula import Aula
from repositories.institucion.clase import Clase

from schemas.institucion.aula import AulaBase, AulaUpdate
from schemas.institucion.biblioteca import BibliotecaBase, BibliotecaUpdate
from schemas.institucion.edificio import EdificioBase, EdificioUpdate
from schemas.institucion.clase import ClaseBase, ClaseUpdate
from schemas.institucion.institucion import InstitucionBase, InstitucionUpdate

institucionRouter = APIRouter()

# -----------------------------
# BIBLIOTECAS
# -----------------------------
@institucionRouter.post("/instituciones/bibliotecas", response_model=dict)
def create_biblioteca(biblioteca: BibliotecaBase):
    return Biblioteca().guardar(biblioteca)

@institucionRouter.get("/instituciones/bibliotecas", response_model=List[dict])
def get_bibliotecas():
    return Biblioteca().obtener_todos()

@institucionRouter.get("/instituciones/bibliotecas/{id}", response_model=dict)
def get_biblioteca(id: int):
    return Biblioteca().mostrar_informacion(id)

@institucionRouter.patch("/instituciones/bibliotecas/{id}", response_model=dict)
def update_biblioteca(id: int, biblioteca: BibliotecaUpdate):
    return Biblioteca().actualizar(id, biblioteca)

@institucionRouter.delete("/instituciones/bibliotecas/{id}", response_model=dict)
def delete_biblioteca(id: int):
    return Biblioteca().eliminar(id)

# -----------------------------
# EDIFICIOS
# -----------------------------
@institucionRouter.post("/instituciones/edificios", response_model=dict)
def create_edificio(edificio: EdificioBase):
    return Edificio().guardar(edificio)

@institucionRouter.get("/instituciones/edificios", response_model=List[dict])
def get_edificios():
    return Edificio().obtener_todos()

@institucionRouter.get("/instituciones/edificios/{id}", response_model=dict)
def get_edificio(id: int):
    return Edificio().mostrar_informacion(id)

@institucionRouter.patch("/instituciones/edificios/{id}", response_model=dict)
def update_edificio(id: int, edificio: EdificioUpdate):
    return Edificio().actualizar(id, edificio)

@institucionRouter.delete("/instituciones/edificios/{id}", response_model=dict)
def delete_edificio(id: int):
    return Edificio().eliminar(id)

# -----------------------------
# AULAS
# -----------------------------
@institucionRouter.post("/instituciones/edificios/aulas", response_model=dict)
def create_aula(aula: AulaBase):
    return Aula().guardar(aula)

@institucionRouter.get("/instituciones/edificios/aulas/all", response_model=List[dict])
def get_aulas():
    return Aula().obtener_todos()

@institucionRouter.get("/instituciones/edificios/aulas/{id}", response_model=dict)
def get_aula(id: int):
    return Aula().mostrar_informacion(id)

@institucionRouter.patch("/instituciones/edificios/aulas/{id}", response_model=dict)
def update_aula(id: int, aula: AulaUpdate):
    return Aula().actualizar(id, aula)

@institucionRouter.delete("/instituciones/edificios/aulas/{id}", response_model=dict)
def delete_aula(id: int):
    return Aula().eliminar(id)

# -----------------------------
# CLASES
# -----------------------------
@institucionRouter.post("/instituciones/edificios/aulas/clase", response_model=dict)
def create_clase(clase: ClaseBase):
    return Clase().guardar(clase)


@institucionRouter.get("/instituciones/edificios/aulas/clase/all", response_model=List[dict])
def get_all_clases():
    return Clase().obtener_todas_clases()

@institucionRouter.get("/instituciones/edificios/aulas/clase/{id}", response_model=dict)
def get_clase(id: int):
    return Clase().mostrar_informacion(id)


@institucionRouter.get("/instituciones/edificios/aulas/{id}/clase", response_model=List[dict])
def get_clases(id: int):
    return Clase().obtener_todos(id)

@institucionRouter.patch("/instituciones/edificios/aulas/clase/{clase_id}", response_model=dict)
def update_clase(clase: ClaseUpdate, clase_id: int):
    return Clase().actualizar(clase_id, clase)

@institucionRouter.delete("/instituciones/edificios/aulas/clase/{clase_id}", response_model=dict)
def delete_clase(clase_id: int):
    return Clase().eliminar(clase_id)

# -----------------------------
# INSTITUCIONES (genéricas al final)
# -----------------------------
@institucionRouter.post("/instituciones", response_model=dict)
def create_institucion(institucion: InstitucionBase):
    return Institucion().guardar(institucion)

@institucionRouter.get("/instituciones", response_model=List[dict])
def get_instituciones():
    return Institucion().obtener_todos()

@institucionRouter.get("/instituciones/{id}", response_model=dict)
def get_institucion(id: int):
    return Institucion().mostrar_informacion(id)

@institucionRouter.patch("/instituciones/{id}", response_model=dict)
def update_institucion(id: int, institucion: InstitucionUpdate):
    return Institucion().actualizar(institucion, id)


@institucionRouter.delete("/instituciones/{id}", response_model=dict)
def delete_institucion(id: int):
    return Institucion().eliminar(id)

