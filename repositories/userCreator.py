from repositories.user import DocenteFactory, EstudianteFactory, AdministradorFactory
from fastapi import HTTPException

class UsuarioCreator:
    def __init__(self):
        self._factories = {
            "docente": DocenteFactory(),
            "estudiante": EstudianteFactory(),
            "administrador": AdministradorFactory(),
        }

    def get_factory(self, tipo: str):
        factory = self._factories.get(tipo)
        if not factory:
            raise HTTPException(status_code=400, detail="Tipo de usuario inválido")
        return factory
