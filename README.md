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
Cliente → Equipo → Orden → Diagnóstico → Presupuesto → Aprobación/Rechazo → Reparación → Listo → Entrega
```

Compras a proveedores, analítica avanzada e IA quedan fuera de esta instancia: se incorporan recién sobre un núcleo operativo ya validado.

### Módulos del P0

1. **Órdenes de Trabajo** (núcleo): flujo de estados Recibido → Diagnosticado → Presupuestado → Esperando aprobación adicional → Aprobado → Esperando repuesto → En Reparación → Listo → Listo - No retirado → Entregado, con estado de pago (Pendiente/Parcial/Pagado) llevado como campo separado.
2. **Clientes**: ficha de cliente con historial de equipos y órdenes.
3. **Presupuestos y Cobros**: presupuestos versionados por orden (ninguna versión se borra), pagos parciales y saldo pendiente. Cuenta corriente queda fuera del P0: el [caso de referencia](entrega-2/Caso-Completo-Reparacion.md) confirma que el taller no entrega equipos con saldo pendiente; se reincorpora si otro taller confirma lo contrario.
4. **Repuestos y Stock**: modelado genérico (`equipos`/`repuestos` + `categoria_id`); el repuesto se reserva al presupuestar y se descuenta de stock recién cuando el técnico confirma su uso.

### Fuera de alcance del P0 (para instancias posteriores)

- **Proveedores y Compras**: gestión de órdenes de compra a proveedores.
- **Panel de Métricas + IA**: dashboard analítico y generación de contenido/resúmenes vía IA. Se incorpora una vez que el núcleo operativo tenga datos reales, no como punto de partida.
- Facturación electrónica (AFIP), pasarelas de pago (Mercado Pago), impresoras fiscales, automatización vía WhatsApp API.

## Entregas

| Instancia | Fecha | Contenido |
| --- | --- | --- |
| 1.ª Entrega | 30/08/2026 | Propuesta + repositorio → [`entrega-1/`](entrega-1/TRABAJO-FINAL-INTEGRADOR-unificado.md) |
| 2.ª Entrega | 27/09/2026 | Caso completo, esquema de base de datos, módulos P0 y arquitectura → [`entrega-2/`](entrega-2/) |
| Entrega Final | 14/11/2026 | Código fuente, despliegue, documentación técnica y video |

Documentos de la 2.ª entrega:

- [Caso completo de reparación](entrega-2/Caso-Completo-Reparacion.md)
- [Esquema de base de datos](docs/Esquema-Base-Datos.md) ([DDL](database/postgresql/schema.sql))
- [Módulos del P0](docs/Modulos-P0.md)
- [Arquitectura del proyecto](docs/Arquitectura.md)

## Plan de trabajo

1. Propuesta + repositorio (1.ª entrega, completa).
2. Caso de referencia, diseño de base de datos, definición de módulos y arquitectura (2.ª entrega, pendiente de validación del tutor y del comité).
3. Implementación del MVP: núcleo operativo (órdenes, clientes, presupuestos, stock) primero, analítica e IA al final.
4. Despliegue online, informe final y video explicativo.
5. Defensa oral ante el comité.

## Stack tecnológico

- **Frontend**: React + TypeScript (Vite), Tailwind CSS, Zustand, TanStack (Query/Table/Form). Hosting: Vercel.
- **Backend**: FastAPI (Python 3.10+), SQLAlchemy, OAuth2 + JWT. Hosting: Render.
- **Base de datos**: PostgreSQL. Alojada en Supabase como Postgres administrado, sin adoptar el resto de su plataforma.
- **Gestión de proyecto**: Trello (Kanban).
- **Control de versiones**: Git, con ramas `main`/`develop`/`feature`.

Ver justificación completa de cada decisión técnica en [docs/Arquitectura.md](docs/Arquitectura.md).

## Estructura del repositorio

```text
/entrega-1      — propuesta unificada de la 1.ª entrega (Markdown navegable)
/entrega-2      — caso de referencia, esquema de base de datos y módulos de la 2.ª entrega
/docs           — arquitectura del proyecto y documentación técnica
/database       — scripts y migraciones (postgresql/)
/frontend       — aplicación React (estructura inicial; código a partir de la implementación del MVP)
/backend        — API FastAPI (estructura inicial; código a partir de la implementación del MVP)
/Devoluciones   — devoluciones formales del tutor
```

