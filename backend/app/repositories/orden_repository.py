from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Orden, Trabajo
from app.models.enums import EstadoTecnicoTrabajo


class OrdenRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def crear(
        self,
        equipo_id: int,
        tecnico_id: int,
        falla_reportada: str,
        estado_fisico_ingreso: str,
        accesorios_entregados: str | None,
    ) -> Orden:
        orden = Orden(
            equipo_id=equipo_id,
            tecnico_id=tecnico_id,
            falla_reportada=falla_reportada,
            estado_fisico_ingreso=estado_fisico_ingreso,
            accesorios_entregados=accesorios_entregados,
        )
        self.db.add(orden)
        self.db.flush()
        return orden

    def obtener(self, orden_id: int) -> Orden | None:
        return self.db.get(Orden, orden_id)

    def obtener_para_actualizar(self, orden_id: int) -> Orden | None:
        """Bloquea la fila para evitar transiciones concurrentes sobre la misma orden."""
        stmt = select(Orden).where(Orden.id == orden_id).with_for_update()
        return self.db.execute(stmt).scalar_one_or_none()


class TrabajoRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def crear(self, orden_id: int, descripcion: str) -> Trabajo:
        trabajo = Trabajo(orden_id=orden_id, descripcion=descripcion)
        self.db.add(trabajo)
        self.db.flush()
        return trabajo

    def obtener(self, trabajo_id: int) -> Trabajo | None:
        return self.db.get(Trabajo, trabajo_id)

    def listar_por_orden(self, orden_id: int) -> list[Trabajo]:
        stmt = select(Trabajo).where(Trabajo.orden_id == orden_id)
        return list(self.db.execute(stmt).scalars())

    def todos_en_estado_terminal(self, orden_id: int) -> bool:
        trabajos = self.listar_por_orden(orden_id)
        if not trabajos:
            return False
        terminales = {
            EstadoTecnicoTrabajo.TERMINADO,
            EstadoTecnicoTrabajo.IRREPARABLE,
            EstadoTecnicoTrabajo.CANCELADO,
        }
        return all(t.estado_tecnico in terminales for t in trabajos)
