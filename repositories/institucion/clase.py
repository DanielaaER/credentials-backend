from sqlalchemy.sql.expression import func, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from config.db import engine
from schemas.institucion.clase import ClaseBase, ClaseUpdate
from models.institucion.clases import clases
from repositories.institucion.componente_educativo import ComponenteEducativo

Session = sessionmaker(bind=engine)

class Clase(ComponenteEducativo):

    def mostrar_informacion(self, id: int):
        try:
            with Session() as session:
                result = session.execute(
                    clases.select().where(clases.c.id == id)
                ).fetchone()
                if not result:
                    raise HTTPException(status_code=404, detail="Clase no encontrada")
                return dict(result._mapping)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener clase: {str(e)}")

    def obtener_todos(self, id: int):
        try:
            with Session() as session:
                result = session.execute(select(clases).where(clases.c.id_aula == id)).fetchall()
                if not result:
                    raise HTTPException(status_code=404, detail="Clases no encontradas")
                clases_result = session.execute(
                    select(clases)
                ).fetchall()
                clases_info = [dict(row._mapping) for row in clases_result]
                if not clases_info:
                    raise HTTPException(status_code=404, detail="Clases no encontradas")
                return clases_info

        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener clases: {str(e)}")

    def obtener_todas_clases(self):
        try:
            with Session() as session:
                result = session.execute(select(clases)).fetchall()
                if not result:
                    raise HTTPException(status_code=404, detail="Clases no encontradas")

                clases_info = [dict(row._mapping) for row in result]
                if not clases_info:
                    raise HTTPException(status_code=404, detail="Clases no encontradas")
                return clases_info

        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener clases: {str(e)}")

    def guardar(self, data: ClaseBase):
        try:
            with Session() as session:
                result = session.execute(
                    select(clases.c.clave_clase).order_by(desc(clases.c.clave_clase)).limit(1)
                ).fetchone()
                print("result")
                print(result)

                if not result or not result[0]:
                    ultima_clave = "CL000"
                else:
                    ultima_clave = result[0]
                ultimo_numero = int(ultima_clave[2:])

                nuevo_numero = ultimo_numero + 1

                nueva_clave = f"CL{nuevo_numero:03d}"

                data.clave_clase = nueva_clave

                result = session.execute(
                    clases.insert().values(data.dict()
                                           )
                )
                session.commit()
                id = result.inserted_primary_key[0]
                return {"message": "Clase creada correctamente", "id": id}
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Error al guardar clase: {str(e)}")

    def actualizar(self, id: int, data_update: ClaseUpdate):
        try:
            with Session() as session:
                update_data = data_update.dict(exclude_unset=True)
                session.execute(
                    clases.update()
                    .where(clases.c.id == id)
                    .values(**update_data)
                )
                session.commit()
                return {"message": "Clase actualizada correctamente"}
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Error al actualizar clase: {str(e)}")

    def eliminar(self, id: int):
        try:
            with Session() as session:
                session.execute(
                    delete(clases)
                    .where(clases.c.id == id)
                )
                session.commit()
                return {"message": "Clase eliminada correctamente"}
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Error al eliminar clase: {str(e)}")

