"""Tipos ENUM de SQLAlchemy ligados a los tipos ya existentes en PostgreSQL.

create_type=False: los tipos ENUM ya existen en la base (schema.sql), no los
crea SQLAlchemy.

values_callable: por defecto, sqlalchemy.Enum manda a la base el *nombre* del
miembro de Python (p. ej. "RECIBIDO"), no su valor ("recibido"). Nuestros
Enum(str, Enum) usan nombres en MAYÚSCULAS por convención de Python pero los
tipos de Postgres están en minúscula — sin este callable, cualquier INSERT
rompe con "invalid input value for enum" (bug real, detectado por el test de
humo del vertical ejecutable)."""

from sqlalchemy import Enum

from app.models.enums import (
    EstadoCotizacion,
    EstadoOrden,
    EstadoReserva,
    EstadoTecnicoTrabajo,
    ResultadoOrden,
    TipoItemCotizacion,
)


def _pg_enum(enum_cls: type, name: str) -> Enum:
    return Enum(
        enum_cls,
        name=name,
        create_type=False,
        validate_strings=True,
        values_callable=lambda cls: [member.value for member in cls],
    )


estado_orden_type = _pg_enum(EstadoOrden, "estado_orden")
resultado_orden_type = _pg_enum(ResultadoOrden, "resultado_orden")
estado_tecnico_trabajo_type = _pg_enum(EstadoTecnicoTrabajo, "estado_tecnico_trabajo")
estado_cotizacion_type = _pg_enum(EstadoCotizacion, "estado_cotizacion")
tipo_item_cotizacion_type = _pg_enum(TipoItemCotizacion, "tipo_item_cotizacion")
estado_reserva_type = _pg_enum(EstadoReserva, "estado_reserva")
