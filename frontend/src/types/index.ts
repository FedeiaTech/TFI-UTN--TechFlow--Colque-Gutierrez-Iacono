export type CategoriaEquipo = 'CELULAR' | 'NOTEBOOK' | 'PC_ESCRITORIO' | 'CONSOLA' | 'AUDIO' | 'OTRO';

export type EstadoOrden = 
  | 'RECIBIDO' 
  | 'EN_DIAGNOSTICO' 
  | 'EN_REPARACION' 
  | 'LISTO_PARA_RETIRAR' 
  | 'ENTREGADO' 
  | 'CANCELADO_DEVUELTO';

export type EstadoTrabajo = 'PENDIENTE_APROBACION' | 'APROBADO' | 'RECHAZADO' | 'FINALIZADO';

export interface TrabajoItem {
  id?: number;
  descripcion: string;
  costoManoObra: number;
  costoRepuesto: number;
  estado: EstadoTrabajo;
}

export interface OrdenIngresoForm {
  clienteNombre: string;
  clienteTelefono: string;
  clienteEmail: string;
  categoria: CategoriaEquipo;
  marcaModelo: string;
  numeroSerieImei: string;
  fallaReportada: string;
  estadoFisicoIngreso: string;
  accesoriosEntregados: string;
}

export interface OrdenTrabajoResumen extends OrdenIngresoForm {
  id: number;
  nroOrden: string;
  fechaIngreso: string;
  estado: EstadoOrden;
  trabajos: TrabajoItem[];
  totalAbonar: number;
  pagosRegistrados: number;
}