from abc import ABC, abstractmethod
from config.db import engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from models.users.users import users
from models.users.docente import docentes
from models.users.estudiante import estudiantes
from models.users.administrador import administradores
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi import Response, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_201_CREATED
from schemas.users.estudiante import EstudianteBase, EstudianteUpdate
from schemas.users.docente import DocenteBase
from schemas.users.administrador import AdministradorBase, AdministradorUpdate
Session = sessionmaker(bind=engine)

from datetime import datetime

class UsuarioFactory(ABC):
    @abstractmethod
    def tabla(self):
        pass

    @abstractmethod
    def campos_personales(self, user_data):
        pass

    @abstractmethod
    def get_schema(self, user_data):
        pass

    @abstractmethod
    def get_update_schema(self, user_data):
        pass

    def _generar_num_control(self, session, prefix):
        """
        Genera el número de control automáticamente basado en el tipo de usuario.
        Ejemplo: DC25000001, ES26000001, AM25000001.
        """
        # Obtener los últimos dos dígitos del año actual
        year_suffix = str(datetime.now().year)[-2:]
        # Prefijo con el año actual
        prefix_year = f"{prefix}{year_suffix}"

        # Consultar el último número de control generado con el mismo prefijo y año
        query = session.execute(
            select(users.c.num_control)
            .where(users.c.num_control.like(f"{prefix_year}%"))
            .order_by(users.c.num_control.desc())
        ).fetchone()

        if query and query[0]:
            # Obtener la parte numérica del último número de control
            ultimo_num = int(query[0][-6:]) + 1
        else:
            # Si no hay registros previos, comenzar desde 1
            ultimo_num = 1

        # Formato: PREFIJO + AÑO + NÚMERO DE 6 DÍGITOS
        return f"{prefix_year}{ultimo_num:06d}"


    
    def _execute_query(self, query, fetch_one=False):
        try:
            with Session() as session:
                result = session.execute(query)
                return result.fetchone() if fetch_one else result.mappings().all()
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Error en la base de datos: {str(e)}")

    def _usuario_existe(self, session, id):
        return session.execute(select(users).where(users.c.id == id)).fetchone()


    def _num_control_existe(self, session, num_control):
        return session.execute(select(users).where(users.c.num_control == num_control)).fetchone()

    def crear_usuario(self, user_data):
        try:
            user_data = self.get_schema(user_data)  
            
            with Session() as session:
                if isinstance(self, DocenteFactory):
                    prefix = "DC"
                elif isinstance(self, EstudianteFactory):
                    prefix = "ES"
                elif isinstance(self, AdministradorFactory):
                    prefix = "AM"
                else:
                    raise HTTPException(status_code=400, detail="Tipo de usuario no reconocido")
                user_data.num_control = self._generar_num_control(session, prefix)
                if self._num_control_existe(session, user_data.num_control):
                    return Response(status_code=HTTP_401_UNAUTHORIZED, content="Usuario ya existe")
                

                hashed_password = generate_password_hash(user_data.password)
                nuevo_usuario = user_data.dict(exclude={"periodo", "semestre", "carrera", "puesto_admin", "id_usuario"})
                nuevo_usuario['num_control'] = user_data.num_control
                nuevo_usuario['password'] = hashed_password
                print(nuevo_usuario)
                result = session.execute(users.insert().values(nuevo_usuario))
                usuario_id = result.inserted_primary_key[0]
                tabla_relacionada = self.tabla()
                dato_extra = self.campos_personales(user_data)
                session.execute(tabla_relacionada.insert().values(id_usuario=usuario_id, **dato_extra))
                session.commit()

                return {"status": HTTP_201_CREATED, "message": "Usuario creado correctamente", "id_usuario": usuario_id}
        except SQLAlchemyError as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear usuario: {str(e)}")

    def get_usuarios(self):
        try:
            with Session() as session:
                tabla_relacionada = self.tabla()
                query = session.execute(
                    select(users, tabla_relacionada)
                    .join(tabla_relacionada, tabla_relacionada.c.id_usuario == users.c.id)
                ).mappings().all()

                return [dict(row) for row in query]
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener usuarios: {str(e)}")

    def get_usuario_por_id(self, user_id):
        try:
            with Session() as session:
                query = session.execute(
                    select(
                        users, docentes.c.periodo, estudiantes.c.semestre, 
                        estudiantes.c.carrera, administradores.c.puesto_admin
                    )
                    .outerjoin(docentes, docentes.c.id_usuario == users.c.id)
                    .outerjoin(estudiantes, estudiantes.c.id_usuario == users.c.id)
                    .outerjoin(administradores, administradores.c.id_usuario == users.c.id)
                    .where(users.c.id == user_id)
                ).mappings().first()

                if not query:
                    raise HTTPException(status_code=404, detail="Usuario no encontrado")

                usuario = {k: v for k, v in query.items() if v is not None}

                return usuario

        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener usuario: {str(e)}")

    def update_usuario(self, user_id, user_data):
        try:
            print(user_data)
            
            user_data = self.get_update_schema(user_data)  
            with Session() as session:
                if not self._usuario_existe(session, user_id):
                    raise HTTPException(status_code=404, detail="Usuario no encontrado")

                user_update_data = user_data.dict(exclude_unset=True)

                columnas_users = set(users.c.keys())
                user_data_filtrado = {k: v for k, v in user_update_data.items() if k in columnas_users and v is not None}

                if "password" in user_data_filtrado:
                    user_data_filtrado["password"] = generate_password_hash(user_data_filtrado["password"])
                if user_data_filtrado:
                    session.execute(
                        users.update().where(users.c.id == user_id).values(**user_data_filtrado)
                    )

                tabla_relacionada = self.tabla()

                usuario_en_tabla = session.execute(
                    select(tabla_relacionada).where(tabla_relacionada.c.id_usuario == user_id)
                ).fetchone()

                if not usuario_en_tabla:
                    raise HTTPException(status_code=400, detail=f"El usuario no pertenece a {tabla_relacionada.name}")

                dato_extra = self.campos_personales(user_data)
                columnas_validas = set(tabla_relacionada.c.keys())
                dato_extra_filtrado = {k: v for k, v in dato_extra.items() if k in columnas_validas and v is not None}

                if dato_extra_filtrado:
                    session.execute(
                        tabla_relacionada.update()
                        .where(tabla_relacionada.c.id_usuario == user_id)
                        .values(**dato_extra_filtrado)
                    )

                session.commit()
                return {"message": "Usuario actualizado correctamente"}

        except SQLAlchemyError as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=f"Error al actualizar usuario: {str(e)}")


    def delete_usuario(self, user_id):
        try:
            with Session() as session:
                if not self._usuario_existe(session, user_id):
                    raise HTTPException(status_code=404, detail="Usuario no encontrado")

                tabla_relacionada = self.tabla()

                session.execute(
                    tabla_relacionada.delete().where(tabla_relacionada.c.id_usuario == user_id)
                )

                session.execute(
                    users.delete().where(users.c.id == user_id)
                )

                session.commit()

                return {"message": "Usuario eliminado correctamente"}
        except SQLAlchemyError as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=f"Error al eliminar usuario: {str(e)}")

class DocenteFactory(UsuarioFactory):
    def tabla(self):
        return docentes

    def campos_personales(self, user_data):
        return {"periodo": user_data.periodo}

    def get_schema(self, user_data):
        return DocenteBase(**user_data)
    
    def get_update_schema(self, user_data):
        return DocenteUpdate(**user_data)

class EstudianteFactory(UsuarioFactory):
    def tabla(self):
        return estudiantes

    def campos_personales(self, user_data):
        return {"semestre": user_data.semestre, "carrera": user_data.carrera}

    def get_schema(self, user_data):
        return EstudianteBase(**user_data)

    def get_update_schema(self, user_data):
        return EstudianteUpdate(**user_data)


class AdministradorFactory(UsuarioFactory):
    def tabla(self):
        return administradores

    def campos_personales(self, user_data):
        return {"puesto_admin": user_data.puesto_admin}

    def get_schema(self, user_data):
        return AdministradorBase(**user_data)
    
    def get_update_schema(self, user_data):
        return AdministradorUpdate(**user_data)
