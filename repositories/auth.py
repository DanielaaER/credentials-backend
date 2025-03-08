
from config.db import engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi import Response, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_201_CREATED
from config.functions_jwt import write_token, validate_token
from models.users.users import users
from schemas.users.user import userAuth

Session = sessionmaker(bind=engine)

class AuthUser:
    def _execute_query(self, query, fetch_one=False):
        try:
            with Session() as session:
                result = session.execute(query)
                return result.fetchone() if fetch_one else result.mappings().all()
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Error en la base de datos: {str(e)}")

    def login(self, login_data: userAuth):
        query = select(users).where(users.c.num_control == login_data.num_control)
        usuario = self._execute_query(query, fetch_one=True)

        if not usuario or not check_password_hash(usuario.password, login_data.password):
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Credenciales incorrectas")

        token = write_token({"sub": usuario.num_control})
        return {
            #"status_code": HTTP_201_CREATED,
            "message": "Login exitoso",
            "data": {
            "access_token": token, "token_type": "bearer", "user": usuario.id} 
        }

    def validate_token(self, token):
        return validate_token(token, output=True)