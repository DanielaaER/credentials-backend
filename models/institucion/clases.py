from sqlalchemy import ForeignKey, Table, Column, Integer, String
from config.db import meta_data, engine

clases = Table('clases', meta_data,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('id_aula', Integer, ForeignKey ('aulas.id')),
    Column('clave_clase', String(10)),
    Column('nombre_clase', String(255), nullable=False)
)
meta_data.bind = engine
meta_data.create_all(meta_data.bind)
