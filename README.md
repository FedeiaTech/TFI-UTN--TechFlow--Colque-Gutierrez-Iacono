# TechFlow — Sistema de Gestión de Órdenes de Trabajo, Reparaciones e Inteligencia Operativa para Servicios Técnicos

Trabajo Final Integrador — Tecnicatura en Programación, UTN.

## Equipo

- Brian Gutiérrez Colque
- David Gutiérrez
- Federico Iacono

## Propuesta

TechFlow es un sistema de gestión pensado para talleres de reparación técnica (celulares, PCs, notebooks, consolas), que cubre el ciclo completo de una orden de trabajo: desde la recepción del equipo hasta la entrega y cobro.

La propuesta surge de un relevamiento de campo (encuestas y entrevistas a 3 talleres de distinto tamaño), no de una idea genérica de ERP de retail. Los perfiles relevados mostraron problemas recurrentes: sobrecarga de actualizaciones de estado por WhatsApp, falta de visibilidad sobre la rentabilidad real del negocio, y necesidad de delegar tareas por roles (Recepcionista vs. Técnico) a medida que el equipo crece.

A partir de eso, el núcleo del producto quedó definido por el siguiente pipeline:

```
Órdenes de Trabajo → Clientes → Presupuestos → Repuestos/Stock → Ventas → Analítica → IA
```

La IA (generación de descripciones, resúmenes de ventas en lenguaje natural) se suma al final, sobre un núcleo operativo ya funcional — no es el punto de partida del desarrollo.

### Módulos

1. **Órdenes de Trabajo** (núcleo): flujo de estados Recibido → Diagnosticado → Presupuestado → Aprobado/Rechazado → En Reparación → Listo → Entregado/Cobrado.
2. **Presupuestos y Cobros**: presupuestos por orden, pagos parciales y cuenta corriente.
3. **Repuestos y Stock**: modelado genérico (`equipos`/`repuestos` + `categoria_id`), sin tablas específicas por tipo de dispositivo.
4. **Clientes y Proveedores**.
5. **Panel de Métricas + IA**: dashboard analítico y generación de contenido/resúmenes vía IA (Gemini API).

**Fuera de alcance del MVP**: facturación electrónica (AFIP), integración con pasarelas de pago (Mercado Pago), impresoras fiscales, automatización vía WhatsApp API.

## Plan de trabajo

1. Propuesta + repositorio (esta entrega).
2. Diseño de base de datos y definición de módulos, con validación del tutor y del comité.
3. Implementación del MVP: núcleo operativo (órdenes, clientes, presupuestos, stock) primero, analítica e IA al final.
4. Despliegue online, informe final y video explicativo.
5. Defensa oral ante el comité.

## Stack tecnológico

- **Frontend**: React + TypeScript (Vite), Tailwind CSS, Zustand, TanStack (Query/Table/Form). Hosting: Vercel o Netlify.
- **Backend**: Spring Boot (Java) o FastAPI (Python + Pydantic/SQLModel), autenticación JWT. Hosting: Render o Railway.
- **Base de datos** (persistencia poliglota): PostgreSQL (datos transaccionales — ventas, saldos, usuarios, clientes) + MongoDB (catálogo de especificaciones dinámicas, logs de auditoría, registros no estructurados). Cloud: Supabase/Aiven (Postgres) + MongoDB Atlas.
- **Gestión de proyecto**: Trello (Kanban).
- **Control de versiones**: Git, con ramas `main`/`develop`/`feature`.

## Estructura del repositorio

```
/frontend       — aplicación React
/backend        — API (Spring Boot o FastAPI)
/database       — scripts y migraciones (postgresql/, mongodb/)
/docs           — documentación y entregas
/propuesta-original — versión original de la propuesta, previa a la unificación
TRABAJO FINAL INTEGRADOR - unificado.docx — documento de propuesta unificado
```
