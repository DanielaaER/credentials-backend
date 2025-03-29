from sqlalchemy import Table, Column, Integer, String, ForeignKey, Time
from config.db import meta_data

horarios_usuarios = Table(
    "horarios_usuarios", meta_data,
    Column("id", Integer, primary_key=True),
    Column("id_usuario", Integer, ForeignKey("users.id")),
    Column("id_clase", Integer, ForeignKey("clases.id"))
)
