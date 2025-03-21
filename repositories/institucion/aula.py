from sqlalchemy.sql.expression import func, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from config.db import engine
from repositories.institucion.componente_educativo import ComponenteEducativo
from schemas.institucion.aula import AulaBase, AulaUpdate
from models.institucion.aulas import aulas
from models.institucion.clases import clases

Session = sessionmaker(bind=engine)

class Aula(ComponenteEducativo):
    def mostrar_informacion(self, id: int):
        try:
            with Session() as session:
                # Obtener el aula por su ID
                print("aula")
                result = session.execute(
                    select(aulas).where(aulas.c.id == id)
                ).fetchone()
                # Verificar si se encontró el aula
                print("result")
                print(result)

                if not result:
                    raise HTTPException(status_code=404, detail="Aula no encontrado")

                aula_info = {
                    "id": result.id,
                    "nombre_aula": result.nombre_aula,
                    "id_edificio": result.id_edificio,
                    "clases": []
                }

                # Obtener las aulas asociadas al edificio
                clases_result = session.execute(
                    select(clases).where(clases.c.id_aula == id)
                ).fetchall()

                clases_info = []
                if clases_result:
                    clases_info = [
                        {"id": row.id, "nombre_clase": row.nombre_clase}
                        for row in clases_result
                    ]

                aula_info["clases"] = clases_info
                return aula_info

        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener aula: {str(e)}")

    def obtener_todos(self):
        print("Aulas")
        try:
            with Session() as session:
                print("aulas")
                result = session.execute(select(aulas)).fetchall()
                print(result)

                if not result:
                    raise HTTPException(status_code=404, detail="Aulas no encontradas")
                aulas_info = [
                    {
                        "id": row.id,
                        "nombre_aula": row.nombre_aula,
                        "id_edificio": row.id_edificio
                    }
                    for row in result
                ]
                return aulas_info
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener aulas: {str(e)}")

    def guardar(self, data: AulaBase):
        try:
            with Session() as session:

                save_data = data.dict()
                result = session.execute(
                    aulas.insert().values(save_data
                                          )
                )
                session.commit()
                return {"message": "Aula creada correctamente", "id": result.inserted_primary_key[0]}
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Error al guardar aula: {str(e)}")

    def actualizar(self, id: int, data_update: AulaUpdate):
        try:
            with Session() as session:
                update_data = data_update.dict(exclude_unset=True)
                session.execute(
                    update(aulas)
                    .where(aulas.c.id == id)
                    .values(**update_data)
                )
                session.commit()
                return {"message": "Aula actualizada correctamente"}
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Error al actualizar aula: {str(e)}")

    def eliminar(self, id: int):
        try:
            with Session() as session:
                session.execute(
                    delete(aulas)
                    .where(aulas.c.id == id)
                )
                session.commit()
                return {"message": "Aula eliminada correctamente"}
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Error al eliminar aula: {str(e)}")

