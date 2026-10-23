from sqlalchemy.orm import Session

from app.models import Cliente, Equipo
from app.repositories.cliente_repository import ClienteRepository, EquipoRepository
from app.schemas.cliente import ClienteCreate, EquipoCreate
from app.services.errors import DomainError


class ClienteService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.clientes = ClienteRepository(db)
        self.equipos = EquipoRepository(db)

    def crear_cliente(self, data: ClienteCreate) -> Cliente:
        cliente = self.clientes.crear(nombre=data.nombre, telefono=data.telefono)
        self.db.commit()
        self.db.refresh(cliente)
        return cliente

    def agregar_equipo(self, cliente_id: int, data: EquipoCreate) -> Equipo:
        if self.clientes.obtener(cliente_id) is None:
            raise DomainError(f"el cliente {cliente_id} no existe")
        equipo = self.equipos.crear(
            cliente_id=cliente_id,
            tipo=data.tipo,
            modelo=data.modelo,
            marca=data.marca,
            numero_serie=data.numero_serie,
            imei=data.imei,
        )
        self.db.commit()
        self.db.refresh(equipo)
        return equipo
