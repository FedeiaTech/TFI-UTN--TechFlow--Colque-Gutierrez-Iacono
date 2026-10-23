from pydantic import BaseModel, ConfigDict


class ClienteCreate(BaseModel):
    nombre: str
    telefono: str


class ClienteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    telefono: str


class EquipoCreate(BaseModel):
    tipo: str
    marca: str | None = None
    modelo: str
    numero_serie: str | None = None
    imei: str | None = None


class EquipoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cliente_id: int
    tipo: str
    marca: str | None
    modelo: str
    numero_serie: str | None
    imei: str | None
