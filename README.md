# Virtual Credentials API

## Descripción

Esta API permite la gestión de credenciales virtuales para el control de acceso en instituciones educativas y administrativas. Utiliza FastAPI como framework principal y cuenta con autenticación basada en JWT.

### Funcionalidades Principales

* Gestión de usuarios (creación, actualización, eliminación)
* Gestión de aulas, clases y horarios
* Autenticación con JWT
* Generación y validación de códigos QR
* Control de acceso a rutas mediante middleware

## Tecnologías Utilizadas

* Python 3.10
* FastAPI
* SQLAlchemy
* JWT
* Uvicorn
* PostgreSQL

## Instalación

### Clonar el repositorio

```
git clone https://github.com/DanielaaER/credentials-backend
```

### Crear entorno virtual

```
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### Instalar dependencias

```
pip install -r requirements.txt
```

## Ejecución


### Iniciar el servidor

```
uvicorn app:app --reload
```


## Variables de Entorno

* SECRET\_KEY: Clave para firmar los tokens JWT
* DEV_DB_USER: Usuario de Postgres
* DEV_DB_PASS: Contraseña de DB
* DEV_DB_HOST: Host de la DB
* DEV_DB_NAME: Nombre de la DB
* DEV_DB_PORT: Puerto de la DB


## Desarrollo BackEnd

Daniela Espinosa Rojas