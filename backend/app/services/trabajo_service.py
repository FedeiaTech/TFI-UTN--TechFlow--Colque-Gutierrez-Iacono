from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models import Trabajo
from app.models.enums import ESTADOS_TERMINALES_TRABAJO, EstadoOrden, EstadoTecnicoTrabajo, ResultadoOrden
from app.repositories.historial_repository import HistorialRepository
from app.repositories.orden_repository import OrdenRepository, TrabajoRepository
from app.services.errors import DomainError


class TrabajoService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.trabajos = TrabajoRepository(db)
        self.ordenes = OrdenRepository(db)
        self.historial = HistorialRepository(db)

    def crear(self, orden_id: int, descripcion: str, usuario_id: int) -> Trabajo:
        orden = self.ordenes.obtener(orden_id)
        if orden is None:
            raise DomainError(f"la orden {orden_id} no existe")
        if orden.estado == EstadoOrden.RECIBIDO:
            # El primer trabajo de la orden la saca de 'recibido'.
            orden.estado = EstadoOrden.EN_PROCESO
            self.historial.registrar_orden(orden.id, EstadoOrden.RECIBIDO, EstadoOrden.EN_PROCESO, usuario_id)

        trabajo = self.trabajos.crear(orden_id, descripcion)
        self.historial.registrar_trabajo(
            trabajo.id, None, EstadoTecnicoTrabajo.PENDIENTE_DIAGNOSTICO, usuario_id
        )
        self.db.commit()
        self.db.refresh(trabajo)
        return trabajo

    def diagnosticar(self, trabajo_id: int, diagnostico: str, usuario_id: int) -> Trabajo:
        trabajo = self.trabajos.obtener(trabajo_id)
        if trabajo is None:
            raise DomainError(f"el trabajo {trabajo_id} no existe")
        if trabajo.estado_tecnico != EstadoTecnicoTrabajo.PENDIENTE_DIAGNOSTICO:
            raise DomainError(
                f"el trabajo {trabajo_id} está en estado '{trabajo.estado_tecnico.value}', "
                "solo se puede diagnosticar desde 'pendiente_diagnostico'"
            )
        trabajo.diagnostico = diagnostico
        estado_anterior = trabajo.estado_tecnico
        trabajo.estado_tecnico = EstadoTecnicoTrabajo.DIAGNOSTICADO
        self.historial.registrar_trabajo(trabajo.id, estado_anterior, trabajo.estado_tecnico, usuario_id)
        self.db.commit()
        self.db.refresh(trabajo)
        return trabajo

    def marcar_irreparable(self, trabajo_id: int, motivo: str, usuario_id: int) -> Trabajo:
        trabajo = self._transicionar_a_terminal(trabajo_id, EstadoTecnicoTrabajo.IRREPARABLE, motivo, usuario_id)
        self.actualizar_orden_si_corresponde(trabajo.orden_id, usuario_id)
        self.db.commit()
        self.db.refresh(trabajo)
        return trabajo

    def marcar_cancelado(self, trabajo_id: int, motivo: str, usuario_id: int) -> Trabajo:
        """El cliente rechaza la cotización vigente del trabajo. Se usa desde
        CotizacionService.decidir(), no como endpoint propio: no tiene sentido
        cancelar un trabajo sin una cotización rechazada de por medio."""
        trabajo = self._transicionar_a_terminal(trabajo_id, EstadoTecnicoTrabajo.CANCELADO, motivo, usuario_id)
        self.actualizar_orden_si_corresponde(trabajo.orden_id, usuario_id)
        return trabajo

    def marcar_en_reparacion(self, trabajo_id: int, usuario_id: int) -> Trabajo:
        """El cliente aprueba la cotización vigente del trabajo. Se usa desde
        CotizacionService.decidir(), no como endpoint propio."""
        trabajo = self.trabajos.obtener(trabajo_id)
        if trabajo is None:
            raise DomainError(f"el trabajo {trabajo_id} no existe")
        if trabajo.estado_tecnico not in (
            EstadoTecnicoTrabajo.DIAGNOSTICADO,
            EstadoTecnicoTrabajo.ESPERANDO_REPUESTO,
        ):
            raise DomainError(
                f"el trabajo {trabajo_id} está en estado '{trabajo.estado_tecnico.value}', "
                "solo pasa a 'en_reparacion' desde 'diagnosticado' o 'esperando_repuesto'"
            )
        estado_anterior = trabajo.estado_tecnico
        trabajo.estado_tecnico = EstadoTecnicoTrabajo.EN_REPARACION
        self.historial.registrar_trabajo(trabajo.id, estado_anterior, trabajo.estado_tecnico, usuario_id)
        return trabajo

    def marcar_terminado(self, trabajo_id: int, usuario_id: int) -> Trabajo:
        """Reparación física completada. Se usa desde CotizacionService.confirmar_uso()
        una vez aplicada la transacción atómica de reserva + stock, no como endpoint
        propio: terminar un trabajo sin confirmar el uso de sus repuestos dejaría
        reservas colgadas."""
        trabajo = self._transicionar_a_terminal(trabajo_id, EstadoTecnicoTrabajo.TERMINADO, None, usuario_id)
        self.actualizar_orden_si_corresponde(trabajo.orden_id, usuario_id)
        return trabajo

    def _transicionar_a_terminal(
        self, trabajo_id: int, nuevo_estado: EstadoTecnicoTrabajo, motivo: str | None, usuario_id: int
    ) -> Trabajo:
        trabajo = self.trabajos.obtener(trabajo_id)
        if trabajo is None:
            raise DomainError(f"el trabajo {trabajo_id} no existe")
        if trabajo.estado_tecnico in ESTADOS_TERMINALES_TRABAJO:
            raise DomainError(f"el trabajo {trabajo_id} ya está en un estado terminal")
        estado_anterior = trabajo.estado_tecnico
        trabajo.estado_tecnico = nuevo_estado
        self.historial.registrar_trabajo(trabajo.id, estado_anterior, nuevo_estado, usuario_id, motivo)
        return trabajo

    def actualizar_orden_si_corresponde(self, orden_id: int, usuario_id: int) -> None:
        """Regla: la orden pasa a 'listo' solo cuando TODOS sus trabajos están en
        estado terminal (terminado, irreparable o cancelado), sin importar que
        alguno siga esperando repuesto en otro trabajo (eso se resuelve dejando
        ese trabajo abierto, no bloqueando la orden entera)."""
        if not self.trabajos.todos_en_estado_terminal(orden_id):
            return

        orden = self.ordenes.obtener_para_actualizar(orden_id)
        if orden is None or orden.estado != EstadoOrden.EN_PROCESO:
            return

        trabajos = self.trabajos.listar_por_orden(orden_id)
        hay_terminados = any(t.estado_tecnico == EstadoTecnicoTrabajo.TERMINADO for t in trabajos)
        hay_no_terminados = any(
            t.estado_tecnico in (EstadoTecnicoTrabajo.IRREPARABLE, EstadoTecnicoTrabajo.CANCELADO)
            for t in trabajos
        )
        if hay_terminados and hay_no_terminados:
            resultado = ResultadoOrden.PARCIAL
        elif hay_terminados:
            resultado = ResultadoOrden.REPARADO
        else:
            resultado = ResultadoOrden.SIN_REPARACION

        estado_anterior = orden.estado
        orden.estado = EstadoOrden.LISTO
        orden.resultado = resultado
        orden.fecha_listo = datetime.now(timezone.utc)
        self.historial.registrar_orden(orden.id, estado_anterior, EstadoOrden.LISTO, usuario_id)
