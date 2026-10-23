from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.orden import OrdenCreate, OrdenRead, OrdenSaldo, TrabajoCreate, TrabajoDiagnosticar, TrabajoRead
from app.services.orden_service import OrdenService
from app.services.trabajo_service import TrabajoService

router = APIRouter(prefix="/api/v1/ordenes", tags=["ordenes"])


@router.post("", response_model=OrdenRead, status_code=201)
def crear_orden(data: OrdenCreate, db: Session = Depends(get_db)) -> OrdenRead:
    orden = OrdenService(db).crear(data, usuario_id=data.tecnico_id)
    return OrdenRead.model_validate(orden)


@router.get("/{orden_id}/saldo", response_model=OrdenSaldo)
def obtener_saldo(orden_id: int, db: Session = Depends(get_db)) -> OrdenSaldo:
    return OrdenService(db).saldo(orden_id)


@router.patch("/{orden_id}/entregar", response_model=OrdenRead)
def entregar_orden(orden_id: int, usuario_id: int, db: Session = Depends(get_db)) -> OrdenRead:
    orden = OrdenService(db).entregar(orden_id, usuario_id)
    return OrdenRead.model_validate(orden)


@router.post("/{orden_id}/trabajos", response_model=TrabajoRead, status_code=201)
def crear_trabajo(
    orden_id: int, data: TrabajoCreate, usuario_id: int, db: Session = Depends(get_db)
) -> TrabajoRead:
    trabajo = TrabajoService(db).crear(orden_id, data.descripcion, usuario_id)
    return TrabajoRead.model_validate(trabajo)


@router.patch("/trabajos/{trabajo_id}/diagnosticar", response_model=TrabajoRead)
def diagnosticar_trabajo(
    trabajo_id: int, data: TrabajoDiagnosticar, usuario_id: int, db: Session = Depends(get_db)
) -> TrabajoRead:
    trabajo = TrabajoService(db).diagnosticar(trabajo_id, data.diagnostico, usuario_id)
    return TrabajoRead.model_validate(trabajo)


@router.patch("/trabajos/{trabajo_id}/irreparable", response_model=TrabajoRead)
def marcar_irreparable(
    trabajo_id: int, motivo: str, usuario_id: int, db: Session = Depends(get_db)
) -> TrabajoRead:
    trabajo = TrabajoService(db).marcar_irreparable(trabajo_id, motivo, usuario_id)
    return TrabajoRead.model_validate(trabajo)
