from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.pago import PagoCreate, PagoRead
from app.services.pago_service import PagoService

router = APIRouter(prefix="/api/v1/ordenes", tags=["pagos"])


@router.post("/{orden_id}/pagos", response_model=PagoRead, status_code=201)
def registrar_pago(orden_id: int, data: PagoCreate, db: Session = Depends(get_db)) -> PagoRead:
    pago = PagoService(db).registrar(orden_id, data)
    return PagoRead.model_validate(pago)
