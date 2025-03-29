from sqlalchemy import Table, Column, Integer, String, ForeignKey, Time
from config.db import meta_data

horarios = Table(
    "horarios", meta_data,
    Column("id", Integer, primary_key=True),
    Column("id_clase", Integer, ForeignKey("clases.id")),
    Column("dia", String(10)),
    Column("hora_inicio", Time),
    Column("hora_fin", Time)
)

