import React, { useState } from 'react';
import type { OrdenIngresoForm } from '../types';

interface Props {
  onOrdenCreada: (nuevaOrden: OrdenIngresoForm) => void;
}

export const FormularioIngreso: React.FC<Props> = ({ onOrdenCreada }) => {
  const [formData, setFormData] = useState<OrdenIngresoForm>({
    clienteNombre: '',
    clienteTelefono: '',
    clienteEmail: '',
    categoria: 'CELULAR',
    marcaModelo: '',
    numeroSerieImei: '',
    fallaReportada: '',
    estadoFisicoIngreso: '',
    accesoriosEntregados: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.clienteNombre || !formData.clienteTelefono || !formData.marcaModelo) {
      alert('Por favor completá los campos obligatorios del cliente y equipo.');
      return;
    }
    onOrdenCreada(formData);
    setFormData({
      clienteNombre: '',
      clienteTelefono: '',
      clienteEmail: '',
      categoria: 'CELULAR',
      marcaModelo: '',
      numeroSerieImei: '',
      fallaReportada: '',
      estadoFisicoIngreso: '',
      accesoriosEntregados: '',
    });
  };

  return (
    <div className="bg-slate-800 rounded-xl border border-slate-700 p-6 shadow-lg mb-8">
      <h2 className="text-xl font-bold text-slate-100 mb-4 flex items-center gap-2">
        <span>📥</span> Nuevo Ingreso de Equipo (Recepción)
      </h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Datos del Cliente */}
        <div className="border-b border-slate-700 pb-4">
          <p className="text-xs font-bold uppercase tracking-wider text-indigo-400 mb-3">Datos del Cliente</p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            <div>
              <label className="block text-xs text-slate-300 mb-1">Nombre Completo *</label>
              <input
                type="text"
                name="clienteNombre"
                value={formData.clienteNombre}
                onChange={handleChange}
                placeholder="Ej. Juan Pérez"
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-indigo-500"
                required
              />
            </div>
            <div>
              <label className="block text-xs text-slate-300 mb-1">WhatsApp / Teléfono *</label>
              <input
                type="tel"
                name="clienteTelefono"
                value={formData.clienteTelefono}
                onChange={handleChange}
                placeholder="Ej. 1123456789"
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-indigo-500"
                required
              />
            </div>
            <div>
              <label className="block text-xs text-slate-300 mb-1">Email</label>
              <input
                type="email"
                name="clienteEmail"
                value={formData.clienteEmail}
                onChange={handleChange}
                placeholder="juan@email.com"
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-indigo-500"
              />
            </div>
          </div>
        </div>

        {/* Datos del Equipo */}
        <div className="border-b border-slate-700 pb-4">
          <p className="text-xs font-bold uppercase tracking-wider text-indigo-400 mb-3">Identificación del Dispositivo</p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            <div>
              <label className="block text-xs text-slate-300 mb-1">Categoría</label>
              <select
                name="categoria"
                value={formData.categoria}
                onChange={handleChange}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-indigo-500"
              >
                <option value="CELULAR">Celular</option>
                <option value="NOTEBOOK">Notebook</option>
                <option value="PC_ESCRITORIO">PC de Escritorio</option>
                <option value="CONSOLA">Consola</option>
                <option value="AUDIO">Audio</option>
                <option value="OTRO">Otro</option>
              </select>
            </div>
            <div>
              <label className="block text-xs text-slate-300 mb-1">Marca y Modelo *</label>
              <input
                type="text"
                name="marcaModelo"
                value={formData.marcaModelo}
                onChange={handleChange}
                placeholder="Ej. Samsung Galaxy S21"
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-indigo-500"
                required
              />
            </div>
            <div>
              <label className="block text-xs text-slate-300 mb-1">Nro Serie o IMEI (opcional)</label>
              <input
                type="text"
                name="numeroSerieImei"
                value={formData.numeroSerieImei}
                onChange={handleChange}
                placeholder="Opcional según equipo"
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-indigo-500"
              />
            </div>
          </div>
        </div>

        {/* Falla, Estado Físico y Accesorios */}
        <div>
          <p className="text-xs font-bold uppercase tracking-wider text-indigo-400 mb-3">Diagnóstico Inicial y Condiciones</p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            <div>
              <label className="block text-xs text-slate-300 mb-1">Falla Reportada *</label>
              <textarea
                name="fallaReportada"
                value={formData.fallaReportada}
                onChange={handleChange}
                rows={2}
                placeholder="No enciende, reinicios, módulo roto..."
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-indigo-500"
                required
              />
            </div>
            <div>
              <label className="block text-xs text-slate-300 mb-1">Estado Físico al Ingreso</label>
              <textarea
                name="estadoFisicoIngreso"
                value={formData.estadoFisicoIngreso}
                onChange={handleChange}
                rows={2}
                placeholder="Rayones en tapa trasera, golpes en bordes..."
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-indigo-500"
              />
            </div>
            <div>
              <label className="block text-xs text-slate-300 mb-1">Accesorios Entregados</label>
              <textarea
                name="accesoriosEntregados"
                value={formData.accesoriosEntregados}
                onChange={handleChange}
                rows={2}
                placeholder="Cargador original, funda plástica, cable USB..."
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-indigo-500"
              />
            </div>
          </div>
        </div>

        <div className="pt-2 flex justify-end">
          <button
            type="submit"
            className="bg-indigo-600 hover:bg-indigo-500 text-white font-medium py-2 px-5 rounded-lg text-sm transition-colors duration-150 shadow-md"
          >
            Registrar Orden de Ingreso
          </button>
        </div>
      </form>
    </div>
  );
};