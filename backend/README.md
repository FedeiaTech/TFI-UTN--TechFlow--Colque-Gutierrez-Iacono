# Backend — TechFlow

> Este directorio contendrá la API REST a partir de la etapa de implementación (Entrega Final).

## Stack

- **FastAPI** (Python 3.10+)
- **SQLAlchemy / SQLModel** para persistencia
- **OAuth2 + JWT** para autenticación
- **PostgreSQL** como base de datos

## Arquitectura interna (N-Capas)

```text
backend/
├── app/
│   ├── main.py         — punto de entrada (FastAPI)
│   ├── routers/        — controladores REST (capa de presentación)
│   ├── services/       — lógica de negocio (capa de servicio)
│   ├── repositories/   — acceso a datos (capa de persistencia)
│   ├── models/         — entidades (mapeo a tablas PostgreSQL)
│   ├── schemas/        — Pydantic (objetos de transferencia de datos - DTO)
│   ├── core/           — configuración (seguridad, CORS, settings, etc.)
│   └── database/       — conexión y dependencias de base de datos
├── requirements.txt
└── README.md
```

## Patrones aplicados

- **Repository Pattern** — aislamiento del acceso a datos
- **Service Layer** — lógica de negocio separada de los routers
- **DTO Pattern** — validación con Pydantic
- **State Pattern** — máquina de estados para órdenes de trabajo
- **Facade** — routers como fachada de servicios

## Hosting

Render (deploy desde GitHub, soporte nativo para Python/FastAPI).

---

> **Enfoque de implementación**: el modelo se valida construyendo. Se modela, se implementa un recorrido pequeño, se comprueba, se corrige el modelo y se continúa. No se espera a una aprobación total del diseño para empezar a codificar.
>
> **Primer objetivo**: una vertical ejecutable cliente → equipo → orden → diagnóstico → cotización → aprobación → reserva → reparación → listo → pago → entrega.
>
> **Segundo objetivo**: una segunda situación con trabajo adicional durante la reparación (nueva falla, nuevo trabajo y cotización independiente).
>
> El esquema vigente está en [`database/postgresql/schema.sql`](../database/postgresql/schema.sql). Las pruebas de backend obligatorias están en [`docs/entrega-2/Esquema-Base-Datos.md`](../docs/entrega-2/Esquema-Base-Datos.md).
