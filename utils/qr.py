import jwt
import datetime

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

def generar_qr_token(data: dict, expiracion_segundos: int = 30):
    exp = datetime.datetime.utcnow() + datetime.timedelta(seconds=expiracion_segundos)
    payload = {**data, "exp": exp}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def validar_qr_token(token: str):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {
            "valido": True,
            "data": decoded  # Devolvemos exactamente lo que se codificó
        }
    except jwt.ExpiredSignatureError:
        return {
            "valido": False,
            "error": "Token expirado"
        }
    except jwt.InvalidTokenError:
        return {
            "valido": False,
            "error": "Token inválido"
        }
