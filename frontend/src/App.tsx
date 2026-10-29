import { useState, useEffect } from 'react';
import { checkBackendHealth } from './services/api';
import { FormularioIngreso } from './components/FormularioIngreso';
import { ListaOrdenes } from './components/ListaOrdenes';
import type { OrdenIngresoForm, OrdenTrabajoResumen } from './types';

export default function App() {
  const [backendStatus, setBackendStatus] = useState<string>('Verificando...');
  
  // Datos iniciales de demostración basados en el caso de TecnoRepair
  const [ordenes, setOrdenes] = useState<OrdenTrabajoResumen[]>([
    {
      id: 1,
      nroOrden: 'ORD-2026-001',
      clienteNombre: 'Carlos Gómez',
      clienteTelefono: '1144556677',
      clienteEmail: 'carlos@email.com',
      categoria: 'CELULAR',
      marcaModelo: 'Motorola Edge 30',
      numeroSerieImei: '356789012345678',
      fallaReportada: 'No carga la batería ni reconoce cargador',
      estadoFisicoIngreso: 'Tapa trasera marcada, pantalla sin fisuras',
      accesoriosEntregados: 'Sin funda ni cargador',
      fechaIngreso: '2026-10-27',
      estado: 'EN_REPARACION',
      trabajos: [
        {
          id: 1,
          descripcion: 'Reemplazo módulo pin de carga Tipo C',
          costoManoObra: 15000,
          costoRepuesto: 10000,
          estado: 'APROBADO',
        },
      ],
      totalAbonar: 25000,
      pagosRegistrados: 10000,
    },
  ]);

  useEffect(() => {
    checkBackendHealth().then((data) => {
      setBackendStatus(data.status === 'ok' ? 'Online 🟢' : 'Offline o sin conexión 🔴');
    });
  }, []);

  const handleNuevaOrden = (data: OrdenIngresoForm) => {
    const nueva: OrdenTrabajoResumen = {
      ...data,
      id: Date.now(),
      nroOrden: `ORD-2026-00${ordenes.length + 1}`,
      fechaIngreso: new Date().toISOString().split('T')[0],
      estado: 'RECIBIDO',
      trabajos: [
        {
          id: Date.now() + 1,
          descripcion: `Diagnóstico y revisión: ${data.fallaReportada}`,
          costoManoObra: 0,
          costoRepuesto: 0,
          estado: 'PENDIENTE_APROBACION',
        },
      ],
      totalAbonar: 0,
      pagosRegistrados: 0,
    };
    setOrdenes([nueva, ...ordenes]);
  };

  const handleCambiarEstado = (id: number, nuevoEstado: OrdenTrabajoResumen['estado']) => {
    setOrdenes((prev) =>
      prev.map((ord) => {
        if (ord.id === id) {
          // Bloqueo de entrega con saldo pendiente
          if (nuevoEstado === 'ENTREGADO' && ord.totalAbonar - ord.pagosRegistrados > 0) {
            alert('⚠️ Regla de negocio: No se puede marcar como ENTREGADO si la orden conserva saldo pendiente.');
            return ord;
          }
          return { ...ord, estado: nuevoEstado };
        }
        return ord;
      })
    );
  };

  const handleAgregarTrabajoAdicional = (
    ordenId: number,
    descripcion: string,
    manoObra: number,
    repuesto: number
  ) => {
    setOrdenes((prev) =>
      prev.map((ord) => {
        if (ord.id === ordenId) {
          const nuevoTrabajo = {
            id: Date.now(),
            descripcion,
            costoManoObra: manoObra,
            costoRepuesto: repuesto,
            estado: 'PENDIENTE_APROBACION' as const,
          };
          return {
            ...ord,
            trabajos: [...ord.trabajos, nuevoTrabajo],
            // No altera totalAbonar hasta ser aprobado
          };
        }
        return ord;
      })
    );
  };

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 p-4 md:p-8">
      <div className="max-w-6xl mx-auto">
        {/* Encabezado */}
        <header className="flex flex-col sm:flex-row justify-between items-start sm:items-center pb-6 mb-6 border-b border-slate-800 gap-4">
          <div>
            <h1 className="text-3xl font-extrabold text-indigo-400">TechFlow</h1>
            <p className="text-sm text-slate-400">
              Sistema de Gestión de Órdenes de Trabajo e Inteligencia Operativa
            </p>
          </div>
          <div className="flex items-center gap-3 bg-slate-800 px-4 py-2 rounded-xl border border-slate-700">
            <span className="text-xs text-slate-400 uppercase font-semibold">Backend FastAPI:</span>
            <span className="text-sm font-mono font-bold">{backendStatus}</span>
          </div>
        </header>

        {/* Formulario de Ingreso */}
        <FormularioIngreso onOrdenCreada={handleNuevaOrden} />

        {/* Listado de Órdenes con WhatsApp y Trabajos */}
        <ListaOrdenes
          ordenes={ordenes}
          onCambiarEstado={handleCambiarEstado}
          onAgregarTrabajoAdicional={handleAgregarTrabajoAdicional}
        />
      </div>
    </div>
  );
}