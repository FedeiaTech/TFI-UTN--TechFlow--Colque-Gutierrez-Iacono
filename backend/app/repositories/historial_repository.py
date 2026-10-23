from app.models import HistorialEstadoOrden, HistorialEstadoTrabajo
from app.models.enums import EstadoOrden, EstadoTecnicoTrabajo
from sqlalchemy.orm import Session


class HistorialRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def registrar_orden(
        self,
        orden_id: int,
        estado_anterior: EstadoOrden | None,
        estado_nuevo: EstadoOrden,
        usuario_id: int | None,
        motivo: str | None = None,
    ) -> None:
        self.db.add(
            HistorialEstadoOrden(
                entidad_id=orden_id,
                estado_anterior=estado_anterior,
                estado_nuevo=estado_nuevo,
                usuario_id=usuario_id,
                motivo=motivo,
            )
        )

    def registrar_trabajo(
        self,
        trabajo_id: int,
        estado_anterior: EstadoTecnicoTrabajo | None,
        estado_nuevo: EstadoTecnicoTrabajo,
        usuario_id: int | None,
        motivo: str | None = None,
    ) -> None:
        self.db.add(
            HistorialEstadoTrabajo(
                entidad_id=trabajo_id,
                estado_anterior=estado_anterior,
                estado_nuevo=estado_nuevo,
                usuario_id=usuario_id,
                motivo=motivo,
            )
        )
