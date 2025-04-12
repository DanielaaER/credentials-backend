
import pytest
import time
from utils.qr_utils import generar_qr_token, validar_qr_token

def test_qr_valido():
    token = generar_qr_token(usuario_id=1, tipo_usuario='docente')
    resultado = validar_qr_token(token)
    assert resultado['valido'] == True
    assert resultado['usuario_id'] == 1
    assert resultado['tipo'] == 'docente'

def test_qr_expirado():
    token = generar_qr_token(usuario_id=2, tipo_usuario='estudiante')
    time.sleep(31)
    resultado = validar_qr_token(token)
    assert resultado['valido'] == False
    assert resultado['razon'] == 'expirado'
