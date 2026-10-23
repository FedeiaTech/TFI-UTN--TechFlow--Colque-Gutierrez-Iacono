from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base
from app.models.enums import EstadoOrden, EstadoTecnicoTrabajo
from app.models.pg_types import estado_orden_type, estado_tecnico_trabajo_type


class HistorialEstadoOrden(Base):
    __tablename__ = "historial_estados_orden"

    id: Mapped[int] = mapped_column(primary_key=True)
    entidad_id: Mapped[int] = mapped_column(nullable=False)
    estado_anterior: Mapped[EstadoOrden | None] = mapped_column(estado_orden_type)
    estado_nuevo: Mapped[EstadoOrden] = mapped_column(estado_orden_type)
    usuario_id: Mapped[int | None]
    motivo: Mapped[str | None]
    creado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class HistorialEstadoTrabajo(Base):
    __tablename__ = "historial_estados_trabajo"

    id: Mapped[int] = mapped_column(primary_key=True)
    entidad_id: Mapped[int] = mapped_column(nullable=False)
    estado_anterior: Mapped[EstadoTecnicoTrabajo | None] = mapped_column(estado_tecnico_trabajo_type)
    estado_nuevo: Mapped[EstadoTecnicoTrabajo] = mapped_column(estado_tecnico_trabajo_type)
    usuario_id: Mapped[int | None]
    motivo: Mapped[str | None]
    creado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
