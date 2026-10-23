from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models import Cotizacion
from app.models.enums import EstadoCotizacion, EstadoReserva, EstadoTecnicoTrabajo, TipoItemCotizacion
from app.repositories.cotizacion_repository import CotizacionRepository
from app.repositories.orden_repository import TrabajoRepository
from app.repositories.repuesto_repository import RepuestoRepository
from app.schemas.cotizacion import CotizacionCreate, CotizacionDecision
from app.services.errors import DomainError
from app.services.trabajo_service import TrabajoService


class CotizacionService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.cotizaciones = CotizacionRepository(db)
        self.trabajos = TrabajoRepository(db)
        self.repuestos = RepuestoRepository(db)
        self.trabajo_service = TrabajoService(db)

    def crear(self, trabajo_id: int, data: CotizacionCreate, usuario_id: int) -> Cotizacion:
        trabajo = self.trabajos.obtener(trabajo_id)
        if trabajo is None:
            raise DomainError(f"el trabajo {trabajo_id} no existe")
        if trabajo.estado_tecnico not in (
            EstadoTecnicoTrabajo.DIAGNOSTICADO,
            EstadoTecnicoTrabajo.ESPERANDO_REPUESTO,
        ):
            raise DomainError(
                f"el trabajo {trabajo_id} está en estado '{trabajo.estado_tecnico.value}', "
                "solo se puede cotizar desde 'diagnosticado' o 'esperando_repuesto'"
            )
        if self.cotizaciones.existe_vigente(trabajo_id):
            raise DomainError(f"el trabajo {trabajo_id} ya tiene una cotización vigente (pendiente o aprobada)")
        if not data.items:
            raise DomainError("una cotización necesita al menos un ítem")

        numero = self.cotizaciones.siguiente_numero(trabajo_id)
        cotizacion = self.cotizaciones.crear(trabajo_id, numero)

        for item_in in data.items:
            item = self.cotizaciones.agregar_item(
                cotizacion_id=cotizacion.id,
                tipo=item_in.tipo,
                descripcion=item_in.descripcion,
                repuesto_id=item_in.repuesto_id,
                cantidad=item_in.cantidad,
                precio_unitario=item_in.precio_unitario,
            )
            if item_in.tipo == TipoItemCotizacion.REPUESTO:
                # Regla 2: el repuesto se reserva al presupuestar (acá), no al
                # aprobar. FOR UPDATE evita que dos cotizaciones concurrentes
                # reserven más de lo disponible sobre el mismo repuesto.
                self.repuestos.obtener_para_actualizar(item_in.repuesto_id)
                disponible = self.repuestos.disponibilidad(item_in.repuesto_id)
                if disponible < item_in.cantidad:
                    raise DomainError(
                        f"repuesto {item_in.repuesto_id}: disponibilidad insuficiente "
                        f"({disponible} < {item_in.cantidad})"
                    )
                self.repuestos.crear_reserva(item.id, item_in.repuesto_id, item_in.cantidad)

        self.db.commit()
        self.db.refresh(cotizacion)
        return cotizacion

    def decidir(self, cotizacion_id: int, data: CotizacionDecision, usuario_id: int) -> Cotizacion:
        cotizacion = self.cotizaciones.obtener(cotizacion_id)
        if cotizacion is None:
            raise DomainError(f"la cotización {cotizacion_id} no existe")
        if cotizacion.estado != EstadoCotizacion.PENDIENTE:
            raise DomainError(f"la cotización {cotizacion_id} ya fue decidida ('{cotizacion.estado.value}')")

        ahora = datetime.now(timezone.utc)
        if data.aprobar:
            cotizacion.estado = EstadoCotizacion.APROBADA
            cotizacion.decidida_en = ahora
            self.trabajo_service.marcar_en_reparacion(cotizacion.trabajo_id, usuario_id)
        else:
            cotizacion.estado = EstadoCotizacion.RECHAZADA
            cotizacion.motivo_rechazo = data.motivo_rechazo
            cotizacion.decidida_en = ahora
            self._liberar_reservas(cotizacion_id, ahora)
            self.trabajo_service.marcar_cancelado(cotizacion.trabajo_id, data.motivo_rechazo or "", usuario_id)

        self.db.commit()
        self.db.refresh(cotizacion)
        return cotizacion

    def _liberar_reservas(self, cotizacion_id: int, ahora: datetime) -> None:
        for item in self.cotizaciones.items(cotizacion_id):
            reserva = self.repuestos.obtener_reserva_por_item(item.id)
            if reserva is not None and reserva.estado == EstadoReserva.RESERVADA:
                reserva.estado = EstadoReserva.LIBERADA
                reserva.liberada_en = ahora

    def confirmar_uso(self, trabajo_id: int, usuario_id: int) -> None:
        """Reparación terminada: en una sola transacción, cada reserva pasa a
        'utilizada' y se decrementa repuestos.stock_total (regla: deben ocurrir
        juntas). El FOR UPDATE sobre el repuesto es lo que vuelve seguro este
        decremento frente a confirmaciones concurrentes sobre el mismo repuesto."""
        trabajo = self.trabajos.obtener(trabajo_id)
        if trabajo is None:
            raise DomainError(f"el trabajo {trabajo_id} no existe")
        if trabajo.estado_tecnico != EstadoTecnicoTrabajo.EN_REPARACION:
            raise DomainError(
                f"el trabajo {trabajo_id} está en estado '{trabajo.estado_tecnico.value}', "
                "solo se puede confirmar el uso desde 'en_reparacion'"
            )

        cotizacion = self.cotizaciones.obtener_aprobada_vigente(trabajo_id)
        if cotizacion is None:
            raise DomainError(f"el trabajo {trabajo_id} no tiene una cotización aprobada vigente")

        ahora = datetime.now(timezone.utc)
        for item in self.cotizaciones.items(cotizacion.id):
            if item.tipo != TipoItemCotizacion.REPUESTO:
                continue
            reserva = self.repuestos.obtener_reserva_por_item(item.id)
            if reserva is None or reserva.estado != EstadoReserva.RESERVADA:
                raise DomainError(f"el ítem {item.id} no tiene una reserva en estado 'reservada'")
            repuesto = self.repuestos.obtener_para_actualizar(item.repuesto_id)
            if repuesto is None:
                raise DomainError(f"el repuesto {item.repuesto_id} no existe")
            reserva.estado = EstadoReserva.UTILIZADA
            reserva.utilizada_en = ahora
            repuesto.stock_total -= item.cantidad

        self.trabajo_service.marcar_terminado(trabajo_id, usuario_id)
        self.db.commit()
