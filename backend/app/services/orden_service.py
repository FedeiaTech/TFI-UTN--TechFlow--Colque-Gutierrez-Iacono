from sqlalchemy.orm import Session

from app.models import Orden
from app.models.enums import EstadoOrden
from app.repositories.historial_repository import HistorialRepository
from app.repositories.orden_repository import OrdenRepository
from app.repositories.pago_repository import PagoRepository
from app.schemas.orden import OrdenCreate, OrdenSaldo
from app.services.errors import DomainError


class OrdenService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.ordenes = OrdenRepository(db)
        self.pagos = PagoRepository(db)
        self.historial = HistorialRepository(db)

    def crear(self, data: OrdenCreate, usuario_id: int) -> Orden:
        orden = self.ordenes.crear(
            equipo_id=data.equipo_id,
            tecnico_id=data.tecnico_id,
            falla_reportada=data.falla_reportada,
            estado_fisico_ingreso=data.estado_fisico_ingreso,
            accesorios_entregados=data.accesorios_entregados,
        )
        self.historial.registrar_orden(orden.id, None, EstadoOrden.RECIBIDO, usuario_id)
        self.db.commit()
        self.db.refresh(orden)
        return orden

    def saldo(self, orden_id: int) -> OrdenSaldo:
        return self.pagos.saldo(orden_id)

    def entregar(self, orden_id: int, usuario_id: int) -> Orden:
        """Regla 8 (saldo pendiente): una orden solo puede pasar a 'entregado' si
        v_orden_saldo.saldo == 0. Es la regla que Oscar pidió que esté implementada
        y testeada en backend, no solo documentada."""
        orden = self.ordenes.obtener_para_actualizar(orden_id)
        if orden is None:
            raise DomainError(f"la orden {orden_id} no existe")
        if orden.estado not in (EstadoOrden.LISTO, EstadoOrden.LISTO_NO_RETIRADO):
            raise DomainError(
                f"la orden {orden_id} está en estado '{orden.estado.value}', solo se puede entregar desde "
                "'listo' o 'listo_no_retirado'"
            )

        saldo = self.pagos.saldo(orden_id)
        if saldo.saldo > 0:
            raise DomainError(f"no se puede entregar la orden con saldo pendiente (${saldo.saldo})")

        estado_anterior = orden.estado
        orden.estado = EstadoOrden.ENTREGADO
        self.historial.registrar_orden(orden.id, estado_anterior, EstadoOrden.ENTREGADO, usuario_id)
        self.db.commit()
        self.db.refresh(orden)
        return orden
