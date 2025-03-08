from datetime import datetime
from sqlalchemy import ForeignKey, Table, Column, Integer, String, Text, DateTime
from config.db import meta_data, engine

estudiantes = Table("estudiantes", meta_data,
                    Column('id', Integer, primary_key=True, autoincrement=True),
                    Column('id_usuario', Integer, ForeignKey('users.id'), nullable=False),
                    Column('semestre', Integer),
                    Column('carrera', String(50))

                    )

meta_data.bind = engine
meta_data.create_all(meta_data.bind)