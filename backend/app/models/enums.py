from enum import Enum


class EstadoOrden(str, Enum):
    RECIBIDO = "recibido"
    EN_PROCESO = "en_proceso"
    LISTO = "listo"
    LISTO_NO_RETIRADO = "listo_no_retirado"
    ENTREGADO = "entregado"


class ResultadoOrden(str, Enum):
    REPARADO = "reparado"
    PARCIAL = "parcial"
    SIN_REPARACION = "sin_reparacion"


class EstadoTecnicoTrabajo(str, Enum):
    PENDIENTE_DIAGNOSTICO = "pendiente_diagnostico"
    DIAGNOSTICADO = "diagnosticado"
    ESPERANDO_REPUESTO = "esperando_repuesto"
    EN_REPARACION = "en_reparacion"
    TERMINADO = "terminado"
    IRREPARABLE = "irreparable"
    CANCELADO = "cancelado"


# Estados terminales: una vez alcanzados, el trabajo ya no cambia de estado técnico.
ESTADOS_TERMINALES_TRABAJO = {
    EstadoTecnicoTrabajo.TERMINADO,
    EstadoTecnicoTrabajo.IRREPARABLE,
    EstadoTecnicoTrabajo.CANCELADO,
}


class EstadoCotizacion(str, Enum):
    PENDIENTE = "pendiente"
    APROBADA = "aprobada"
    RECHAZADA = "rechazada"
    REEMPLAZADA = "reemplazada"


class TipoItemCotizacion(str, Enum):
    REPUESTO = "repuesto"
    MANO_OBRA = "mano_obra"
    DESCRIPCION = "descripcion"


class EstadoReserva(str, Enum):
    RESERVADA = "reservada"
    UTILIZADA = "utilizada"
    LIBERADA = "liberada"
