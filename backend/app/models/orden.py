from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base
from app.models.enums import EstadoOrden, EstadoTecnicoTrabajo, ResultadoOrden
from app.models.pg_types import estado_orden_type, estado_tecnico_trabajo_type, resultado_orden_type


class Orden(Base):
    __tablename__ = "ordenes"

    id: Mapped[int] = mapped_column(primary_key=True)
    equipo_id: Mapped[int] = mapped_column(nullable=False)
    tecnico_id: Mapped[int] = mapped_column(nullable=False)
    falla_reportada: Mapped[str]
    estado_fisico_ingreso: Mapped[str]
    accesorios_entregados: Mapped[str | None]
    estado: Mapped[EstadoOrden] = mapped_column(estado_orden_type, default=EstadoOrden.RECIBIDO)
    resultado: Mapped[ResultadoOrden | None] = mapped_column(resultado_orden_type)
    fecha_listo: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    fecha_primer_aviso_no_retirado: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    fecha_segundo_aviso_no_retirado: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    creado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    actualizado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Trabajo(Base):
    __tablename__ = "trabajos"

    id: Mapped[int] = mapped_column(primary_key=True)
    orden_id: Mapped[int] = mapped_column(nullable=False)
    descripcion: Mapped[str]
    diagnostico: Mapped[str | None]
    estado_tecnico: Mapped[EstadoTecnicoTrabajo] = mapped_column(
        estado_tecnico_trabajo_type, default=EstadoTecnicoTrabajo.PENDIENTE_DIAGNOSTICO
    )
    creado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    actualizado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
