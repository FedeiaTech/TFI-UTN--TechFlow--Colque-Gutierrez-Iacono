# TechFlow — Sistema de Gestión de Órdenes de Trabajo, Reparaciones e Inteligencia Operativa para Servicios Técnicos

Trabajo Final Integrador — Tecnicatura en Programación, UTN.

## Equipo

- Brian Gutiérrez Colque
- David Gutiérrez
- Federico Iacono

## Propuesta

TechFlow es un sistema de gestión pensado para talleres de reparación técnica (celulares, PCs, notebooks, consolas), que cubre el ciclo completo de una orden de trabajo: desde la recepción del equipo hasta la entrega y cobro.

La propuesta surge de un relevamiento de campo (encuestas y entrevistas a 3 talleres de distinto tamaño), no de una idea genérica de ERP de retail. Los perfiles relevados mostraron problemas recurrentes: sobrecarga de actualizaciones de estado por WhatsApp, falta de visibilidad sobre la rentabilidad real del negocio, y necesidad de delegar tareas por roles (Recepcionista vs. Técnico) a medida que el equipo crece.

A partir de eso, el núcleo obligatorio del producto (P0) quedó definido por el siguiente flujo operativo, validado con el tutor:

```text
Cliente → Equipo → Orden → Diagnóstico → Cotización → Aprobación/Rechazo → Reparación → Listo → Entrega
```

Compras a proveedores, analítica avanzada e IA quedan fuera de esta instancia: se incorporan recién sobre un núcleo operativo ya validado.

### Módulos del P0

1. **Órdenes de Trabajo** (núcleo): estado global simple (Recibido → En proceso → Listo → Listo - No retirado → Entregado) con resultado (Reparado/Parcial/Sin reparación). Cada orden agrupa trabajos con su propio diagnóstico y estado técnico (por ejemplo, Esperando repuesto o En reparación), a cargo de un técnico responsable, con historial de cambios de estado. El estado de pago (Pendiente/Parcial/Pagado) no es un campo editable: se deriva de las cotizaciones aprobadas y los pagos.
2. **Clientes**: ficha de cliente con historial de equipos y órdenes.
3. **Cotizaciones y Cobros**: cotizaciones independientes por trabajo (ninguna se borra; el total de la orden es la suma de las aprobadas), pagos parciales y saldo pendiente. Cuenta corriente queda fuera del P0: por decisión del grupo (ver [caso de referencia](docs/entrega-2/Caso-Completo-Reparacion.md), regla 8) una orden no se entrega con saldo pendiente. Es una decisión no validada por un negocio real; se reincorpora si un negocio indica lo contrario.
4. **Repuestos y Stock**: modelado genérico (`equipos`/`repuestos` + `categoria_id`); el repuesto se reserva al cotizar y se descuenta de stock recién cuando el técnico confirma su uso.

### Fuera de alcance del P0 (para instancias posteriores)

- **Proveedores y Compras**: gestión de órdenes de compra a proveedores.
- **Panel de Métricas + IA**: dashboard analítico y generación de contenido/resúmenes vía IA. Se incorpora una vez que el núcleo operativo tenga datos reales, no como punto de partida.
- Facturación electrónica (AFIP), pasarelas de pago (Mercado Pago), impresoras fiscales, automatización vía WhatsApp API.

## Entregas

| Instancia | Fecha | Contenido |
| --- | --- | --- |
| 1.ª Entrega | 30/08/2026 | Propuesta + repositorio → [`docs/entrega-1/`](docs/entrega-1/TRABAJO-FINAL-INTEGRADOR-unificado.md) |
| 2.ª Entrega | 27/09/2026 | Caso completo, esquema de base de datos y módulos P0 → [`docs/entrega-2/`](docs/entrega-2/) |
| Entrega Final | 14/11/2026 | Código fuente, despliegue, documentación técnica y video |

Documentos de la 2.ª entrega (índice completo en [`docs/entrega-2/`](docs/entrega-2/README.md)):

- [01 — Contexto, Problemática y Relevamiento](docs/entrega-2/01-contexto-problematica-y-relevamiento.md)
- [02 — Propuesta de Valor, Viabilidad y Criterios](docs/entrega-2/02-propuesta-valor-y-viabilidad.md)
- [03 — Objetivos, Alcance y Módulos P0](docs/entrega-2/03-objetivos-alcance-y-modulos.md)
- [04 — Caso Completo de Reparación y Reglas de Negocio](docs/entrega-2/04-caso-completo-reparacion.md)
- [05 — Especificación de Requerimientos (SRS ISO 29148)](docs/entrega-2/05-especificacion-requerimientos.md)
- [06 — Casos de Uso y Actores](docs/entrega-2/06-casos-de-uso-y-actores.md)
- [07 — Modelo de Dominio y Máquinas de Estado](docs/entrega-2/07-modelo-dominio-y-maquinas-estado.md)
- [08 — Diseño UX, Arquitectura de Información y Pantallas](docs/entrega-2/08-diseno-ux-y-flujos-pantalla.md)
- [09 — Organización del Equipo y Roles](docs/entrega-2/09-roles-y-organizacion-equipo.md)
- [10 — Arquitectura Técnica y Patrones de Diseño](docs/entrega-2/10-arquitectura-tecnica.md)
- [11 — Esquema de Base de Datos y Persistencia](docs/entrega-2/11-esquema-base-datos.md) ([DDL](database/postgresql/schema.sql))
- [Diagramas PlantUML editables (.puml)](docs/entrega-2/diagramas/)

## Plan de trabajo

1. Propuesta + repositorio (1.ª entrega, completa).
2. Caso de referencia, diseño de base de datos y definición de módulos (2.ª entrega, conforme con correcciones según la devolución del tutor del 05-10).
3. Implementación del MVP: núcleo operativo (órdenes, clientes, cotizaciones, stock) primero, analítica e IA al final.
4. Despliegue online, informe final y video explicativo.
5. Defensa oral ante el comité.

## Stack tecnológico

- **Frontend**: React + TypeScript (Vite), Tailwind CSS, Zustand, TanStack (Query/Table/Form). Hosting: Vercel. Detalle en [`frontend/README.md`](frontend/README.md).
- **Backend**: FastAPI (Python 3.10+), SQLAlchemy/SQLModel, OAuth2 + JWT. Hosting: Render. Detalle en [`backend/README.md`](backend/README.md).
- **Base de datos**: PostgreSQL, alojada en Supabase como Postgres administrado, sin adoptar el resto de su plataforma.
- **Gestión de proyecto**: Trello (Kanban).
- **Control de versiones**: Git, con ramas `main`/`develop`/`feature`.

## Estructura del repositorio

```text
/docs
  /entrega-1    — propuesta unificada de la 1.ª entrega (Markdown navegable)
  /entrega-2    — caso de referencia, esquema de base de datos y módulos de la 2.ª entrega
/database       — scripts y migraciones (postgresql/)
/frontend       — aplicación React (estructura inicial; código a partir de la implementación del MVP)
/backend        — API FastAPI (estructura inicial; código a partir de la implementación del MVP)
/Devoluciones   — devoluciones formales del tutor
```
