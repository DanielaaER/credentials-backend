from pydantic import BaseModel

class QRGenerarRequest(BaseModel):
    tipo: str  # docente, estudiante, admin
    id: int

class QRRespuesta(BaseModel):
    token: str

class QRValidarRequest(BaseModel):
    token: str
