from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, insert, update, delete, and_, or_
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from config.db import engine
from schemas.horario import HorarioCreate, HorarioResponse, HorarioClase, HorarioUpdate
from abc import ABC, abstractmethod

from models.users.docente import docentes
from models.users.estudiante import estudiantes
from models.horario import horarios
from models.institucion.clases import clases
from models.horario_usuario import horarios_usuarios
from models.institucion.aulas import aulas
from models.users.users import users
from schemas.institucion.clase import ClaseResponse
from schemas.users.estudiante import EstudianteClase
from sqlalchemy.sql.expression import func
Session = sessionmaker(bind=engine)

class Horario(ABC):
    @abstractmethod
    def mostrar_informacion(self, id: int) -> HorarioResponse: pass

    @abstractmethod
    def obtener_todos(self) -> list[HorarioResponse]: pass

    @abstractmethod
    def guardar(self, data: HorarioCreate) -> dict: pass

    @abstractmethod
    def actualizar(self, id: int, data: dict) -> dict: pass

    @abstractmethod
    def eliminar(self, id: int) -> dict: pass


class HorarioRepository(Horario):
    
    def mostrar_informacion(self, id: int) -> HorarioResponse:
        """Obtiene la información del horario por ID"""
        try:
            with Session() as session:
                result = session.execute(
                    select(horarios).where(horarios.c.id == id)
                ).mappings().first()

                if not result:
                    raise HTTPException(status_code=404, detail="Horario no encontrado")
                
                # Devolver el resultado como un objeto Pydantic HorarioResponse
                return HorarioResponse(**result)
        
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener horario: {str(e)}")

    def obtener_todos(self) -> list[HorarioResponse]:
        """Obtiene todos los horarios disponibles con información de la clase y aula"""
        try:
            with Session() as session:
                result = session.execute(
                    select(
                        horarios.c.id,
                        horarios.c.dia,
                        horarios.c.hora_inicio,
                        horarios.c.hora_fin,
                        clases.c.nombre_clase,
                        clases.c.clave_clase
                    ).select_from(
                        horarios.join(clases, horarios.c.id_clase == clases.c.id)
                    )
                ).mappings().all()

                # Obtener el nombre del aula para cada resultado
                for row in result:
                    aula = session.execute(
                        select(clases.c.nombre_clase).where(clases.c.id_aula == row['id_aula'])
                    ).scalar()
                    row['nombre_aula'] = aula

                # Convertir el resultado en una lista de objetos Pydantic
                return [HorarioResponse(**row) for row in result]
        
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener horarios: {str(e)}")


    def guardar(self, data: HorarioCreate) -> dict:
        """Guarda un nuevo horario para una clase, verificando conflictos por aula"""
        try:
            with Session() as session:
                # Normalizar día
                dia_normalizado = data.dia.strip().capitalize()

                # Buscar aula
                clase = session.execute(
                    select(clases.c.id_aula).where(clases.c.id == data.id_clase)
                ).first()

                if not clase:
                    raise HTTPException(status_code=404, detail="Clase no encontrada")

                id_aula = clase.id_aula

                # Verificar conflicto en la misma aula, mismo día, solapamiento
                conflicto = session.execute(
                    select(horarios).select_from(
                        horarios.join(clases, horarios.c.id_clase == clases.c.id)
                    ).where(
                        and_(
                            clases.c.id_aula == id_aula,
                            horarios.c.dia == dia_normalizado,
                            horarios.c.hora_inicio < data.hora_fin,
                            horarios.c.hora_fin > data.hora_inicio
                        )
                    )
                ).first()

                if conflicto:
                    raise HTTPException(
                        status_code=409,
                        detail="Conflicto de horario: el aula ya está ocupada en ese horario y día."
                    )

                # Insertar
                result = session.execute(
                    insert(horarios).values(
                        id_clase=data.id_clase,
                        dia=dia_normalizado,
                        hora_inicio=data.hora_inicio,
                        hora_fin=data.hora_fin
                    )
                )
                session.commit()

                return {
                    "message": "Horario creado correctamente",
                    "id": result.inserted_primary_key[0]
                }

        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Error al guardar horario: {str(e)}")



    def actualizar(self, id: int, data: HorarioUpdate) -> dict:
        """Actualiza un horario existente verificando conflictos con otros horarios de usuarios y aulas"""
        try:
            with Session() as session:
                # Obtener el horario actual para verificar el aula
                horario_actual = session.execute(
                    select(horarios.c.id_clase, horarios.c.dia, horarios.c.hora_inicio, horarios.c.hora_fin)
                    .where(horarios.c.id == id)
                ).first()

                if not horario_actual:
                    raise HTTPException(status_code=404, detail="Horario no encontrado")

                # Normalizar el día
                dia_normalizado = data.dia.strip().capitalize()

                # Obtener el ID del aula a partir de la clase
                clase = session.execute(
                    select(clases.c.id_aula).where(clases.c.id == horario_actual.id_clase)
                ).first()

                if not clase:
                    raise HTTPException(status_code=404, detail="Clase no encontrada")

                id_aula = clase.id_aula

                # Verificar conflictos de solapamiento con otros horarios en el mismo aula
                conflicto_aula = session.execute(
                    select(horarios).select_from(
                        horarios.join(clases, horarios.c.id_clase == clases.c.id)
                    ).where(
                        and_(
                            clases.c.id_aula == id_aula,
                            horarios.c.dia == dia_normalizado,
                            horarios.c.id != id,  # Excluir el propio horario
                            horarios.c.hora_inicio < data.hora_fin,
                            horarios.c.hora_fin > data.hora_inicio
                        )
                    )
                ).first()

                if conflicto_aula:
                    raise HTTPException(
                        status_code=409,
                        detail=f"Conflicto de horario: el aula ya está ocupada en ese horario y día por la clase '{conflicto_aula['nombre_clase']}'."
                    )

                # Obtener usuarios asignados a la clase actual
                usuarios_asignados = session.execute(
                    select(horarios_usuarios.c.id_usuario)
                    .where(horarios_usuarios.c.id_clase == horario_actual.id_clase)
                ).mappings().all()

                usuario_ids = [usuario['id_usuario'] for usuario in usuarios_asignados]

                # Verificar conflictos de horarios con otros usuarios (docentes y estudiantes)
                for id_usuario in usuario_ids:
                    horarios_usuario = session.execute(
                        select(
                            horarios.c.dia,
                            horarios.c.hora_inicio,
                            horarios.c.hora_fin,
                            clases.c.nombre_clase
                        ).select_from(
                            horarios.join(horarios_usuarios, horarios.c.id_clase == horarios_usuarios.c.id_clase)
                                    .join(clases, horarios.c.id_clase == clases.c.id)
                        ).where(
                            and_(
                                horarios_usuarios.c.id_usuario == id_usuario,
                                horarios.c.id != id  # Excluir el propio horario
                            )
                        )
                    ).mappings().all()

                    # Verificar solapamiento
                    for horario_asignado in horarios_usuario:
                        if (
                            horario_asignado['dia'] == dia_normalizado and
                            data.hora_inicio < horario_asignado['hora_fin'] and
                            data.hora_fin > horario_asignado['hora_inicio']
                        ):
                            raise HTTPException(
                                status_code=409,
                                detail=f"Conflicto de horario: el usuario con ID {id_usuario} ya tiene asignada la clase '{horario_asignado['nombre_clase']}' en ese horario."
                            )

                # Actualizar el horario si no hay conflictos
                session.execute(
                    update(horarios)
                    .where(horarios.c.id == id)
                    .values(**data.dict(exclude_unset=True))
                )
                session.commit()
                return {"message": "Horario actualizado correctamente"}

        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Error al actualizar horario: {str(e)}")

    def eliminar(self, id: int) -> dict:
        """Elimina un horario por ID"""
        try:
            with Session() as session:
                session.execute(
                    delete(horarios).where(horarios.c.id == id)
                )
                session.commit()
                return {"message": "Horario eliminado correctamente"}
        
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Error al eliminar horario: {str(e)}")
    
    def obtener_por_usuario(self, id_usuario: int) -> list[HorarioClase]:
        """Obtiene horarios por ID de usuario con información de la clase y aula"""
        try:
            with Session() as session:
                # Obtener los horarios junto con la información de la clase y aula
                result = session.execute(
                    select(
                        horarios.c.id,
                        horarios.c.dia,
                        horarios.c.hora_inicio,
                        horarios.c.hora_fin,
                        clases.c.nombre_clase,
                        clases.c.clave_clase,
                        aulas.c.nombre_aula
                    ).select_from(
                        horarios.join(horarios_usuarios, horarios.c.id_clase == horarios_usuarios.c.id_clase)
                                .join(clases, horarios.c.id_clase == clases.c.id)
                                .join(aulas, clases.c.id_aula == aulas.c.id)
                    ).where(horarios_usuarios.c.id_usuario == id_usuario)
                ).mappings().all()
                
                print(result)
                # Convertir el resultado en una lista de objetos Pydantic
                return [HorarioClase(**row) for row in result]
            
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener horarios por usuario: {str(e)}")


    def obtener_por_clase(self, id_clase: int) -> list[HorarioClase]:
        """Obtiene horarios por ID de clase con información de la clase y aula"""
        try:
            with Session() as session:
                result = session.execute(
                    select(
                        horarios.c.id,
                        horarios.c.dia,
                        horarios.c.hora_inicio,
                        horarios.c.hora_fin,
                        clases.c.nombre_clase,
                        clases.c.clave_clase,
                        aulas.c.nombre_aula
                    ).select_from(
                        horarios.join(clases, horarios.c.id_clase == clases.c.id)
                                .join(aulas, clases.c.id_aula == aulas.c.id)
                    ).where(horarios.c.id_clase == id_clase)
                ).mappings().all()
                print(result)

                return [HorarioClase(**row) for row in result]

        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener horarios por clase: {str(e)}")


    def obtener_por_aula(self, id_aula: int) -> list[HorarioClase]:
        """Obtiene horarios por ID de aula con información de la clase y aula"""
        try:
            with Session() as session:
                result = session.execute(
                    select(
                        horarios.c.id,
                        horarios.c.dia,
                        horarios.c.hora_inicio,
                        horarios.c.hora_fin,
                        clases.c.nombre_clase,
                        clases.c.clave_clase,
                        aulas.c.nombre_aula
                    ).select_from(
                        horarios.join(clases, horarios.c.id_clase == clases.c.id)
                                .join(aulas, clases.c.id_aula == aulas.c.id)
                    ).where(clases.c.id_aula == id_aula)
                ).mappings().all()
                 
                return [HorarioClase(**row) for row in result]
            
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener horarios por aula: {str(e)}")

    def asignar_usuario_a_clase(self, id_usuario: int, id_clase: int) -> dict:
        try:
            with Session() as session:
                horario_nuevo = session.execute(
                    select(horarios.c.dia, horarios.c.hora_inicio, horarios.c.hora_fin)
                    .where(horarios.c.id_clase == id_clase)
                ).mappings().all()

                if not horario_nuevo:
                    raise HTTPException(status_code=404, detail="Clase no encontrada o no tiene horario asignado.")

                # Obtener los horarios ya asignados al usuario en otras clases
                horarios_usuario = session.execute(
                    select(
                        horarios.c.dia,
                        horarios.c.hora_inicio,
                        horarios.c.hora_fin,
                        clases.c.nombre_clase
                    ).select_from(
                        horarios.join(horarios_usuarios, horarios.c.id_clase == horarios_usuarios.c.id_clase)
                                .join(clases, horarios.c.id_clase == clases.c.id)
                    ).where(horarios_usuarios.c.id_usuario == id_usuario)
                ).mappings().all()

                # Verificar solapamiento de horarios
                for horario_asignado in horarios_usuario:
                    for nuevo in horario_nuevo:
                        if (
                            horario_asignado['dia'] == nuevo['dia'] and 
                            nuevo['hora_inicio'] < horario_asignado['hora_fin'] and 
                            nuevo['hora_fin'] > horario_asignado['hora_inicio']
                        ):
                            raise HTTPException(
                                status_code=409,
                                detail=f"Conflicto de horario: la clase '{horario_asignado['nombre_clase']}' ya ocupa ese horario."
                            )

                # Verificar si el usuario es docente
                es_docente = session.execute(
                    select(docentes).where(docentes.c.id_usuario == id_usuario)
                ).first()

                if es_docente:
                    # Verificar si el docente ya tiene una clase asignada
                    clase_asignada = session.execute(
                        select(horarios_usuarios).where(
                            horarios_usuarios.c.id_clase == id_clase,
                            horarios_usuarios.c.id_usuario.in_(
                                select(docentes.c.id_usuario)
                            )
                        )
                    ).first()

                    if clase_asignada:
                        raise HTTPException(status_code=400, detail="El docente ya tiene una clase asignada.")

                    # Asignar clase
                    print("asignando")
                    session.execute(
                        insert(horarios_usuarios).values(
                            id_usuario=id_usuario,
                            id_clase=id_clase
                        )
                    )
                    # Verificar si el docente tiene un horario asignado{{}}
                    session.commit()
                    return {"message": "Docente asignado correctamente a la clase"}

                # Verificar si el usuario es estudiante
                es_estudiante = session.execute(
                    select(estudiantes).where(estudiantes.c.id_usuario == id_usuario)
                ).first()

                if es_estudiante:
                    # Verificar cuántos estudiantes ya están asignados a la clase
                    total_estudiantes = session.execute(
                        select(func.count()).select_from(horarios_usuarios).where(
                            horarios_usuarios.c.id_clase == id_clase
                        )
                    ).scalar()

                    if total_estudiantes >= 30:
                        raise HTTPException(status_code=400, detail="La clase ya tiene 30 estudiantes asignados.")

                    # Asignar estudiante
                    session.execute(
                        insert(horarios_usuarios).values(
                            id_usuario=id_usuario,
                            id_clase=id_clase
                        )
                    )
                    session.commit()
                    return {"message": "Estudiante asignado correctamente a la clase"}

                raise HTTPException(status_code=400, detail="El usuario no es ni docente ni estudiante.")

        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Error al asignar usuario: {str(e)}")

    def obtener_clases_por_usuario(self, id_usuario: int) -> list[ClaseResponse]:
        """Obtiene las clases de un usuario por ID de usuario"""
        try:
            with Session() as session:
                result = session.execute(
                    select(
                        clases.c.id,
                        clases.c.id_aula,
                        clases.c.nombre_clase,
                        clases.c.clave_clase
                    ).select_from(
                        clases.join(horarios_usuarios, clases.c.id == horarios_usuarios.c.id_clase)
                    ).where(horarios_usuarios.c.id_usuario == id_usuario)
                ).mappings().all()
                print(result)

                return [ClaseResponse(**row) for row in result]

        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener clases por usuario: {str(e)}")

    def obtener_usuarios_por_clase(self, id_clase: int) -> list[EstudianteClase]:
        """Obtiene los usuarios de una clase por ID de clase"""
        try:
            with Session() as session:
                result = session.execute(
                    select(
                        users.c.num_control,
                        users.c.nombre,
                        users.c.apellido_pat,
                        users.c.apellido_mat
                    ).select_from(
                        users.join(
                            horarios_usuarios, users.c.id == horarios_usuarios.c.id_usuario
                        ).join(estudiantes, estudiantes.c.id_usuario == users.c.id)
                      ).where(horarios_usuarios.c.id_clase == id_clase)
                ).mappings().all()
                print(result)

                return [EstudianteClase(**row) for row in result]

        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener usuarios por clase: {str(e)}")

    def obtener_docente_por_clase(self, id_clase: int) -> EstudianteClase:
        """Obtiene los docentes de una clase por ID de clase"""
        try:
            with Session() as session:
                result = session.execute(
                    select(
                        users.c.num_control,
                        users.c.nombre,
                        users.c.apellido_pat,
                        users.c.apellido_mat
                    ).select_from(
                        users.join(
                            horarios_usuarios, users.c.id == horarios_usuarios.c.id_usuario
                        ).join(docentes, docentes.c.id_usuario == users.c.id)
                    ).where(horarios_usuarios.c.id_clase == id_clase)
                ).mappings().first()
                if not result:
                    raise HTTPException(status_code=404, detail="Docente no encontrado")
                print(result)
                return EstudianteClase(**result)

        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener docentes por clase: {str(e)}")