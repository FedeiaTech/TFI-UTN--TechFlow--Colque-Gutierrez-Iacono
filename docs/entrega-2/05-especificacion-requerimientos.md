# 05 — Especificación de Requerimientos del Sistema (SRS)

Estructurada bajo los lineamientos del estándar internacional **ISO/IEC/IEEE 29148:2018** (*Systems and software engineering — Requirements engineering*).

---

## 1. Requerimientos Funcionales (RF) — Núcleo P0

### 1.1. Módulo de Clientes (CLI)

#### RF-CLI-01: Alta de Cliente
- **Descripción:** El sistema debe permitir registrar un nuevo cliente ingresando nombre completo y número de teléfono.
- **Prioridad:** P0 (Obligatorio).
- **Regla asociada:** N/A.
- **Criterio de aceptación:**
  ```gherkin
  DADO un operador en el formulario de recepción
  CUANDO ingresa "María López" y teléfono "1122334455" y confirma
  ENTONCES el sistema persiste el cliente y devuelve su identificador único generado.
  ```

#### RF-CLI-02: Búsqueda y Selección de Cliente Existente
- **Descripción:** El sistema debe permitir localizar clientes existentes por coincidencia de nombre o teléfono para vincularlos a nuevas órdenes.
- **Prioridad:** P0 (Obligatorio).
- **Criterio de aceptación:**
  ```gherkin
  DADO un conjunto de clientes registrados
  CUANDO el operador ingresa al menos 3 caracteres en el buscador
  ENTONCES el sistema lista las coincidencias mostrando nombre, teléfono y cantidad de equipos previos.
  ```

---

### 1.2. Módulo de Equipos (EQ)

#### RF-EQ-01: Alta de Dispositivo Vinculado a Cliente
- **Descripción:** El sistema debe permitir dar de alta un equipo indicando cliente propietario, tipo genérico (`celular`, `notebook`, `consola`, `otro`), marca (opcional), modelo, número de serie genérico (opcional) e IMEI opcional.
- **Prioridad:** P0 (Obligatorio).
- **Regla asociada:** Estructura estable del equipo disociada de la orden.
- **Criterio de aceptación:**
  ```gherkin
  DADO un cliente seleccionado
  CUANDO se completan tipo="celular", marca="Apple", modelo="iPhone 12", imei="356987412589632"
  ENTONCES el equipo se registra y queda disponible para generar órdenes presentes y futuras.
  ```

#### RF-EQ-02: Restricción de Cero Almacenamiento de Credenciales
- **Descripción:** El sistema no debe poseer campos para ingresar ni almacenar contraseñas, PIN numérico ni secuencias de desbloqueo de los dispositivos.
- **Prioridad:** P0 (Obligatorio).
- **Regla asociada:** RN-05.
- **Criterio de aceptación:**
  ```gherkin
  DADO el esquema de datos y los formularios de la aplicación
  CUANDO se audita la estructura de la base de datos y los contratos de la API
  ENTONCES no existe ninguna columna ni campo DTO referente a PIN, password de equipo o patrón.
  ```

---

### 1.3. Módulo de Órdenes de Trabajo (ORD)

#### RF-ORD-01: Creación de Orden de Trabajo
- **Descripción:** El sistema debe permitir abrir una nueva orden de trabajo para un equipo, requiriendo obligatoriamente: técnico responsable (`tecnico_id`), falla reportada por el cliente y descripción del estado físico de ingreso visible. Opcionalmente debe admitir la lista de accesorios entregados.
- **Prioridad:** P0 (Obligatorio).
- **Regla asociada:** RN-10.
- **Criterio de aceptación:**
  ```gherkin
  DADO un equipo seleccionado y un usuario técnico autenticado
  CUANDO se envía la solicitud con estado_fisico="Rayones visibles en pantalla" y falla_reportada="No carga"
  ENTONCES se crea la orden con estado="recibido", resultado=NULL, fecha de creación automática y registro en historial.
  ```

#### RF-ORD-02: Máquina de Estados Global de la Orden
- **Descripción:** El sistema debe controlar las transiciones del estado global de la orden siguiendo estrictamente el flujo:
  $$\text{recibido} \longrightarrow \text{en\_proceso} \longrightarrow \text{listo} \longrightarrow \text{entregado}$$
  con la variante temporal `listo_no_retirado` para órdenes en `listo` con más de 30 días.
- **Prioridad:** P0 (Obligatorio).
- **Criterio de aceptación:**
  ```gherkin
  DADO una orden en estado "recibido"
  CUANDO se intenta transicionar directamente a "entregado" sin pasar por "listo"
  ENTONCES la API rechaza la petición con código HTTP 400 Bad Request.
  ```

#### RF-ORD-03: Asignación Obligatoria de Resultado al Quedar Lista
- **Descripción:** Toda orden que transicione al estado `listo` debe fijar obligatoriamente su campo `resultado` en uno de tres valores: `reparado`, `parcial` o `sin_reparacion`, y registrar `fecha_listo`.
- **Prioridad:** P0 (Obligatorio).
- **Regla asociada:** Restricción de integridad CHECK en base de datos.
- **Criterio de aceptación:**
  ```gherkin
  DADO una orden en "en_proceso" con todos sus trabajos concluidos
  CUANDO pasa a "listo"
  ENTONCES si el resultado no es provisto, la base de datos o el backend cancelan la operación arrojando violación de restricción.
  ```

#### RF-ORD-04: Bloqueo de Entrega con Saldo Pendiente
- **Descripción:** El backend debe rechazar cualquier intento de cambiar una orden a estado `entregado` si la vista `v_orden_saldo` indica un saldo estrictamente mayor a 0.
- **Prioridad:** P0 (Obligatorio).
- **Regla asociada:** RN-08.
- **Criterio de aceptación:**
  ```gherkin
  DADO una orden en estado "listo" con cotizaciones aprobadas por $10.000 y pagos registrados por $4.000 (saldo = $6.000)
  CUANDO el operador intenta cambiar el estado a "entregado"
  ENTONCES la operación se deniega con error 400 informando "No se puede entregar la orden con saldo pendiente ($6.000)".
  ```

#### RF-ORD-05: Cierre sin Reparación sin Exigencia de Pagos
- **Descripción:** Si una orden llega a estado `listo` con `resultado = 'sin_reparacion'` (debido a rechazo de presupuestos o inviabilidad técnica), y el total de cotizaciones aprobadas es $0, el sistema debe permitir la entrega inmediata sin exigir pagos.
- **Prioridad:** P0 (Obligatorio).
- **Regla asociada:** Cierre sin reparación (2.ª Devolución).
- **Criterio de aceptación:**
  ```gherkin
  DADO una orden con trabajos cancelados e irreparables y total aprobado = $0
  CUANDO se transiciona a "entregado"
  ENTONCES el sistema valida saldo = $0 y permite el cierre sin registrar pago.
  ```

---

### 1.4. Módulo de Trabajos Técnicos (TRAB)

#### RF-TRAB-01: Creación de Trabajos dentro de una Orden
- **Descripción:** El sistema debe permitir asociar uno o más trabajos técnicos a una misma orden, identificados por su descripción técnica y su estado inicial `pendiente_diagnostico`.
- **Prioridad:** P0 (Obligatorio).
- **Regla asociada:** RN-03.
- **Criterio de aceptación:**
  ```gherkin
  DADO una orden en estado "recibido" o "en_proceso"
  CUANDO el técnico agrega un trabajo "Reparación de placa de carga"
  ENTONCES el trabajo queda registrado bajo la orden con su propio identificador y estado técnico independiente.
  ```

#### RF-TRAB-02: Ciclo de Estados Técnicos del Trabajo
- **Descripción:** Cada trabajo debe transicionar de forma autónoma a través de los estados:
  `pendiente_diagnostico` $\rightarrow$ `diagnosticado` $\rightarrow$ `esperando_repuesto` $\rightarrow$ `en_reparacion` $\rightarrow$ `terminado` / `irreparable` / `cancelado`.
- **Prioridad:** P0 (Obligatorio).
- **Criterio de aceptación:**
  ```gherkin
  DADO una orden con Trabajo A y Trabajo B
  CUANDO Trabajo A pasa a "en_reparacion" y Trabajo B pasa a "esperando_repuesto"
  ENTONCES el sistema persiste ambos estados sin interferencia mutua.
  ```

---

### 1.5. Módulo de Cotizaciones y Cobros (COT / PAG)

#### RF-COT-01: Cotizaciones Independientes con Snapshot de Precios
- **Descripción:** Cada trabajo debe admitir la emisión de cotizaciones independientes numeradas secuencialmente (1, 2...). Cada ítem de cotización debe almacenar su descripción, cantidad ($>0$), tipo (`repuesto`, `mano_obra`, `descripcion`) y precio unitario snapshot ($\ge 0$).
- **Prioridad:** P0 (Obligatorio).
- **Regla asociada:** Reconstrucción de presupuestos (2.ª Devolución).
- **Criterio de aceptación:**
  ```gherkin
  DADO un repuesto cuyo precio de referencia en catálogo es $5.000
  CUANDO se incluye en una cotización con precio snapshot $5.000 y posteriormente el catálogo cambia a $7.000
  ENTONCES la cotización histórica mantiene su precio unitario en $5.000 inalterable.
  ```

#### RF-COT-02: Garantía de Única Cotización Vigente por Trabajo
- **Descripción:** Un trabajo solo puede tener una cotización en estado vigente (`pendiente` o `aprobada`) simultáneamente.
- **Prioridad:** P0 (Obligatorio).
- **Regla asociada:** Índice parcial único en base de datos.
- **Criterio de aceptación:**
  ```gherkin
  DADO un trabajo con Cotización 1 en estado "pendiente"
  CUANDO se intenta crear una Cotización 2 con estado "pendiente" para el mismo trabajo
  ENTONCES el sistema rechaza la creación por violación de restricción de unicidad.
  ```

#### RF-COT-03: Registro Inmutable de Decisiones y Motivos de Rechazo
- **Descripción:** El cliente puede aprobar o rechazar una cotización. En caso de rechazo, el sistema debe exigir un texto con el motivo de rechazo y mantener la cotización en el historial sin eliminarla.
- **Prioridad:** P0 (Obligatorio).
- **Regla asociada:** RN-01.
- **Criterio de aceptación:**
  ```gherkin
  DADO una cotización en estado "pendiente"
  CUANDO el operador registra su rechazo con motivo="Cliente considera costo excesivo"
  ENTONCES la cotización pasa a estado "rechazada", guarda motivo y fecha, y no es borrada del registro.
  ```

#### RF-PAG-01: Registro de Pagos Parciales con Monto Estrictamente Positivo
- **Descripción:** El sistema debe permitir asentar múltiples pagos sobre una misma orden. Cada pago debe registrar fecha, usuario receptor y un monto numérico mayor a cero.
- **Prioridad:** P0 (Obligatorio).
- **Regla asociada:** Observación de Oscar (CHECK monto > 0).
- **Criterio de aceptación:**
  ```gherkin
  DADO una orden en cualquier estado
  CUANDO se intenta registrar un pago con monto=0 o monto=-500
  ENTONCES el sistema rechaza el pago tanto en la validación Pydantic como en la base de datos.
  ```

---

### 1.6. Módulo de Stock y Pañol (REP)

#### RF-REP-01: Reserva en Pañol al Presupuestar
- **Descripción:** Al crear un ítem de cotización de tipo `repuesto`, el sistema debe generar automáticamente un registro de reserva en `repuesto_reservas` con estado `reservada` por la cantidad especificada.
- **Prioridad:** P0 (Obligatorio).
- **Regla asociada:** RN-02.
- **Criterio de aceptación:**
  ```gherkin
  DADO un repuesto con stock_total=5 y reservas_activas=1 (disponible=4)
  CUANDO se genera una cotización con 1 unidad de dicho repuesto
  ENTONCES la vista de disponibilidad pasa a reportar 3 unidades disponibles y stock_total permanece en 5.
  ```

#### RF-REP-02: Descuento Atómico y Cambio a Utilizada
- **Descripción:** Cuando el técnico confirma la utilización del repuesto tras la aprobación del cliente, el sistema debe ejecutar en la misma transacción la transición de la reserva a `utilizada` y el decremento correspondiente sobre `repuestos.stock_total`.
- **Prioridad:** P0 (Obligatorio).
- **Regla asociada:** Transaccionalidad de stock (2.ª Devolución).
- **Criterio de aceptación:**
  ```gherkin
  DADO una reserva en estado "reservada" con repuestos.stock_total=5
  CUANDO el técnico confirma el uso del repuesto
  ENTONCES en un único commit la reserva pasa a "utilizada" y repuestos.stock_total pasa a 4.
  ```

#### RF-REP-03: Liberación Inmediata de Reserva ante Rechazo
- **Descripción:** Cuando una cotización es rechazada o el trabajo es cancelado, todas las reservas vinculadas deben pasar al estado `liberada`, restaurando la disponibilidad neta del repuesto.
- **Prioridad:** P0 (Obligatorio).
- **Regla asociada:** RN-02.
- **Criterio de aceptación:**
  ```gherkin
  DADO una cotización rechazada con una reserva activa
  CUANDO se procesa el rechazo
  ENTONCES la reserva queda en "liberada" y la cantidad se reincorpora a la vista de stock disponible.
  ```

---

### 1.7. Comunicación Asistida (COM)

#### RF-COM-01: Generación y Copiado de Mensaje de Estado Preformateado
- **Descripción:** La interfaz debe proveer un botón de un clic que ensamble y copie al portapapeles un mensaje de texto formateado con el nombre del cliente, modelo del equipo, número de orden, estado actual, diagnóstico y cotización vigente.
- **Prioridad:** P0 (Obligatorio).
- **Regla asociada:** RN-09.
- **Criterio de aceptación:**
  ```gherkin
  DADO un operador visualizando la Orden #101 en estado "listo"
  CUANDO hace clic en el botón "Copiar Mensaje de Estado"
  ENTONCES el portapapeles del sistema operativo recibe el texto formateado listo para enviar por WhatsApp.
  ```

---

## 2. Requerimientos No Funcionales (RNF)

| Identificador | Categoría | Requisito Específico | Métrica / Criterio de Verificación |
|---|---|---|---|
| **RNF-SEG-01** | **Seguridad** | Autenticación stateless basada en tokens JWT con algoritmo HMAC-SHA256 y expiración temporal. | Ningún endpoint protegido accesible sin header `Authorization: Bearer <token>`. |
| **RNF-SEG-02** | **Seguridad** | Almacenamiento de contraseñas bajo hashing criptográfico seguro (Bcrypt/Argon2). | Nunca se almacena texto plano en la columna `usuarios.password_hash`. |
| **RNF-SEG-03** | **Seguridad** | Cero almacenamiento de contraseñas de dispositivos de clientes. | Inexistencia total de columnas para PIN/patrón en la base de datos. |
| **RNF-INT-01** | **Integridad** | Consistencia ACID mediante motor PostgreSQL: claves foráneas con restricción estricta y transacciones bloqueantes. | Errores en transacciones compuestas ejecutan rollback total sin dejar datos huérfanos. |
| **RNF-CON-01** | **Concurrencia** | Prevención de carreras en pañol mediante bloqueo pesimista de fila (`SELECT ... FOR UPDATE`) en repuestos. | Prueba de estrés: 2 reservas simultáneas para `stock = 1` resulta en exactamente 1 éxito y 1 rechazo. |
| **RNF-PERF-01** | **Rendimiento** | Tiempo de respuesta de endpoints de lectura y consulta de saldo inferior a 300 ms en condiciones normales de red. | Medición en benchmarks de testing automatizado de FastAPI. |
| **RNF-USAB-01** | **Usabilidad** | Diseño responsivo y contrastado (móvil y escritorio) optimizado para operadores de pañol y recepción. | Flujo de copiado de mensaje realizable en un único clic de mouse o toque de pantalla. |
| **RNF-PORT-01** | **Portabilidad** | Despliegue en la nube reproducible vía contenedores o servicios serverless estándar (Vercel, Render, Supabase). | El sistema se ejecuta de idéntica forma en entorno local y en los servidores cloud elegidos. |

---

## 3. Matriz de Trazabilidad de Requerimientos

| Problema Relevado | Regla de Negocio | Requerimiento Funcional | Módulo | Prueba de Verificación Obligatoria |
|---|---|---|---|---|
| P1 (Falta de trazabilidad) | RN-10 | RF-ORD-01, RF-TRAB-01 | Órdenes / Trabajos | Test de inserción en tablas de historial por cada cambio de estado |
| P2 (Consultas repetitivas WhatsApp) | RN-09 | RF-COM-01 | Comunicación | Test funcional de generación de plantilla de texto contextual |
| P3 (Presupuestos informales) | RN-01 | RF-COT-01, RF-COT-03 | Cotizaciones | Test de inmutabilidad de snapshot ante actualización de catálogo |
| P4 (Stock fantasma y descontrol) | RN-02 | RF-REP-01, RF-REP-02, RF-REP-03 | Repuestos | Test de reserva concurrente con `stock = 1` y uso atómico de repuesto |
| P5 (Equipos abandonados a 30 días) | RN-06 | RF-ORD-02 | Órdenes | Test de cálculo de vencimiento y registro de 2.º aviso |
| Desacople financiero vs técnico | RN-04, RN-08 | RF-ORD-04, RF-PAG-01 | Pagos / Órdenes | Test de bloqueo de paso a `entregado` con saldo pendiente |
