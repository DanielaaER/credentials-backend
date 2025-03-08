from sqlalchemy import ForeignKey, Table, Column, Integer, String, Text, DateTime
from config.db import meta_data, engine


institucion = Table('institucion', meta_data,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('nombre_institucion', String(255), nullable=False),
    Column('telefono_institucion', String(255), nullable=False),
    Column('ubicacion_institucion', String(255), nullable=False)
)


meta_data.bind = engine
meta_data.create_all(meta_data.bind)