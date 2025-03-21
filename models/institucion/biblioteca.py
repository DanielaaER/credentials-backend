from sqlalchemy import ForeignKey, Table, Column, Integer, String
from config.db import meta_data, engine

biblioteca = Table(
    'biblioteca',
    meta_data,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('id_institucion', Integer, ForeignKey('institucion.id')),
    Column('nombre_biblioteca', String(100)),
)
meta_data.bind = engine
meta_data.create_all(meta_data.bind)
