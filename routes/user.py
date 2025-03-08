
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from schemas.users.user import  UsuarioBase, UsuarioUpdate
from repositories.userCreator import UsuarioCreator


userRouter = APIRouter()
userCreator = UsuarioCreator()
@userRouter.post("/usuarios/{tipo}")
def crear_usuario(tipo: str, user_data: UsuarioBase):
    user_data = user_data.dict()
    factory = userCreator.get_factory(tipo)
    return factory.crear_usuario(user_data)

@userRouter.get("/usuarios/{tipo}", response_model=List[dict])
def get_usuarios(tipo: str):
    return userCreator.get_factory(tipo).get_usuarios()

@userRouter.get("/usuario/{user_id}", response_model=dict)
def get_usuario(user_id: int):
    for factory in userCreator._factories.values():
        usuario = factory.get_usuario_por_id(user_id)
        if usuario:
            return usuario
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@userRouter.patch("/usuarios/update/{tipo}/{user_id}")
def update_usuario(tipo: str, user_id: int, user_data: UsuarioUpdate):
    user_data = user_data.dict()
    factory = userCreator.get_factory(tipo)
    return factory.update_usuario(user_id, user_data)

@userRouter.delete("/usuarios/delete/{tipo}/{user_id}")
def delete_usuario(tipo: str, user_id: int):
    return userCreator.get_factory(tipo).delete_usuario(user_id)