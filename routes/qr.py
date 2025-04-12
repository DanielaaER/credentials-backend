from fastapi import APIRouter
from schemas.qr_schema import QRGenerarRequest, QRRespuesta, QRValidarRequest
from utils.qr import generar_qr_token, validar_qr_token
from repositories.ingreso import IngresoRepository
import datetime

qrRouter = APIRouter(prefix="/qr", tags=["QR"])
repo = IngresoRepository()

@qrRouter.post("/generar", response_model=QRRespuesta)
def generar_qr(req: QRGenerarRequest):
    token = generar_qr_token({"tipo": req.tipo, "id": req.id})
    return {"token": token}

@qrRouter.post("/validar/{id_institucion}")
def validar_qr(id_institucion: int, req: QRValidarRequest):
    print(f"Validando QR para aula: {id_institucion}")
    datos = validar_qr_token(req.token)
    print(f"Datos decodificados: {datos}")
    datos = datos.get("data")
    if not datos:
        return {"error": "Token inválido o expirado"}
    print(f"Datos decodificados: {datos}")
    id_usuario = datos.get("id")
    print(f"Validando QR para usuario: {id_usuario} en aula: {id_institucion}")
    return repo.registrar_ingreso_qr(id_usuario=id_usuario, id_aula=id_institucion)

@qrRouter.get("/asistencia/clase/{id_clase}")
def obtener_asistencia(id_clase: int, fecha: datetime.date):
    return repo.obtener_lista_asistencia(id_clase=id_clase, fecha=fecha)

@qrRouter.get("/asistencia/aula/{id_aula}")
def obtener_asistencia_aula(id_aula: int, fecha: datetime.date):
    return repo.obtener_lista_asistencia_aula(id_aula=id_aula, fecha=fecha)
