import React, { useState } from 'react';
import type { OrdenTrabajoResumen } from '../types';

interface Props {
  ordenes: OrdenTrabajoResumen[];
  onCambiarEstado: (id: number, nuevoEstado: OrdenTrabajoResumen['estado']) => void;
  onAgregarTrabajoAdicional: (id: number, descripcion: string, manoObra: number, repuesto: number) => void;
}

export const ListaOrdenes: React.FC<Props> = ({ ordenes, onCambiarEstado, onAgregarTrabajoAdicional }) => {
  const [copiadoId, setCopiadoId] = useState<number | null>(null);
  const [ordenNuevaFallaId, setOrdenNuevaFallaId] = useState<number | null>(null);
  const [descripcionFalla, setDescripcionFalla] = useState('');
  const [manoObraFalla, setManoObraFalla] = useState(0);
  const [repuestoFalla, setRepuestoFalla] = useState(0);

  const generarMensajeWhatsApp = (orden: OrdenTrabajoResumen) => {
    const saldoPendiente = orden.totalAbonar - orden.pagosRegistrados;
    return `Hola ${orden.clienteNombre}! Desde el servicio técnico te informamos el estado de tu equipo ${orden.marcaModelo} (Orden ${orden.nroOrden}):
- Estado actual: ${orden.estado}
- Saldo pendiente: $${saldoPendiente.toLocaleString('es-AR')}
Cualquier consulta estamos a disposición.`;
  };

  const copiarAlPortapapeles = (orden: OrdenTrabajoResumen) => {
    const texto = generarMensajeWhatsApp(orden);
    navigator.clipboard.writeText(texto);
    setCopiadoId(orden.id);
    setTimeout(() => setCopiadoId(null), 3000);
  };

  const abrirEnlaceWhatsApp = (orden: OrdenTrabajoResumen) => {
    const texto = encodeURIComponent(generarMensajeWhatsApp(orden));
    window.open(`https://wa.me/?text=${texto}`, '_blank');
  };

  const handleGuardarNuevaFalla = (ordenId: number) => {
    if (!descripcionFalla) return;
    onAgregarTrabajoAdicional(ordenId, descripcionFalla, Number(manoObraFalla), Number(repuestoFalla));
    setOrdenNuevaFallaId(null);
    setDescripcionFalla('');
    setManoObraFalla(0);
    setRepuestoFalla(0);
  };

  return (
    <div className="bg-slate-800 rounded-xl border border-slate-700 p-6 shadow-lg">
      <h2 className="text-xl font-bold text-slate-100 mb-4 flex items-center justify-between">
        <span>📋 Órdenes de Trabajo Activas</span>
        <span className="text-xs bg-slate-700 px-3 py-1 rounded-full text-slate-300 font-normal">
          {ordenes.length} registradas
        </span>
      </h2>

      <div className="space-y-4">
        {ordenes.map((orden) => {
          const saldo = orden.totalAbonar - orden.pagosRegistrados;

          return (
            <div key={orden.id} className="bg-slate-900 border border-slate-700/80 rounded-xl p-5 hover:border-slate-600 transition-colors">
              <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-2 mb-3 border-b border-slate-800 pb-3">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-sm font-bold text-indigo-400">{orden.nroOrden}</span>
                    <span className="text-sm font-semibold text-slate-200">{orden.marcaModelo}</span>
                    <span className="text-xs px-2 py-0.5 rounded bg-slate-800 text-slate-400 border border-slate-700">
                      {orden.categoria}
                    </span>
                  </div>
                  <p className="text-xs text-slate-400 mt-1">
                    Cliente: <strong className="text-slate-300">{orden.clienteNombre}</strong> ({orden.clienteTelefono})
                  </p>
                </div>

                <div className="flex items-center gap-2">
                  <select
                    value={orden.estado}
                    onChange={(e) => onCambiarEstado(orden.id, e.target.value as OrdenTrabajoResumen['estado'])}
                    className="bg-slate-800 border border-slate-700 text-xs text-slate-200 rounded-lg px-2 py-1.5 focus:outline-none"
                  >
                    <option value="RECIBIDO">Recibido</option>
                    <option value="EN_DIAGNOSTICO">En Diagnóstico</option>
                    <option value="EN_REPARACION">En Reparación</option>
                    <option value="LISTO_PARA_RETIRAR">Listo para Retirar</option>
                    <option value="ENTREGADO">Entregado</option>
                    <option value="CANCELADO_DEVUELTO">Devuelto / Cancelado</option>
                  </select>
                </div>
              </div>

              {/* Falla y condiciones físicas registradas */}
              <div className="text-xs text-slate-400 grid grid-cols-1 md:grid-cols-3 gap-2 mb-3">
                <p><strong>Falla:</strong> {orden.fallaReportada}</p>
                <p><strong>Estado ingreso:</strong> {orden.estadoFisicoIngreso || 'Sin detalles'}</p>
                <p><strong>Accesorios:</strong> {orden.accesoriosEntregados || 'Sin accesorios'}</p>
              </div>

              {/* Lista de trabajos / fallas adicionales */}
              <div className="bg-slate-950/60 rounded-lg p-3 border border-slate-800 mb-3">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Trabajos / Cotizaciones</span>
                  <button
                    onClick={() => setOrdenNuevaFallaId(orden.id)}
                    className="text-xs text-indigo-400 hover:text-indigo-300 font-medium underline"
                  >
                    + Detectar nueva falla (Trabajo adicional)
                  </button>
                </div>

                <div className="space-y-1.5">
                  {orden.trabajos.map((trabajo, index) => (
                    <div key={index} className="flex justify-between items-center text-xs text-slate-300 py-1 border-b border-slate-800/60 last:border-0">
                      <span>• {trabajo.descripcion}</span>
                      <div className="flex items-center gap-3">
                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                          trabajo.estado === 'APROBADO' ? 'bg-emerald-950 text-emerald-400 border border-emerald-800' :
                          trabajo.estado === 'PENDIENTE_APROBACION' ? 'bg-amber-950 text-amber-400 border border-amber-800' :
                          'bg-slate-800 text-slate-400'
                        }`}>
                          {trabajo.estado}
                        </span>
                        <span className="font-mono text-slate-200">
                          ${(trabajo.costoManoObra + trabajo.costoRepuesto).toLocaleString('es-AR')}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>

                {/* Subformulario para agregar nueva falla sin romper lo aprobado */}
                {ordenNuevaFallaId === orden.id && (
                  <div className="mt-3 p-3 bg-slate-900 border border-indigo-900/50 rounded-lg">
                    <p className="text-xs font-semibold text-indigo-300 mb-2">Cargar hallazgo adicional durante reparación:</p>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-2 mb-2">
                      <input
                        type="text"
                        placeholder="Descripción de la nueva falla"
                        value={descripcionFalla}
                        onChange={(e) => setDescripcionFalla(e.target.value)}
                        className="bg-slate-950 border border-slate-700 text-xs px-2 py-1 rounded text-slate-200"
                      />
                      <input
                        type="number"
                        placeholder="Mano de obra ($)"
                        value={manoObraFalla || ''}
                        onChange={(e) => setManoObraFalla(Number(e.target.value))}
                        className="bg-slate-950 border border-slate-700 text-xs px-2 py-1 rounded text-slate-200"
                      />
                      <input
                        type="number"
                        placeholder="Costo repuesto ($)"
                        value={repuestoFalla || ''}
                        onChange={(e) => setRepuestoFalla(Number(e.target.value))}
                        className="bg-slate-950 border border-slate-700 text-xs px-2 py-1 rounded text-slate-200"
                      />
                    </div>
                    <div className="flex justify-end gap-2">
                      <button
                        onClick={() => setOrdenNuevaFallaId(null)}
                        className="text-xs px-2 py-1 text-slate-400 hover:text-slate-200"
                      >
                        Cancelar
                      </button>
                      <button
                        onClick={() => handleGuardarNuevaFalla(orden.id)}
                        className="text-xs bg-indigo-600 hover:bg-indigo-500 text-white px-3 py-1 rounded font-medium"
                      >
                        Registrar Falla
                      </button>
                    </div>
                  </div>
                )}
              </div>

              {/* Pie de orden: Saldos y WhatsApp */}
              <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 pt-2">
                <div className="flex items-center gap-4 text-xs font-mono">
                  <span>Total aprobado: <strong className="text-slate-200">${orden.totalAbonar.toLocaleString('es-AR')}</strong></span>
                  <span>Pagos: <strong className="text-emerald-400">${orden.pagosRegistrados.toLocaleString('es-AR')}</strong></span>
                  <span className={`font-bold ${saldo > 0 ? 'text-amber-400' : 'text-emerald-400'}`}>
                    Saldo: ${saldo.toLocaleString('es-AR')}
                  </span>
                </div>

                {/* Botones de acción WhatsApp */}
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => copiarAlPortapapeles(orden)}
                    className="bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-600 px-3 py-1 rounded-lg text-xs font-medium transition-colors"
                  >
                    {copiadoId === orden.id ? '✓ Mensaje Copiado!' : '📋 Copiar p/ WhatsApp'}
                  </button>
                  <button
                    onClick={() => abrirEnlaceWhatsApp(orden)}
                    className="bg-emerald-600 hover:bg-emerald-500 text-white px-3 py-1 rounded-lg text-xs font-medium transition-colors flex items-center gap-1 shadow-sm"
                  >
                    <span>💬</span> Enviar a Cliente
                  </button>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};