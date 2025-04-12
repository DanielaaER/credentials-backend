import time
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_generar_y_validar_qr_valido():
    data = {"tipo": "docente", "id": 1}
    response = client.post("/qr/generar", json=data)
    assert response.status_code == 200
    token = response.json()["token"]

    # Validar inmediatamente
    validacion = client.post("/qr/validar", json={"token": token})
    assert validacion.status_code == 200
    assert validacion.json()["valido"] == True

def test_validar_qr_expirado():
    data = {"tipo": "admin", "id": 99}
    response = client.post("/qr/generar", json=data)
    token = response.json()["token"]

    time.sleep(31)  # Esperar que expire

    validacion = client.post("/qr/validar", json={"token": token})
    assert validacion.status_code == 200
    assert validacion.json()["valido"] == False
    assert "expirado" in validacion.json()["error"]

def test_crear_horario():
    horario = {
        "id_clase": 1,
        "dia": "Lunes",
        "hora_inicio": "08:00",
        "duracion_min": 60
    }
    response = client.post("/horarios/", json=horario)
    assert response.status_code == 200
    data = response.json()
    assert data["dia"] == "Lunes"
    assert data["hora_inicio"] == "08:00"
    assert data["duracion_min"] == 60

def test_listar_horarios():
    response = client.get("/horarios/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
