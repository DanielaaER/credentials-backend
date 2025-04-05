from sqlalchemy import ForeignKey, Table, Column, Integer, String, Text, DateTime, Boolean
from config.db import meta_data, engine

ingreso = Table(
    'ingreso',
    meta_data,
    Column('id_ingreso', Integer, primary_key=True),
    Column('id_usuario', Integer, ForeignKey('users.id')),
    Column('id_aula', Integer, ForeignKey('aulas.id')),
    Column('id_clase', Integer, ForeignKey('clases.id')), 
    Column('fecha_ingreso', DateTime),
    Column('hora_ingreso', DateTime),
    Column('tipo_ingreso', Boolean),
)


meta_data.bind = engine
meta_data.create_all(meta_data.bind)