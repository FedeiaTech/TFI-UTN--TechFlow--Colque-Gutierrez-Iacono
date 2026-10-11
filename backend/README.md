# Backend — TechFlow

> Este directorio contiene el esqueleto de la API REST (FastAPI): configuración, conexión a PostgreSQL, endpoints de salud y pruebas. La lógica de dominio se incorporará de forma incremental.

## Stack

- **FastAPI** (Python 3.10+)
- **SQLAlchemy 2.x** (decisión tomada; no se usa SQLModel) con **psycopg 3** para persistencia
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

## Puesta en marcha local

Desde el directorio `backend/` (PowerShell en Windows):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
copy .env.example .env   # completar DATABASE_URL; el .env no se versiona
uvicorn app.main:app --reload
pytest
```

- `GET /health` responde `{"status":"ok"}` sin tocar la base.
- `GET /health/db` ejecuta `SELECT 1`; responde 503 con un mensaje genérico si falta `DATABASE_URL` o falla la conexión.
- `DATABASE_URL` admite `postgresql://...`; se normaliza a `postgresql+psycopg://` para SQLAlchemy.
- Las pruebas que requieren base se omiten si no hay `DATABASE_URL`.

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
