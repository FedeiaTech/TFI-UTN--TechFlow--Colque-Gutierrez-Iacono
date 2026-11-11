# TechFlow — Gestión de Órdenes de Trabajo para Servicios Técnicos

Trabajo Final Integrador — Tecnicatura Universitaria en Programación, UTN.

TechFlow gestiona el ciclo completo de una reparación en un taller técnico (celulares, notebooks, consolas): desde que el equipo entra hasta que se entrega y se cobra, dejando registro de qué se hizo, quién lo hizo y cuánto se debe.

## Integrantes

- Brian Gutiérrez Colque
- David Gutiérrez
- Federico Iacono

## Entrega final

| Recurso | Enlace |
| --- | --- |
| API desplegada | https://techflow-api.onrender.com |
| Documentación interactiva (Swagger) | https://techflow-api.onrender.com/docs |
| Informe Final (PDF) | _pendiente_ |
| Video de presentación | _pendiente_ |
| Versión entregada | _pendiente (tag del repositorio)_ |

> **Primera carga lenta.** La API está en el plan gratuito de Render, que suspende el servicio tras 15 minutos sin uso. Si estaba dormida, el primer request tarda alrededor de 50 segundos; los siguientes responden normal. Un workflow de GitHub Actions ([`keepalive.yml`](.github/workflows/keepalive.yml)) la consulta cada 10 minutos para evitarlo.

## El problema

El proyecto surge de un relevamiento de campo con talleres de reparación de distinto tamaño ([evidencia](docs/entrega-2/01-contexto-problematica-y-relevamiento.md)). Los problemas que se repitieron:

- El estado de cada reparación vive en la memoria del técnico o en WhatsApp, y el cliente pregunta una y otra vez.
- Una misma orden suele tener varias fallas con tiempos distintos (una espera un repuesto, otra ya está lista), y un estado único no alcanza para representarlo.
- No queda claro cuánto debe el cliente ni qué repuestos ya están comprometidos para otra reparación.

## Estado de la entrega

### Implementado y probado

| Funcionalidad | Cómo se comprobó |
| --- | --- |
| Alta de cliente, equipo y orden de trabajo, con técnico responsable, estado físico y accesorios de ese ingreso | Test end-to-end y recorrido sobre el deploy |
| Varios trabajos por orden, cada uno con su diagnóstico y estado técnico propio | Escenario de falla nueva sobre el deploy |
| Cotizaciones independientes por trabajo, con precio guardado como *snapshot* | Test end-to-end |
| Reserva de repuesto al cotizar, con bloqueo de fila (`SELECT ... FOR UPDATE`); sin disponibilidad, la cotización se rechaza | Deploy: con stock 1, una segunda reserva responde 400. Falta un test automatizado de reservas simultáneas |
| Aprobación o rechazo por trabajo; el rechazo libera la reserva | Deploy, con la disponibilidad verificada en la base |
| Un trabajo declarado irreparable libera su reserva y deja de sumar al saldo | Deploy, con disponibilidad y saldo verificados en la base |
| Confirmación de uso: la reserva pasa a utilizada y se descuenta el stock en la misma transacción | Recorrido sobre el deploy, con el stock verificado en la base |
| La orden pasa sola a `listo` cuando todos sus trabajos terminaron, con resultado `reparado`, `parcial` o `sin_reparacion` | Test end-to-end y escenario de falla nueva |
| Pagos parciales; total, saldo y estado de pago calculados en vistas SQL, nunca editables a mano | Recorrido sobre el deploy |
| **Regla:** una orden con saldo pendiente no se puede entregar | Test end-to-end y deploy (responde 400) |
| **Regla:** el monto de un pago debe ser mayor a 0 | Deploy (responde 422) y `CHECK` en la base |
| **Regla:** una falla nueva durante la reparación genera otro trabajo sin alterar lo ya aprobado | Escenario de falla nueva sobre el deploy |
| Historial de cambios de estado de órdenes y trabajos, con usuario y fecha | Se registra en cada transición |

### No implementado en esta versión

Algunas de estas funcionalidades están diseñadas en la documentación de la 2.ª entrega, pero **no forman parte del sistema entregado**:

- **Autenticación JWT**: en revisión ([PR #4](https://github.com/FedeiaTech/TFI-UTN--TechFlow--Colque-Gutierrez-Iacono/pull/4)). Hoy el usuario que realiza cada acción se indica con el parámetro `usuario_id`.
- **Interfaz web**: hay un prototipo en revisión ([PR #5](https://github.com/FedeiaTech/TFI-UTN--TechFlow--Colque-Gutierrez-Iacono/pull/5)), no conectado a la API. El sistema se usa a través de la API y su documentación Swagger.
- Consultas y listados de órdenes, clientes e historial (la API solo expone el saldo de una orden).
- Mensaje de estado para enviar por WhatsApp.
- Paso de un trabajo a `esperando_repuesto`, reemplazo de una cotización pendiente y liberación manual de una reserva.
- Alerta automática de equipos listos y no retirados a los 30 días (los campos existen en la base, el proceso no).
- Roles diferenciados, proveedores y compras, métricas e IA (fuera del alcance desde la 2.ª entrega).

## Probar el sistema desplegado

Desde [Swagger](https://techflow-api.onrender.com/docs) se puede recorrer el flujo completo. La base tiene precargados ([`seed.sql`](database/postgresql/seed.sql)) los datos que la API no expone por endpoint:

- **Técnico de demostración:** id `6`. Usar este valor en `tecnico_id`, `usuario_id` y `registrado_por`. Es una cuenta ficticia, no corresponde a ningún integrante.
- **Repuestos:** id `6` (pantalla), id `7` (pin de carga, con stock 1 para probar la falta de disponibilidad) e id `8` (batería).

Recorrido sugerido:

1. `POST /api/v1/clientes` y `POST /api/v1/clientes/{id}/equipos`
2. `POST /api/v1/ordenes`
3. `POST /api/v1/ordenes/{id}/trabajos` y `PATCH /api/v1/ordenes/trabajos/{id}/diagnosticar`
4. `POST /api/v1/trabajos/{id}/cotizaciones` (un ítem de tipo `repuesto` reserva stock)
5. `PATCH /api/v1/cotizaciones/{id}/decidir` con `{"aprobar": true}`
6. `POST /api/v1/trabajos/{id}/confirmar-uso`
7. `PATCH /api/v1/ordenes/{id}/entregar`: falla mientras haya saldo
8. `POST /api/v1/ordenes/{id}/pagos` y volver a entregar

## Ejecutar localmente

Requiere Python 3.10 o superior y una base PostgreSQL. Los pasos detallados están en [`backend/README.md`](backend/README.md).

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
copy .env.example .env      # completar DATABASE_URL
uvicorn app.main:app --reload
```

La base se crea con [`database/postgresql/schema.sql`](database/postgresql/schema.sql) y se cargan los datos de demostración con [`seed.sql`](database/postgresql/seed.sql).

### Variables de entorno

| Variable | Descripción |
| --- | --- |
| `DATABASE_URL` | Conexión a PostgreSQL. En Supabase se usa el **Session pooler** (puerto 5432). |

Las credenciales nunca se versionan: el `.env` está excluido del repositorio y en Render la variable se carga desde el panel.

## Pruebas

```powershell
cd backend
pytest -v
```

- `tests/test_vertical_ejecutable.py`: recorre el flujo completo contra una base real y verifica el bloqueo de entrega con saldo pendiente.
- `tests/test_health.py`: disponibilidad de la API y de la base, sin exponer datos de conexión en los errores.

Las pruebas que necesitan base se omiten si no está definida `DATABASE_URL`.

## Arquitectura y tecnologías

Backend en capas (*routers* → *services* → *repositories* → modelos) sobre **FastAPI** y **SQLAlchemy 2** con **psycopg 3**. Base **PostgreSQL** administrada en **Supabase** (solo como base de datos, sin el resto de su plataforma). Despliegue en **Render**, configurado como código en [`render.yaml`](render.yaml).

Las reglas que no pueden depender de la disciplina del usuario están en la base: el saldo y el estado de pago se derivan en vistas, y los montos y cantidades tienen restricciones `CHECK`. Las que dependen de una transición, como la entrega con saldo o la confirmación de uso con descuento de stock, están en los *services*.

Detalle en [`docs/entrega-2/10-arquitectura-tecnica.md`](docs/entrega-2/10-arquitectura-tecnica.md).

## Documentación

- [1.ª entrega: propuesta](docs/entrega-1/TRABAJO-FINAL-INTEGRADOR-unificado.md)
- [2.ª entrega: análisis, modelo y arquitectura](docs/entrega-2/README.md) (11 documentos y diagramas)
- [Devoluciones del tutor](Devoluciones/)

## Estructura del repositorio

```text
backend/        API FastAPI (código, pruebas y dependencias)
database/       esquema PostgreSQL y datos de demostración
docs/           documentación de la 1.ª y 2.ª entrega
frontend/       reservado para la interfaz web (no incluida en esta versión)
Devoluciones/   devoluciones del tutor
render.yaml     configuración del despliegue
```
