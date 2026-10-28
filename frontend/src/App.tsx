import { useEffect, useState } from 'react';
import { checkBackendHealth } from './services/api';

export default function App() {
  const [backendStatus, setBackendStatus] = useState<string>('Verificando...');

  useEffect(() => {
    checkBackendHealth().then((data) => {
      setBackendStatus(data.status === 'ok' ? 'Online 🟢' : 'Offline o sin conexión 🔴');
    });
  }, []);

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 flex flex-col items-center justify-center p-6">
      <div className="max-w-md w-full bg-slate-800 p-8 rounded-2xl shadow-xl border border-slate-700 text-center">
        <h1 className="text-3xl font-extrabold text-indigo-400 mb-2">TechFlow</h1>
        <p className="text-sm text-slate-400 mb-6">Sistema de Gestión Comercial e Inteligencia Operativa</p>

        <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 mb-6">
          <p className="text-xs text-slate-500 uppercase font-bold tracking-wider mb-1">Estado de la API (FastAPI)</p>
          <p className="text-lg font-mono font-semibold text-emerald-400">{backendStatus}</p>
        </div>

        <p className="text-xs text-slate-500">
          React + TypeScript + Tailwind CSS listo para maquetar módulos P0.
        </p>
      </div>
    </div>
  );
}