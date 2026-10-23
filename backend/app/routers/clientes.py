from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.cliente import ClienteCreate, ClienteRead, EquipoCreate, EquipoRead
from app.services.cliente_service import ClienteService

router = APIRouter(prefix="/api/v1/clientes", tags=["clientes"])


@router.post("", response_model=ClienteRead, status_code=201)
def crear_cliente(data: ClienteCreate, db: Session = Depends(get_db)) -> ClienteRead:
    cliente = ClienteService(db).crear_cliente(data)
    return ClienteRead.model_validate(cliente)


@router.post("/{cliente_id}/equipos", response_model=EquipoRead, status_code=201)
def agregar_equipo(cliente_id: int, data: EquipoCreate, db: Session = Depends(get_db)) -> EquipoRead:
    equipo = ClienteService(db).agregar_equipo(cliente_id, data)
    return EquipoRead.model_validate(equipo)
