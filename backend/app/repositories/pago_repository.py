from decimal import Decimal

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.models import Pago
from app.schemas.orden import OrdenSaldo


class PagoRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def crear(self, orden_id: int, monto: Decimal, registrado_por: int) -> Pago:
        pago = Pago(orden_id=orden_id, monto=monto, registrado_por=registrado_por)
        self.db.add(pago)
        self.db.flush()
        return pago

    def saldo(self, orden_id: int) -> OrdenSaldo:
        """Lee v_orden_saldo (vista SQL, ver database/postgresql/schema.sql). El
        saldo y el estado de pago nunca se calculan a mano en Python: siempre se
        derivan acá, para que no se desincronicen de la regla de negocio real."""
        stmt = text(
            "SELECT orden_id, total_aprobado, total_pagado, saldo, estado_pago "
            "FROM v_orden_saldo WHERE orden_id = :orden_id"
        )
        row = self.db.execute(stmt, {"orden_id": orden_id}).mappings().one()
        return OrdenSaldo(**row)
