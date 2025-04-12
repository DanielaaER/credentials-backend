from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse

from routes.user import userRouter
from routes.login import loginRouter
from routes.institution import institucionRouter
from routes.qr import qrRouter
from routes.horario import horarioRouter
from config.functions_jwt import validate_token
from config.db import engine, meta_data

meta_data.create_all(bind=engine)
EXCLUDED_PATHS = ["/api/login", "/docs", "/openapi.json", "/api/validate_token${token}"]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI(title="REST API To Virtual Credentials", version="0.1")

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Authorization", "Content-Type"]
)

class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            if request.method == "OPTIONS":
                return await call_next(request)
            if any(request.url.path.startswith(path) for path in EXCLUDED_PATHS):
                return await call_next(request)

            token = request.headers.get("Authorization")
            if not token or not token.startswith("Bearer "):
                raise HTTPException(status_code=401, detail="Token no proporcionado ")

            token = token.replace("Bearer ", "")
            if not validate_token(token, output=True):
                raise HTTPException(status_code=401, detail="Token inválido")

            return await call_next(request)
        except Exception as e:
            return JSONResponse(status_code=500, content={"detail": str(e)})

#app.add_middleware(JWTAuthMiddleware)

app.include_router(loginRouter, tags=["Login"], prefix="/api")
app.include_router(userRouter, tags=["Usuarios"], prefix="/api")
app.include_router(institucionRouter, tags=["Institución"], prefix="/api")
app.include_router(horarioRouter, tags=["Horarios"], prefix="/api")
app.include_router(qrRouter, tags=["QR"], prefix="/api")

if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0")
