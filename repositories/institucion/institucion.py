from sqlalchemy.sql.expression import func, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from config.db import engine
from schemas.institucion.institucion import InstitucionBase, InstitucionUpdate
from models.institucion import institucion
from models.institucion.biblioteca import biblioteca
from models.institucion.edificios import edificios
from repositories.institucion.componente_educativo import ComponenteEducativo

Session = sessionmaker(bind=engine)

class Institucion(ComponenteEducativo):

    def mostrar_informacion(self, id: int):
        try:
            with Session() as session:
                # Obtener la institución por su ID
                result = session.execute(
                    select(institucion).where(institucion.c.id == id)
                ).fetchone()
                # Verificar si se encontró la institución
                if not result:
                    raise HTTPException(status_code=404, detail="Institución no encontrada")
                    
 
                institucion_info = {
                    "id": result.id,
                    "nombre_institucion": result.nombre_institucion,
                    "telefono_institucion": result.telefono_institucion,
                    "ubicacion_institucion": result.ubicacion_institucion,
                    "componentes": []
                }
                
                componentes_info = []
                # Obtener bibliotecas asociadas a la institución
                bibliotecas_result = session.execute(select(biblioteca).where(biblioteca.c.id_institucion == id)).fetchall()
                if bibliotecas_result:
                    bibliotecas_info = [
                        {"id": row.id, "id_institucion": row.id_institucion, "nombre_biblioteca": row.nombre_biblioteca}
                        for row in bibliotecas_result
                    ]
                    componentes_info.append(bibliotecas_info)
                    print("bibliotecas_info")
                    print(bibliotecas_info)


                # Obtener edificios asociados a la institución
                edificios_result = session.execute(select(edificios).where(edificios.c.id_institucion == id)).fetchall()
                if edificios_result:
                    edificios_info = [
                        {"id": row.id, "id_institucion": row.id_institucion, "nombre_edificio": row.nombre_edificio}
                        for row in edificios_result
                    ]
                    print("edificios_info")
                    print(edificios_info)

                    componentes_info = componentes_info + edificios_info
                
                institucion_info["componentes"] = componentes_info
                print("institucion_info")
                print(institucion_info)
                
                return institucion_info
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener institución: {str(e)}")


    def obtener_todos(self):
        try:
            with Session() as session:
                result = session.execute(select(institucion)).fetchall()
                instituciones_info = [
                    {
                        "id": row.id, 
                        "nombre_institucion": row.nombre_institucion, 
                        "telefono_institucion": row.telefono_institucion, 
                        "ubicacion_institucion": row.ubicacion_institucion
                    }
                    for row in result
                ]
                return instituciones_info
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener instituciones: {str(e)}")

    def guardar(self, data: InstitucionBase):
        try:
            
            with Session() as session:
                # Verificar si ya existe una institución con el mismo nombre
                existing_institucion = session.execute(
                    select(institucion).where(institucion.c.nombre_institucion == data.nombre_institucion)
                ).fetchone()
                if existing_institucion:
                    raise HTTPException(status_code=400, detail="Ya existe una institución con ese nombre")
                save_data = data.dict()
                print("save_data")
                print(save_data)
                result = session.execute(
                    institucion.insert().values(save_data)
                )
                id = result.inserted_primary_key[0]
                print("id")
                print(id)
                session.commit()
                return {"message": "Institución creada correctamente", "id": id}
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Error al guardar institución: {str(e)}")

    def actualizar(self, data_update: InstitucionUpdate, id: int):
        try:
            with Session() as session:
                update_data = data_update.dict(exclude_unset=True)
                session.execute(
                    update(institucion)
                    .where(institucion.c.id == id)
                    .values(**update_data)
                )
                session.commit()
                return {"message": "Institución actualizada correctamente"}
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Error al actualizar institución: {str(e)}")

    def eliminar(self, id: int):
        try:
            with Session() as session:
                session.execute(
                    delete(institucion)
                    .where(institucion.c.id == id)
                )
                session.commit()
                return {"message": "Institución eliminada correctamente"}
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Error al eliminar institución: {str(e)}")