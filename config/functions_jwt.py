from jwt import encode, decode, exceptions
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from fastapi.responses import JSONResponse

load_dotenv()

def expire_date(days: int):
    date = datetime.now()
    new_date = date + timedelta(days)
    return new_date

def write_token(data:dict):
    token = encode(payload={**data, "exp": expire_date(1)}, key = os.getenv("SECRET_KEY"), algorithm="HS256")
    return token

def validate_token(token, output=False):
    try:
        if output:
            return decode(token, key = os.getenv("SECRET_KEY"), algorithms=["HS256"])
        decode(token, key = os.getenv("SECRET_KEY"), algorithms=["HS256"])
    except exceptions.DecodeError:
        return JSONResponse(content={"message":"Invalid Token"}, status_code = 401)
    except exceptions.ExpiredSignatureError:
        return JSONResponse(content={"message":"Invalid Token"}, status_code = 401)