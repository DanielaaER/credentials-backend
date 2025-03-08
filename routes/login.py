
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from repositories.auth import AuthUser
from schemas.users.user import userAuth
loginRouter = APIRouter()


@loginRouter.post("/login/")
def login_user(login_data: userAuth):
    return AuthUser().login(login_data)

@loginRouter.get("/validate_token/")
def validate_token(token: str):
    return AuthUser().validate_token(token)