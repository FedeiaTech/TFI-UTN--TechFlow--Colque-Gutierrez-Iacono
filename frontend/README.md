# Frontend — TechFlow

> Este directorio contendrá la aplicación frontend a partir de la etapa de implementación (Entrega Final).

## Stack

- **React 18** + **TypeScript** (via Vite)
- **Tailwind CSS** para estilos
- **Zustand** para estado global
- **TanStack** (Query, Table, Form) para data fetching, tablas y formularios

## Estructura prevista

```text
frontend/
├── src/
│   ├── components/     — componentes reutilizables
│   ├── pages/          — páginas/vistas de la aplicación
│   ├── services/       — llamadas a la API REST
│   ├── store/          — estado global (Zustand)
│   ├── types/          — tipos e interfaces TypeScript
│   └── utils/          — funciones utilitarias
├── public/
├── package.json
├── vite.config.ts
├── tailwind.config.js
└── tsconfig.json
```

## Hosting

Vercel (deploy automático desde GitHub).

---

> **Enfoque de implementación**: el modelo se valida construyendo. Se modela, se implementa un recorrido pequeño, se comprueba, se corrige el modelo y se continúa. No se espera a una aprobación total del diseño para empezar a codificar.
>
> **Primer objetivo**: una vertical ejecutable cliente → equipo → orden → diagnóstico → cotización → aprobación → reserva → reparación → listo → pago → entrega.
>
> **Segundo objetivo**: una segunda situación con trabajo adicional durante la reparación (nueva falla, nuevo trabajo y cotización independiente).
>
> El esquema vigente está en [`database/postgresql/schema.sql`](../database/postgresql/schema.sql). Las pruebas de backend obligatorias están en [`docs/entrega-2/Esquema-Base-Datos.md`](../docs/entrega-2/Esquema-Base-Datos.md).
