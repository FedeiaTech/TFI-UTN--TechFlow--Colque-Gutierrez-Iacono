from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class PagoCreate(BaseModel):
    monto: Decimal = Field(gt=0)
    registrado_por: int


class PagoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    orden_id: int
    monto: Decimal
    registrado_por: int
    pagado_en: datetime
