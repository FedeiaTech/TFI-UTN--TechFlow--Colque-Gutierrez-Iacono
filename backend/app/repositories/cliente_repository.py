from sqlalchemy.orm import Session

from app.models import Cliente, Equipo


class ClienteRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def crear(self, nombre: str, telefono: str) -> Cliente:
        cliente = Cliente(nombre=nombre, telefono=telefono)
        self.db.add(cliente)
        self.db.flush()
        return cliente

    def obtener(self, cliente_id: int) -> Cliente | None:
        return self.db.get(Cliente, cliente_id)


class EquipoRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def crear(
        self,
        cliente_id: int,
        tipo: str,
        modelo: str,
        marca: str | None,
        numero_serie: str | None,
        imei: str | None,
    ) -> Equipo:
        equipo = Equipo(
            cliente_id=cliente_id,
            tipo=tipo,
            modelo=modelo,
            marca=marca,
            numero_serie=numero_serie,
            imei=imei,
        )
        self.db.add(equipo)
        self.db.flush()
        return equipo

    def obtener(self, equipo_id: int) -> Equipo | None:
        return self.db.get(Equipo, equipo_id)
