from sqlalchemy.sql.expression import func, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from config.db import engine
from schemas.institucion.biblioteca import BibliotecaBase, BibliotecaUpdate
from models.institucion.biblioteca import biblioteca
from repositories.institucion.componente_educativo import ComponenteEducativo


Session = sessionmaker(bind=engine)


class Biblioteca(ComponenteEducativo):
    def mostrar_informacion(self, id: int):
        try:
            with Session() as session:
                query = session.execute(
                    select(biblioteca).where(biblioteca.c.id == id)
                ).fetchone()
                if not query:
                    raise HTTPException(status_code=404, detail="Biblioteca no encontrada")
                print(query)
                bibliotecas = dict(query._mapping)
                return bibliotecas
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener biblioteca: {str(e)}")

    def obtener_todos(self):
        try:
            with Session() as session:
                query = session.execute(select(biblioteca)).fetchall()
                bibliotecas = [dict(row._mapping) for row in query]
                return bibliotecas
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener bibliotecas: {str(e)}")

    def guardar(self, data: BibliotecaBase):
        try:
            with Session() as session:
                result = session.execute(
                    insert(biblioteca).values(data.dict()
                                              )
                )
                session.commit()
                return {"message": "Biblioteca creada correctamente", "id": result.inserted_primary_key[0]}
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Error al guardar biblioteca: {str(e)}")

    def actualizar(self, id: int, data_update: BibliotecaUpdate):
        try:
            with Session() as session:
                update_data = data_update.dict(exclude_unset=True)
                session.execute(
                    update(biblioteca)
                    .where(biblioteca.c.id == id)
                    .values(**update_data)
                )
                session.commit()
                return {"message": "Biblioteca actualizada correctamente"}
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Error al actualizar biblioteca: {str(e)}")

    def eliminar(self, id: int):
        try:
            with Session() as session:
                session.execute(
                    delete(biblioteca)
                    .where(biblioteca.c.id == id)
                )
                session.commit()
                return {"message": "Biblioteca eliminada correctamente"}
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Error al eliminar biblioteca: {str(e)}")

