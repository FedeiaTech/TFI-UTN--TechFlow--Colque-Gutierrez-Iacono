# 03 — Objetivos, Alcance y Módulos del Sistema

## 1. Objetivos del Proyecto

### 1.1. Objetivo General
Desarrollar e implementar un sistema de software web para la gestión integral de órdenes de trabajo en servicios técnicos de electrónica, que asegure la trazabilidad completa del ciclo de reparación, desacople los estados técnicos de los estados financieros, prevenga inconsistencias en el control de repuestos y reduzca las interrupciones operativas derivadas de la comunicación con clientes.

### 1.2. Objetivos Específicos
1. **Modelar la orden de trabajo desagregada:** Permitir que una misma orden agrupe múltiples fallas o tareas técnicas independientes (trabajos), cada una con su propio diagnóstico, estado operativo y cotización asociada.
2. **Garantizar la integridad del presupuesto:** Implementar cotizaciones independientes por trabajo con snapshot inmutable de precios de catálogo y cantidades, derivando los totales mediante vistas para imposibilitar la manipulación arbitraria de montos.
3. **Asegurar la consistencia transaccional del stock:** Modelar el ciclo de reservas de repuestos (`reservada` $\rightarrow$ `utilizada` / `liberada`) y garantizar mediante bloqueos pesimistas de fila que nunca se produzca sobre-reserva en condiciones de concurrencia.
4. **Desacoplar la dimensión técnica de la financiera:** Mantener el estado operativo de la orden independiente del estado de pago, calculando saldos y estados de cobro (`pendiente`, `parcial`, `pagado`) de forma automática a partir de cotizaciones aprobadas y pagos registrados.
5. **Asegurar la regla de no entrega con saldo deudor:** Validar programáticamente en backend que ninguna orden pase al estado `entregado` mientras conserve un saldo pendiente mayor a cero.
6. **Facilitar la comunicación sin intermediación de APIs de terceros:** Implementar un mecanismo de generación de mensajes de estado preformateados, copiables en un solo clic, mitigando las consultas repetitivas de WhatsApp.
7. **Proveer una arquitectura limpia y desplegable:** Estructurar el backend en N-capas (FastAPI) desacoplado de la interfaz SPA (React + TypeScript), con persistencia relacional estricta en PostgreSQL y despliegue funcional en servicios en la nube.

---

## 2. Definición del Alcance por Prioridades (Matriz MoSCoW)

A fin de cumplir rigurosamente con la indicación del tutor de **recortar el alcance y evitar la deriva hacia un ERP sobredimensionado** (Observación 2 de la 1.ª Devolución), el desarrollo se categoriza en tres fases:

```text
+-------------------------------------------------------------------------------+
| P0 — OBLIGATORIO (MVP - Entrega Regular y Final)                              |
| Circuito vertical de reparación cerrado: Clientes, Equipos, Órdenes,          |
| Trabajos, Cotizaciones, Pagos, Stock básico con reservas, Usuarios y trazabilidad.|
+-------------------------------------------------------------------------------+
                                        │
                                        ▼
+-------------------------------------------------------------------------------+
| P1 — FASE SECUNDARIA (Post-validación del núcleo)                             |
| Gestión de proveedores, órdenes de compra de reposición, matriz avanzada de  |
| permisos (Admin/Técnico/Recepcionista), enlace público seguro para clientes.  |
+-------------------------------------------------------------------------------+
                                        │
                                        ▼
+-------------------------------------------------------------------------------+
| P2 — FASE TERCIARIA / EXTENSIÓN                                               |
| Analítica avanzada con margen directo real, facturación electrónica fiscal,   |
| integración oficial con Meta WhatsApp API, asistencia generativa por IA.      |
+-------------------------------------------------------------------------------+
```

---

## 3. Detalle de Módulos del Núcleo Operativo (P0)

### M1. Módulo de Clientes
- **Propósito:** Registro y administración de datos de contacto de las personas que solicitan servicios en el taller.
- **Funcionalidades:**
  - Alta rápida de cliente durante la recepción del equipo.
  - Búsqueda por nombre o teléfono.
  - Consulta de la ficha de cliente con historial de equipos y órdenes asociadas.

### M2. Módulo de Equipos
- **Propósito:** Registro de los dispositivos que ingresan al taller, manteniendo sus atributos estructurales e invariables a lo largo del tiempo.
- **Funcionalidades:**
  - Asociación unívoca con el cliente propietario.
  - Registro de tipo genérico (`celular`, `notebook`, `consola`, etc.), marca y modelo.
  - Identificación por `numero_serie` genérico y campo `imei` opcional (solo aplicable a telefonía celular).
  - Preservación del dispositivo ante reingresos sucesivos por nuevas reparaciones.

### M3. Módulo de Órdenes de Trabajo (Núcleo)
- **Propósito:** Representación formal del ingreso del equipo al taller, orquestando el flujo global de atención.
- **Funcionalidades:**
  - Apertura de orden asociando un equipo y asignando un **técnico responsable** (usuario del sistema).
  - Captura del **estado físico de ingreso** (rayones, golpes, tapas faltantes) y **accesorios entregados** específicos de ese ingreso.
  - Máquina de estados global simple: `recibido` $\rightarrow$ `en_proceso` $\rightarrow$ `listo` $\rightarrow$ `entregado`, con variante temporal `listo_no_retirado`.
  - Determinación del `resultado_orden` al momento de quedar lista (`reparado`, `parcial`, `sin_reparacion`).
  - Historial inmutable de cambios de estado con fecha, usuario y motivo.
  - Generación de comprobante y función de "copiar mensaje de estado" para comunicación directa.

### M4. Módulo de Trabajos Técnicos y Diagnóstico
- **Propósito:** Gestión desagregada de cada falla, hallazgo o tarea técnica que se efectúa sobre el equipo dentro de la orden.
- **Funcionalidades:**
  - Creación de trabajos iniciales (según falla reportada) o trabajos adicionales (hallazgos posteriores).
  - Registro de diagnóstico técnico por trabajo.
  - Ciclo de estados técnicos independiente: `pendiente_diagnostico` $\rightarrow$ `diagnosticado` $\rightarrow$ `esperando_repuesto` $\rightarrow$ `en_reparacion` $\rightarrow$ `terminado` / `irreparable` / `cancelado`.
  - Historial de estados de cada trabajo con responsable y motivo.

### M5. Módulo de Cotizaciones y Cobros
- **Propósito:** Generación, aprobación y liquidación económica de los trabajos técnicos.
- **Funcionalidades:**
  - Cotizaciones independientes por trabajo (numeradas secuencialmente, una sola vigente por trabajo).
  - Desglose de ítems (`repuesto`, `mano_obra`, `descripcion`) con cantidad y precio unitario snapshot.
  - Registro de decisión del cliente: `aprobada` o `rechazada` (con motivo). Las cotizaciones nunca se borran.
  - Registro de pagos parciales o totales asociados a la orden (`monto > 0`).
  - Cálculo dinámico de total aprobado, total pagado, saldo pendiente y estado financiero (`pendiente`, `parcial`, `pagado`) mediante vistas SQL.
  - Bloqueo de entrega si `saldo > 0`.

### M6. Módulo de Repuestos e Inventario
- **Propósito:** Administración de piezas y componentes para su asignación a las cotizaciones.
- **Funcionalidades:**
  - Catálogo de repuestos clasificados por categoría.
  - Precio de referencia de catálogo y stock total disponible.
  - Creación de reservas automáticas al presupuestar un ítem de repuesto.
  - Ciclo de vida de reservas: `reservada` $\rightarrow$ `utilizada` (descuenta stock en la misma transacción) o `liberada` (en caso de rechazo de la cotización o cancelación del trabajo).
  - Vista de disponibilidad neta en pañol en tiempo real.

### M7. Módulo de Usuarios y Trazabilidad
- **Propósito:** Control de identidad mínima y responsabilidad operativa.
- **Funcionalidades:**
  - Registro de operadores (nombre, email único, hash de contraseña mediante algoritmo seguro).
  - Autenticación stateless mediante tokens JWT.
  - Identificación del técnico responsable de cada orden y registro de autoría en cada pago y cambio de estado.

---

## 4. Límites Declarados (Módulos Fuera de Alcance para el P0)

Para evitar la dispersión de esfuerzos y garantizar la entrega académica en tiempo y forma, quedan explícitamente fuera del alcance P0:

1. **Gestión de Compras y Proveedores (P1):** No se implementarán órdenes de compra automáticas ni directorio de distribuidores mayoristas. La carga de stock en P0 se realiza por actualización manual de pañol.
2. **Matriz de Permisos Diferenciada (P1):** Todos los usuarios autenticados comparten permisos operativos homogéneos en el P0. La segregación formal entre Administrador, Recepcionista y Técnico se posterga.
3. **Cuenta Corriente de Clientes (P1):** Por regla de negocio del MVP, los equipos se cancelan al contado antes de ser retirados. No se gestionan líneas de crédito ni deudas a largo plazo.
4. **Integración con API Oficial de WhatsApp (P2):** La comunicación se resuelve mediante generación de textos listos para copiar, sin consumo de webhooks ni APIs de pago de Meta.
5. **Facturación Fiscal AFIP / ARCA (P2):** No se contempla emisión de comprobantes fiscales electrónicos vía web services de entes gubernamentales.
6. **Módulo de Analítica Avanzada e Inteligencia Artificial (P2):** No se integran modelos de lenguaje, procesamiento de embeddings ni paneles predictivos hasta contar con una base de datos operativa en producción.
