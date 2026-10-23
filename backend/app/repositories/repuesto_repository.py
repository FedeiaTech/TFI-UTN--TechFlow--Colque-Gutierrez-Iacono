from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Repuesto, RepuestoReserva
from app.models.enums import EstadoReserva


class RepuestoRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def obtener(self, repuesto_id: int) -> Repuesto | None:
        return self.db.get(Repuesto, repuesto_id)

    def obtener_para_actualizar(self, repuesto_id: int) -> Repuesto | None:
        """SELECT ... FOR UPDATE: bloquea la fila del repuesto mientras se decide
        si hay disponibilidad, para que dos reservas concurrentes no pisen el
        mismo stock. Debe llamarse dentro de la transacción que crea o confirma
        la reserva (regla de concurrencia del esquema)."""
        stmt = select(Repuesto).where(Repuesto.id == repuesto_id).with_for_update()
        return self.db.execute(stmt).scalar_one_or_none()

    def disponibilidad(self, repuesto_id: int) -> int:
        """stock_total menos lo reservado (estado 'reservada'). Replica
        v_repuesto_disponibilidad; se calcula en Python porque ya tenemos la fila
        bloqueada con FOR UPDATE y no vale la pena una segunda ida a la vista."""
        repuesto = self.obtener(repuesto_id)
        if repuesto is None:
            raise ValueError(f"repuesto {repuesto_id} no existe")
        stmt = select(func.coalesce(func.sum(RepuestoReserva.cantidad), 0)).where(
            RepuestoReserva.repuesto_id == repuesto_id,
            RepuestoReserva.estado == EstadoReserva.RESERVADA,
        )
        reservado = self.db.execute(stmt).scalar_one()
        return repuesto.stock_total - reservado

    def crear_reserva(self, cotizacion_item_id: int, repuesto_id: int, cantidad: int) -> RepuestoReserva:
        reserva = RepuestoReserva(
            cotizacion_item_id=cotizacion_item_id,
            repuesto_id=repuesto_id,
            cantidad=cantidad,
        )
        self.db.add(reserva)
        self.db.flush()
        return reserva

    def obtener_reserva_por_item(self, cotizacion_item_id: int) -> RepuestoReserva | None:
        stmt = select(RepuestoReserva).where(RepuestoReserva.cotizacion_item_id == cotizacion_item_id)
        return self.db.execute(stmt).scalar_one_or_none()
