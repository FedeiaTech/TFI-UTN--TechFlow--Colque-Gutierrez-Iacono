from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Pago(Base):
    __tablename__ = "pagos"

    id: Mapped[int] = mapped_column(primary_key=True)
    orden_id: Mapped[int] = mapped_column(nullable=False)
    monto: Mapped[Decimal]
    registrado_por: Mapped[int] = mapped_column(nullable=False)
    pagado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
