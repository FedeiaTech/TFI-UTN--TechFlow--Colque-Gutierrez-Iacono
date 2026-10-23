from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class CategoriaRepuesto(Base):
    __tablename__ = "categorias_repuesto"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(unique=True)


class Repuesto(Base):
    __tablename__ = "repuestos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]
    categoria_id: Mapped[int] = mapped_column(nullable=False)
    stock_total: Mapped[int] = mapped_column(default=0)
    # Solo referencia del catálogo. El precio cotizado se guarda como snapshot
    # en cotizacion_items.precio_unitario (no se vuelve a leer de acá).
    precio_referencia: Mapped[Decimal | None]
