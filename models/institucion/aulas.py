from sqlalchemy import ForeignKey, Table, Column, Integer, String
from config.db import meta_data, engine

aulas = Table("aulas", meta_data,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('nombre_aula', String(200)),
    Column('id_edificio', Integer, ForeignKey(
    'edificios.id'))
)

meta_data.bind = engine
meta_data.create_all(meta_data.bind)
