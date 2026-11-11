# Backend — TechFlow

> API REST del núcleo P0: clientes, equipos, órdenes, trabajos, cotizaciones, reservas de repuestos y pagos. Desplegada en https://techflow-api.onrender.com ([Swagger](https://techflow-api.onrender.com/docs)).

## Stack

- **FastAPI** (Python 3.10+)
- **SQLAlchemy 2.x** (no se usa SQLModel) con **psycopg 3** para persistencia
- **PostgreSQL** como base de datos
- Autenticación **OAuth2 + JWT**: en revisión, no incluida en esta versión

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

La base se crea con `database/postgresql/schema.sql` y los datos de demostración (técnico y repuestos, que la API no expone por endpoint) se cargan con `database/postgresql/seed.sql`. Con Supabase, `DATABASE_URL` debe apuntar al **Session pooler** (puerto 5432): el Transaction pooler no soporta los *prepared statements* que usa psycopg 3.

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

Render, configurado como código en [`render.yaml`](../render.yaml): construye desde `backend/`, arranca con `uvicorn` y usa `/health` como health check. `DATABASE_URL` se carga desde el panel de Render, nunca en el repositorio.

---

> **Enfoque de implementación**: el modelo se valida construyendo. Se modela, se implementa un recorrido pequeño, se comprueba, se corrige el modelo y se continúa.
>
> El esquema vigente está en [`database/postgresql/schema.sql`](../database/postgresql/schema.sql). Las pruebas de backend obligatorias están descriptas en [`docs/entrega-2/11-esquema-base-datos.md`](../docs/entrega-2/11-esquema-base-datos.md).
