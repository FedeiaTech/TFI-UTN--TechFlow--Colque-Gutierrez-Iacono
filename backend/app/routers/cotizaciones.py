from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.cotizacion import CotizacionCreate, CotizacionDecision, CotizacionRead
from app.services.cotizacion_service import CotizacionService

router = APIRouter(prefix="/api/v1", tags=["cotizaciones"])


@router.post("/trabajos/{trabajo_id}/cotizaciones", response_model=CotizacionRead, status_code=201)
def crear_cotizacion(
    trabajo_id: int, data: CotizacionCreate, usuario_id: int, db: Session = Depends(get_db)
) -> CotizacionRead:
    cotizacion = CotizacionService(db).crear(trabajo_id, data, usuario_id)
    return CotizacionRead.model_validate(cotizacion)


@router.patch("/cotizaciones/{cotizacion_id}/decidir", response_model=CotizacionRead)
def decidir_cotizacion(
    cotizacion_id: int, data: CotizacionDecision, usuario_id: int, db: Session = Depends(get_db)
) -> CotizacionRead:
    cotizacion = CotizacionService(db).decidir(cotizacion_id, data, usuario_id)
    return CotizacionRead.model_validate(cotizacion)


@router.post("/trabajos/{trabajo_id}/confirmar-uso", status_code=204)
def confirmar_uso(trabajo_id: int, usuario_id: int, db: Session = Depends(get_db)) -> None:
    CotizacionService(db).confirmar_uso(trabajo_id, usuario_id)
