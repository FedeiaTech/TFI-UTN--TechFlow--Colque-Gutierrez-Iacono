from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Cotizacion, CotizacionItem
from app.models.enums import EstadoCotizacion


class CotizacionRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def siguiente_numero(self, trabajo_id: int) -> int:
        stmt = select(func.coalesce(func.max(Cotizacion.numero), 0)).where(Cotizacion.trabajo_id == trabajo_id)
        return self.db.execute(stmt).scalar_one() + 1

    def existe_vigente(self, trabajo_id: int) -> bool:
        stmt = select(Cotizacion.id).where(
            Cotizacion.trabajo_id == trabajo_id,
            Cotizacion.estado.in_([EstadoCotizacion.PENDIENTE, EstadoCotizacion.APROBADA]),
        )
        return self.db.execute(stmt).first() is not None

    def crear(self, trabajo_id: int, numero: int) -> Cotizacion:
        cotizacion = Cotizacion(trabajo_id=trabajo_id, numero=numero)
        self.db.add(cotizacion)
        self.db.flush()
        return cotizacion

    def obtener(self, cotizacion_id: int) -> Cotizacion | None:
        return self.db.get(Cotizacion, cotizacion_id)

    def obtener_aprobada_vigente(self, trabajo_id: int) -> Cotizacion | None:
        stmt = select(Cotizacion).where(
            Cotizacion.trabajo_id == trabajo_id,
            Cotizacion.estado == EstadoCotizacion.APROBADA,
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def agregar_item(
        self,
        cotizacion_id: int,
        tipo: str,
        descripcion: str,
        repuesto_id: int | None,
        cantidad: int,
        precio_unitario,
    ) -> CotizacionItem:
        item = CotizacionItem(
            cotizacion_id=cotizacion_id,
            tipo=tipo,
            descripcion=descripcion,
            repuesto_id=repuesto_id,
            cantidad=cantidad,
            precio_unitario=precio_unitario,
        )
        self.db.add(item)
        self.db.flush()
        return item

    def items(self, cotizacion_id: int) -> list[CotizacionItem]:
        stmt = select(CotizacionItem).where(CotizacionItem.cotizacion_id == cotizacion_id)
        return list(self.db.execute(stmt).scalars())
