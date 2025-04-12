import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_crear_docente():
    response = client.post("/docentes/", json={"nombre": "Juan Pérez", "email": "juan@escuela.com"})
    assert response.status_code == 200
    assert response.json()["nombre"] == "Juan Pérez"

def test_crear_estudiante():
    response = client.post("/estudiantes/", json={"nombre": "Ana Torres", "email": "ana@escuela.com"})
    assert response.status_code == 200
    assert response.json()["nombre"] == "Ana Torres"

def test_crear_institucion():
    data = {
        "nombre_institucion": "Preparatoria Nacional",
        "telefono_institucion": "555-1234",
        "ubicacion_institucion": "CDMX"
    }
    response = client.post("/instituciones/", json=data)
    assert response.status_code == 200
    assert response.json()["nombre_institucion"] == "Preparatoria Nacional"

def test_crear_edificio():
    # Crear institución primero
    inst = client.post("/instituciones/", json={
        "nombre_institucion": "Instituto Técnico",
        "telefono_institucion": "1234567890",
        "ubicacion_institucion": "México"
    }).json()

    response = client.post("/edificios/", json={
        "id_institucion": inst["id"],
        "nombre_edificio": "Edificio A",
        "ubicacion_edificio": "Norte"
    })
    assert response.status_code == 200
    assert response.json()["nombre_edificio"] == "Edificio A"

def test_crear_aula():
    # Crear institución y edificio
    inst = client.post("/instituciones/", json={
        "nombre_institucion": "Centro Educativo",
        "telefono_institucion": "0000000000",
        "ubicacion_institucion": "Sur"
    }).json()
    edif = client.post("/edificios/", json={
        "id_institucion": inst["id"],
        "nombre_edificio": "Edificio B",
        "ubicacion_edificio": "Este"
    }).json()

    response = client.post("/aulas/", json={
        "id_edificio": edif["id"],
        "nombre_aula": "Aula 101"
    })
    assert response.status_code == 200
    assert response.json()["nombre_aula"] == "Aula 101"

def test_crear_clase():
    # Crear docente y aula primero
    docente = client.post("/docentes/", json={"nombre": "Carlos Gómez", "email": "carlos@es.com"}).json()
    inst = client.post("/instituciones/", json={
        "nombre_institucion": "Universidad Libre",
        "telefono_institucion": "1111",
        "ubicacion_institucion": "Centro"
    }).json()
    edif = client.post("/edificios/", json={
        "id_institucion": inst["id"],
        "nombre_edificio": "Edif C",
        "ubicacion_edificio": "Oeste"
    }).json()
    aula = client.post("/aulas/", json={"id_edificio": edif["id"], "nombre_aula": "Aula 1"}).json()

    response = client.post("/clases/", json={
        "id_aula": aula["id"],
        "clave_clase": "CLA120",
        "nombre_clase": "Matemáticas",
        "docente": docente["id"]
    })
    assert response.status_code == 200
    assert response.json()["clave_clase"] == "CLA120"
