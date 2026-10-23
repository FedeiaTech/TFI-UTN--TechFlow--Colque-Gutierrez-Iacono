from sqlalchemy.orm import Session

from app.models import Pago
from app.repositories.orden_repository import OrdenRepository
from app.repositories.pago_repository import PagoRepository
from app.schemas.pago import PagoCreate
from app.services.errors import DomainError


class PagoService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.pagos = PagoRepository(db)
        self.ordenes = OrdenRepository(db)

    def registrar(self, orden_id: int, data: PagoCreate) -> Pago:
        if self.ordenes.obtener(orden_id) is None:
            raise DomainError(f"la orden {orden_id} no existe")
        # data.monto > 0 ya lo valida Pydantic (Field(gt=0)) y lo refuerza el
        # CHECK (monto > 0) de la tabla: doble protección, a propósito.
        pago = self.pagos.crear(orden_id=orden_id, monto=data.monto, registrado_por=data.registrado_por)
        self.db.commit()
        self.db.refresh(pago)
        return pago
