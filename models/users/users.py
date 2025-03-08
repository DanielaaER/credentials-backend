from datetime import datetime
from sqlalchemy import ForeignKey, Table, Column, Integer, String, Text, DateTime
from config.db import meta_data, engine

users = Table("users", meta_data,
                Column('id', Integer, primary_key=True, autoincrement=True),
                Column('num_control', String(10)),
                Column('nombre', String(20)),
                Column('apellido_pat', String(20)),
                Column('apellido_mat', String(20)),
                Column('telefono', String(10)),
                Column('direccion', Text),
                Column('email', String(200)),
                Column('password', String(200)),
                Column('foto', String(200)),
                )
meta_data.bind = engine
meta_data.create_all(meta_data.bind)