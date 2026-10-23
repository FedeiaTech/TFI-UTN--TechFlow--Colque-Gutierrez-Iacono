from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base
from app.models.enums import EstadoCotizacion, EstadoReserva, TipoItemCotizacion
from app.models.pg_types import estado_cotizacion_type, estado_reserva_type, tipo_item_cotizacion_type


class Cotizacion(Base):
    __tablename__ = "cotizaciones"

    id: Mapped[int] = mapped_column(primary_key=True)
    trabajo_id: Mapped[int] = mapped_column(nullable=False)
    numero: Mapped[int]
    estado: Mapped[EstadoCotizacion] = mapped_column(estado_cotizacion_type, default=EstadoCotizacion.PENDIENTE)
    motivo_rechazo: Mapped[str | None]
    creada_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    decidida_en: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class CotizacionItem(Base):
    __tablename__ = "cotizacion_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    cotizacion_id: Mapped[int] = mapped_column(nullable=False)
    tipo: Mapped[TipoItemCotizacion] = mapped_column(tipo_item_cotizacion_type)
    descripcion: Mapped[str]
    repuesto_id: Mapped[int | None]
    cantidad: Mapped[int] = mapped_column(default=1)
    # Snapshot: precio aplicado al momento de cotizar. No se vuelve a leer del
    # catálogo, así un cambio futuro de precio_referencia no altera esta cotización.
    precio_unitario: Mapped[Decimal]


class RepuestoReserva(Base):
    __tablename__ = "repuesto_reservas"

    id: Mapped[int] = mapped_column(primary_key=True)
    cotizacion_item_id: Mapped[int] = mapped_column(nullable=False, unique=True)
    repuesto_id: Mapped[int] = mapped_column(nullable=False)
    cantidad: Mapped[int]
    estado: Mapped[EstadoReserva] = mapped_column(estado_reserva_type, default=EstadoReserva.RESERVADA)
    reservada_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    utilizada_en: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    liberada_en: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
