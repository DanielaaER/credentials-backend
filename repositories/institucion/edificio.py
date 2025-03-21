
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from config.db import engine
from repositories.institucion.componente_educativo import ComponenteEducativo
from schemas.institucion.edificio import EdificioBase, EdificioUpdate
from models.institucion.edificios import edificios
from models.institucion.aulas import aulas

Session = sessionmaker(bind=engine)


class Edificio(ComponenteEducativo):
    def mostrar_informacion(self, id: int):
        try:
            with Session() as session:
                result = session.execute(
                    select(edificios).where(edificios.c.id == id)
                ).fetchone()
                if not result:
                    raise HTTPException(status_code=404, detail="Edificio no encontrado")

                edificio_info = {
                    "id": result.id,
                    "nombre_edificio": result.nombre_edificio,
                    "id_institucion": result.id_institucion,
                    "aulas": []
                }

                # Obtener las aulas asociadas al edificio
                aulas_result = session.execute(
                    select(aulas).where(aulas.c.id_edificio == id)
                ).fetchall()
                aulas_info = [
                    {"id": row.id, "id_edificio": row.id_edificio, "nombre_aula": row.nombre_aula}
                    for row in aulas_result
                ]

                edificio_info["aulas"] = aulas_info
                return edificio_info
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener edificio: {str(e)}")

    def obtener_todos(self):
        try:
            with Session() as session:
                result = session.execute(select(edificios)).fetchall()
                edificios_info = [
                    {
                        "id": row.id,
                        "nombre_edificio": row.nombre_edificio,
                        "ubicacion_edificio": row.ubicacion_edificio,
                        "id_institucion": row.id_institucion
                    }
                    for row in result
                ]
                return edificios_info
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener edificios: {str(e)}")

    def guardar(self, data: EdificioBase):
        try:
            with Session() as session:
                save_data = data.dict()
                result = session.execute(
                    edificios.insert().values(save_data)
                )
                id = result.inserted_primary_key[0]
                session.commit()
                return {"message": "Edificio creado correctamente", "id": id}
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Error al guardar edificio: {str(e)}")

    def actualizar(self, id: int, data_update: EdificioUpdate):
        try:
            with Session() as session:
                update_data = data_update.dict(exclude_unset=True)
                session.execute(
                    update(edificios)
                    .where(edificios.c.id == id)
                    .values(**update_data)
                )
                session.commit()
                return {"message": "Edificio actualizado correctamente"}
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Error al actualizar edificio: {str(e)}")

    def eliminar(self, id: int):
        try:
            with Session() as session:
                session.execute(
                    delete(edificios)
                    .where(edificios.c.id == id)
                )
                session.commit()
                return {"message": "Edificio eliminado correctamente"}
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Error al eliminar edificio: {str(e)}")
