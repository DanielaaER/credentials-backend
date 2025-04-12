# repositories/ingreso_repository.py

from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, insert, desc, and_
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from fastapi import HTTPException

from config.db import engine

from models.users.docente import docentes
from models.users.estudiante import estudiantes
from models.ingreso import ingreso
from models.institucion.clases import clases
from models.users.users import users
from models.horario import horarios
from models.institucion.aulas import aulas

Session = sessionmaker(bind=engine)

class IngresoRepository:

    def registrar_ingreso_qr(self, id_usuario: int, id_aula: int) -> dict:
        try:
            with Session() as session:
                print(f"Registrando ingreso QR para usuario: {id_usuario} en aula: {id_aula}")

                # Verificamos si el usuario es docente
                docente = session.execute(
                    select(docentes).where(docentes.c.id_usuario == id_usuario)
                ).first()

                estudiante = None
                if not docente:
                    # Verificamos si es estudiante
                    estudiante = session.execute(
                        select(estudiantes).where(estudiantes.c.id_usuario == id_usuario)
                    ).first()

                if not docente and not estudiante:
                    raise HTTPException(status_code=404, detail="Usuario no encontrado como estudiante ni docente")

                # Buscar si tiene clase activa en ese aula
                ahora = datetime.now()
                dia_semana = ahora.strftime('%A')  # o el formato que uses en tu DB
                hora_actual = ahora.time()

                clase_info = session.execute(
                    select(horarios.c.id_clase)
                    .where(
                        horarios.c.id_aula     == id_aula,
                        horarios.c.dia         == dia_semana,
                        horarios.c.hora_inicio <= hora_actual,
                        horarios.c.hora_fin    >= hora_actual,
                    )
                ).first()


                if not clase_info:
                    raise HTTPException(status_code=404, detail="No hay clase en este aula")

                id_clase = clase_info.id
                print(f"Clase ID: {id_clase}")
                hoy = datetime.now().date()


                # Ver historial para determinar si es entrada o salida
                query = select(ingreso).where(
                    and_(
                        ingreso.c.id_usuario == id_usuario,
                        ingreso.c.id_aula == id_aula,
                        ingreso.c.fecha_ingreso == hoy
                    )
                ).order_by(desc(ingreso.c.hora_ingreso))

                ultimo = session.execute(query).first()
                tipo_ingreso = True if not ultimo or not ultimo.tipo_ingreso else False
                
                session.execute(
                    insert(ingreso).values(
                        id_usuario=id_usuario,
                        id_aula=id_aula,
                        id_clase=id_clase,
                        fecha_ingreso=hoy,
                        hora_ingreso=datetime.now(),
                        tipo_ingreso=tipo_ingreso
                    )
                )
                    
                session.commit()

                return {
                    "mensaje": "Registro exitoso",
                    "tipo": "Entrada" if tipo_ingreso else "Salida"
                }

        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Error en el ingreso: {str(e)}")

    def obtener_lista_asistencia(self, id_clase: int, fecha: datetime.date) -> list:

            try:
                with Session() as session:
                    

                    # Obtener usuarios que ingresaron ese día a ese aula
                    ingresos = session.execute(
                        select(
                            users.c.num_control,
                            users.c.nombre,
                            users.c.apellido_pat,
                            users.c.apellido_mat,
                            ingreso.c.hora_ingreso,
                            ingreso.c.tipo_ingreso
                        ).join(
                            users, users.c.id == ingreso.c.id_usuario
                        ).where(
                            and_(
                                ingreso.c.id_clase == id_clase,
                                ingreso.c.fecha_ingreso == fecha
                            )
                        )
                    ).fetchall()

                    resultados = []
                    for i in ingresos:
                        resultados.append({
                            "num_control": i.num_control,
                            "nombre": i.nombre,
                            "apellido_pat": i.apellido_pat,
                            "apellido_mat": i.apellido_mat,
                            "hora_ingreso": i.hora_ingreso,
                            "tipo": "Entrada" if i.tipo_ingreso else "Salida"
                        })

                    return resultados

            except SQLAlchemyError as e:
                raise HTTPException(status_code=500, detail=f"Error obteniendo asistencia: {str(e)}")


    def obtener_lista_asistencia_aula(self, id_aula: int, fecha: datetime.date) -> list:

            try:
                with Session() as session:
                    
                    ingresos = session.execute(
                        select(
                            users.c.num_control,
                            users.c.nombre,
                            users.c.apellido_pat,
                            users.c.apellido_mat,
                            ingreso.c.hora_ingreso,
                            ingreso.c.tipo_ingreso
                        ).join(
                            users, users.c.id == ingreso.c.id_usuario
                        ).where(
                            and_(
                                ingreso.c.id_aula == id_aula,
                                ingreso.c.fecha_ingreso == fecha
                            )
                        )
                    ).fetchall()
                    if not ingresos:
                        raise HTTPException(status_code=404, detail="No se encontraron registros de asistencia")

                    print(ingresos)

                    resultados = []
                    for i in ingresos:
                        resultados.append({
                            "num_control": i.num_control,
                            "nombre": i.nombre,
                            "apellido_pat": i.apellido_pat,
                            "apellido_mat": i.apellido_mat,
                            "hora_ingreso": i.hora_ingreso,
                            "tipo": "Entrada" if i.tipo_ingreso else "Salida"
                        })

                    return resultados

            except SQLAlchemyError as e:
                raise HTTPException(status_code=500, detail=f"Error obteniendo asistencia: {str(e)}")


    