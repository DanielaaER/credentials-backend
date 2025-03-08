from sqlalchemy.sql.expression import func, desc
from abc import ABC, abstractmethod
from typing import List
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from config.db import engine

Session = sessionmaker(bind=engine)
class ComponenteEducativo(ABC):
    @abstractmethod
    def mostrar_informacion(self, id: int):
        pass

    @abstractmethod
    def obtener_todos(self) -> List:
        pass

    @abstractmethod
    def guardar(self, data):
        pass

    @abstractmethod
    def actualizar(self, id: int, data_update):
        pass

    @abstractmethod
    def eliminar(self, id: int):
        pass
