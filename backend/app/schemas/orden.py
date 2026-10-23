from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.models.enums import EstadoOrden, EstadoTecnicoTrabajo, ResultadoOrden


class OrdenCreate(BaseModel):
    equipo_id: int
    tecnico_id: int
    falla_reportada: str
    estado_fisico_ingreso: str
    accesorios_entregados: str | None = None


class OrdenRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    equipo_id: int
    tecnico_id: int
    falla_reportada: str
    estado_fisico_ingreso: str
    accesorios_entregados: str | None
    estado: EstadoOrden
    resultado: ResultadoOrden | None
    fecha_listo: datetime | None


class OrdenSaldo(BaseModel):
    orden_id: int
    total_aprobado: Decimal
    total_pagado: Decimal
    saldo: Decimal
    estado_pago: str


class TrabajoCreate(BaseModel):
    descripcion: str


class TrabajoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    orden_id: int
    descripcion: str
    diagnostico: str | None
    estado_tecnico: EstadoTecnicoTrabajo


class TrabajoDiagnosticar(BaseModel):
    diagnostico: str
