
# TRABAJO FINAL INTEGRADOR

> **Nota de archivo.** Este documento es la propuesta original de la 1.ª entrega (30/08/2026),
> convertida a Markdown el 25/09/2026 a pedido del tutor Oscar Londero para que el repositorio
> sea navegable desde GitHub sin depender de archivos Word/PDF. El original en `.docx` queda
> conservado en `borradores/.old/` como respaldo histórico. Para el estado **vigente** del proyecto
> (alcance P0, stack cerrado, persistencia en PostgreSQL), ver el `README.md` de la raíz y
> `docs/entrega-2/`.


## 1.ª Entrega — Propuesta de Proyecto y Repositorio

**Carrera:** Analista de Programación (Tecnicatura Universitaria en Programación Virtual - UTN)

**Proyecto:** TechFlow. Sistema de Gestión de Órdenes de Trabajo, Reparaciones e Inteligencia Operativa para Servicios Técnicos de Electrónica

**Integrantes del Equipo:**

Colque Gutiérrez, Brian

Gutiérrez, David

Iacono, Federico


## 1. Información General

**Nombre de la Propuesta / Producto:** TechFlow (Sistema de Gestión de Reparaciones y Analítica de Datos)

**Dominio de Aplicación:** Servicios técnicos de reparación y venta asociada de celulares, computadoras, notebooks y electrónica de consumo.

**Institución:** Universidad Tecnológica Nacional – Facultad Regional La Plata (UTN FRLP).

**Materia:** Trabajo Integrador Final de Carrera.

**Fecha de Presentación:** Agosto de 2026.


## 2. Resumen Ejecutivo (Executive Summary)

TechFlow es un software de gestión orientado a talleres y comercios de servicio técnico (celulares, PC, notebooks y electrónica en general) que centraliza el ciclo completo de una reparación: recepción del equipo, diagnóstico, presupuesto, gestión de repuestos y stock, reparación, aviso al cliente, entrega y cobro.

A diferencia de un ERP de retail genérico, TechFlow nace de un relevamiento de campo con negocios reales del sector, que identificó como problema central no la falta de stock en sí, sino la **ausencia de trazabilidad de todo el ciclo de reparación** y la fuga de tiempo y dinero que eso genera. El sistema integra órdenes de trabajo, clientes, presupuestos, repuestos/stock, ventas y un panel de analítica asistido por Inteligencia Artificial — incorporada una vez que el núcleo operativo esté validado con datos reales, no como punto de partida.

La arquitectura propuesta se apoya en un backend desacoplado y un servicio de persistencia gestionado — hoy evaluamos Firebase y Supabase, sopesando ventajas y desventajas de cada uno — junto con una interfaz frontend moderna, reactiva y pensada para el uso diario de técnicos y recepcionistas, no solo de administradores.


## 3. Planteo del Problema y Justificación del Dominio


### 3.1. Contexto del Territorio y Oportunidad

El sector de soporte técnico (celulares, computadoras y notebooks) creció de forma acelerada de la mano de emprendedores y micro-talleres que atienden de forma presencial o vía redes sociales. Son estructuras chicas (de 1 a 5 personas), con bajo acceso a herramientas de gestión, lo que las vuelve un nicho accesible para validar un producto con usuarios reales en poco tiempo.


### 3.2. Relevamiento de Campo

Se realizó una investigación de campo (encuesta vía formulario y entrevistas directas) a negocios de reparación y venta de celulares, PC y notebooks, identificando tres perfiles recurrentes:

- **Técnico autoempleado** (trabaja solo, sin venta de accesorios): su mayor dolor es el tiempo perdido respondiendo consultas de clientes por WhatsApp ("¿ya está?", "¿cuánto falta?") y el manejo de equipos abandonados.

- **Comercio unipersonal con venta** (repara y vende accesorios/equipos, multi-rubro): su dolor es el caos organizativo — no sabe cuánto gana realmente por mes ni cuánto capital tiene inmovilizado en stock.

- **Taller mediano** (3-5 personas, usa Excel/papel compartido): necesita delegar mediante roles (recepcionista vs. técnico) y visibilidad sobre dónde pierde dinero.


### 3.3. Problemática Detectada

- **Gestión de trabajos fragmentada:** cuadernos, WhatsApp y Excel dispersos, con pérdida de datos del equipo (IMEI, contraseñas) y confusión sobre técnico/estado asignado.

- **Comunicación manual repetitiva:** 1.5 a 2 horas diarias por técnico respondiendo consultas de estado por teléfono o WhatsApp.

- **Presupuestos informales:** sin desglose formal ni aceptación registrada, lo que genera pérdida del tiempo de diagnóstico invertido.

- **Stock fantasma:** control de repuestos "a ojo", con compras de más por miedo a quedarse sin piezas y capital inmovilizado en componentes obsoletos.

- **Rentabilidad invisible:** los negocios no pueden calcular cuánto ganan realmente por reparación, producto o mes (se estima un impacto de 20%-35% del margen neto por errores de diagnóstico y costeo).

- **Inventario rígido:** los talleres no reparan un solo tipo de equipo (celulares, PC, consolas), por lo que un modelo de datos centrado en "celulares" no sirve — se necesita un modelo genérico de "equipos/dispositivos" con categoría variable.


## 4. Definición de la Solución y Alcance del MVP

El objetivo general es desarrollar un sistema de gestión de órdenes de trabajo para servicios técnicos, aplicable a negocios reales del sector, accesible desde la nube, que reduzca tiempos improductivos y dé visibilidad real de la rentabilidad del negocio.

**Núcleo funcional validado por el relevamiento:**

Órdenes de trabajo → Clientes → Presupuestos → Repuestos/Stock → Ventas → Analítica → IA


### 4.1. Módulos Principales del Sistema

**Módulo 1: Gestión de Órdenes de Trabajo (núcleo del sistema)**

Alta de orden de ingreso de equipo: datos del cliente, tipo de equipo (categoría genérica: celular, PC, notebook, consola, etc.), falla reportada, estado inicial del dispositivo (para evitar reclamos por daños preexistentes).

Flujo de estados formal: Recibido → Diagnosticado → Presupuestado → Aprobado/Rechazado → En Reparación → Listo para Retirar → Entregado/Cobrado.

Asignación de técnico responsable por orden.

**Módulo 2: Presupuestos y Cobros**

Presupuesto formal con desglose de mano de obra y repuestos.

Registro de aceptación/rechazo del cliente (base para automatizar el envío por link en una futura iteración).

Gestión de señas, pagos parciales y saldos: una orden no puede marcarse como Entregada si el saldo pendiente es mayor a cero.

**Módulo 3: Gestión de Repuestos y Stock**

Modelo de inventario genérico (`equipos`/`repuestos` con `categoria_id`), no acoplado a un solo rubro.

Descuento automático de stock al asociar un repuesto a una orden.

Alertas de stock mínimo y visibilidad de capital inmovilizado.

**Módulo 4: Clientes y Proveedores**

Ficha de cliente con historial de órdenes y equipos ingresados.

Directorio de proveedores y órdenes de compra que actualizan stock automáticamente.

**Módulo 5: Panel de Métricas e Inteligencia Operativa**

Dashboard con rentabilidad neta real (ingresos - costo de repuestos - mano de obra), volumen de órdenes por estado, y repuestos de mayor rotación.

Roles de usuario (Administrador, Técnico, Recepcionista) con permisos diferenciados según el módulo.

**Asistencia por IA** (incorporada sobre el núcleo ya operativo, no como punto de partida):

Resumen ejecutivo en lenguaje natural de tendencias de órdenes y rentabilidad del período.

Generación de plantillas de mensajes de estado ("equipo listo para retirar") a partir de los datos de la orden.


### 4.2. Límites Declarados del Proyecto (Out of Scope para el MVP)

Integración con API de WhatsApp para envío automático de mensajes (se contempla como plantilla/link manual en esta versión; automatización completa queda para una iteración futura).

Facturación electrónica directa integrada con entes fiscales (ej. AFIP).

Pasarelas de pago bancarias con conciliación en tiempo real (ej. webhooks de Mercado Pago).

Módulo de impresión fiscal o controladores físicos de hardware de caja.


## 5. Arquitectura Técnica y Stack Tecnológico

La solución se basará en una arquitectura desacoplada (Frontend / Backend API REST / Persistencia mediante un servicio gestionado, aún en evaluación) para garantizar mantenibilidad, escalabilidad y buenas prácticas de ingeniería de software.


### 5.1. Stack Tecnológico Detallado

**Frontend:**

Librería / Lenguaje: React con TypeScript (vía Vite).

Diseño y UI: Tailwind CSS.

Gestión de Estado y Datos: Zustand (estado global) y TanStack Suite (Query, Table, Form).

**Backend:**

Servicio Principal: Spring Boot (Java) o FastAPI (Python) con Pydantic/SQLModel para la API REST.

Seguridad: Autenticación y autorización basada en JWT.

**Base de Datos (Servicio Gestionado — Decisión en Evaluación):**

Firebase: base de datos NoSQL (Firestore) con autenticación, hosting y funciones serverless integradas en un mismo ecosistema; evaluamos su velocidad de desarrollo frente a la rigidez de su modelo de consultas para reportes relacionales complejos.

Supabase: base de datos relacional (PostgreSQL) con autenticación y APIs autogeneradas; evaluamos su compatibilidad con SQL estándar y restricciones ACID frente a la necesidad de definir manualmente el modelo de datos.

**Servicios Cloud y Despliegue (obligatorio):**

Frontend Host: Vercel o Netlify.

Backend Host: Render o Railway.

Database Cloud: Firebase o Supabase, según la decisión que consolidemos antes de la 2.ª entrega (27/09).


## 6. Metodología de Trabajo, Plan de Entregas y Herramientas


### 6.1. Metodología Ágil

El equipo trabaja bajo un marco ágil simplificado basado en Kanban, organizando los requerimientos en historias de usuario y tareas técnicas.

**Gestión del Proyecto:** tablero centralizado en Trello (Backlog, En Proceso, En Revisión, Completado).

**Control de Versiones:** Git con flujo de ramas (main, develop, feature branches).

**Validación continua:** el relevamiento de campo inicial (3 negocios) es una hipótesis, no una conclusión definitiva; se planea ampliar la muestra e iterar sobre los requerimientos durante el desarrollo.


### 6.2. Cronograma General y Fechas Hito


| Instancia | Fecha Límite | Entregables Principales |
| --- | --- | --- |
| 1.ª Entrega | 30/08/2026 | Documento de propuesta formal, plan de trabajo, stack técnico y declaración del repositorio único de GitHub. |
| 2.ª Entrega | 27/09/2026 | Esquema DDL/DML de PostgreSQL, modelo de documentos en MongoDB, listado de módulos desarrollados y aprobación formal del tutor/comité. |
| Entrega Final | 14/11/2026 | Código fuente completo en GitHub, servicios desplegados en la nube, documentación técnica/README y video explicativo. |
| Defensa Oral | Mesa de Examen | Exposición oral y justificación del proyecto ante el comité evaluador. |


## 7. Estructura y Organización del Repositorio Único (GitHub)

Acorde a las normativas de la materia, la totalidad de los artefactos del sistema habitarán dentro de un único repositorio centralizado.

**Enlace al Repositorio:** [https://github.com/FedeiaTech/TFI-UTN--TechFlow--Colque-Gutierrez-Iacono.git](https://github.com/FedeiaTech/TFI-UTN--TechFlow--Colque-Gutierrez-Iacono.git)

**Estructura de Directorios Propuesta:**

```text
techflow-tfi/
├── .github/                 # Workflows y plantillas de código
├── docs/                    # Informes de entrega (1a, 2a y Final) y diagramas
│   ├── entrega-1/
│   ├── entrega-2/
│   └── diagramas/           # DER, diagramas de arquitectura y clases
├── frontend/                # Aplicación React + TypeScript + Vite
│   ├── src/
│   ├── package.json
│   └── tailwind.config.js
├── backend/                 # API REST (Spring Boot o FastAPI)
│   ├── src/
│   └── pom.xml / main.py
├── database/                # Scripts de persistencia
│   ├── postgresql/          # Scripts DDL, DML y migraciones
│   └── mongodb/             # Colecciones, esquemas JSON y scripts de inicialización
└── README.md                # Documentación general, instalación y links de despliegue
```
