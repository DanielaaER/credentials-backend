from fastapi import APIRouter, HTTPException
from schemas.horario import HorarioCreate, HorarioUser, HorarioUpdate
from repositories.horario_repository import HorarioRepository

horarioRouter = APIRouter( prefix="/horarios")
repo = HorarioRepository()

@horarioRouter.get("/", summary="Obtener todos los horarios")
def obtener_todos():
    return repo.obtener_todos()

@horarioRouter.get("/{id}", summary="Obtener un horario por ID")
def obtener_por_id(id: int):
    return repo.mostrar_informacion(id)

@horarioRouter.post("/", summary="Crear un nuevo horario")
def crear_horario(horario: HorarioCreate):
    return repo.guardar(horario)

@horarioRouter.patch("/{id}", summary="Actualizar un horario")
def actualizar_horario(id: int, horario: HorarioUpdate):
    return repo.actualizar(id, horario)

@horarioRouter.delete("/{id}", summary="Eliminar un horario")
def eliminar_horario(id: int):
    return repo.eliminar(id)

@horarioRouter.get("/usuario/{id_usuario}", summary="Obtener horarios por usuario")
def obtener_horarios_por_usuario(id_usuario: int):
    return repo.obtener_por_usuario(id_usuario)

@horarioRouter.get("/clase/{id_clase}", summary="Obtener horarios por clase")
def obtener_horarios_por_clase(id_clase: int):
    return repo.obtener_por_clase(id_clase)

@horarioRouter.get("/aula/{id_aula}", summary="Obtener horarios por aula")
def obtener_horarios_por_aula(id_aula: int):
    return repo.obtener_por_aula(id_aula)

@horarioRouter.post("/asignar-usuario")
def asignar_usuario(asignacion: HorarioUser):
    return repo.asignar_usuario_a_clase(asignacion.id_usuario, asignacion.id_clase)

@horarioRouter.get("/clase/usuario/{id_usuario}", summary="Obtener las clases de un usuario")
def obtener_clases_por_usuario(id_usuario: int):
    return repo.obtener_clases_por_usuario(id_usuario)

@horarioRouter.get("/usuario/clase/{id_clase}", summary="Obtener los usuarios de una clase")
def obtener_usuarios_por_clase(id_clase: int):
    return repo.obtener_usuarios_por_clase(id_clase)

@horarioRouter.get("/docente/clase/{id_clase}", summary="Obtener el docente de una clase")
def obtener_docente_por_clase(id_clase: int):
    return repo.obtener_docente_por_clase(id_clase)