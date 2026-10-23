from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, model_validator

from app.models.enums import EstadoCotizacion, TipoItemCotizacion


class CotizacionItemCreate(BaseModel):
    tipo: TipoItemCotizacion
    descripcion: str
    repuesto_id: int | None = None
    cantidad: int = 1
    precio_unitario: Decimal

    @model_validator(mode="after")
    def repuesto_id_coherente_con_tipo(self) -> "CotizacionItemCreate":
        es_repuesto = self.tipo == TipoItemCotizacion.REPUESTO
        if es_repuesto and self.repuesto_id is None:
            raise ValueError("un ítem de tipo 'repuesto' requiere repuesto_id")
        if not es_repuesto and self.repuesto_id is not None:
            raise ValueError("solo un ítem de tipo 'repuesto' puede tener repuesto_id")
        return self


class CotizacionCreate(BaseModel):
    items: list[CotizacionItemCreate]


class CotizacionItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tipo: TipoItemCotizacion
    descripcion: str
    repuesto_id: int | None
    cantidad: int
    precio_unitario: Decimal


class CotizacionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    trabajo_id: int
    numero: int
    estado: EstadoCotizacion
    motivo_rechazo: str | None
    creada_en: datetime
    decidida_en: datetime | None


class CotizacionDecision(BaseModel):
    aprobar: bool
    motivo_rechazo: str | None = None

    @model_validator(mode="after")
    def motivo_requerido_si_rechaza(self) -> "CotizacionDecision":
        if not self.aprobar and not self.motivo_rechazo:
            raise ValueError("motivo_rechazo es obligatorio al rechazar una cotización")
        return self
