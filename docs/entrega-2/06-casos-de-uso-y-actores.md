# 06 — Casos de Uso y Actores del Sistema

## 1. Caracterización de Actores

En la etapa de alcance P0, el sistema interactúa con tres actores clave:

1. **Operador / Técnico (Actor Primario):**
   - Usuario autenticado en el sistema. Representa al personal del taller que recepciona dispositivos, efectúa inspecciones técnicas, genera cotizaciones, registra pagos y entrega los equipos.
   - Cuenta con identidad única (`usuarios.id`), lo que garantiza la trazabilidad de cada acción operativa.
2. **Cliente (Actor Externo / Indirecto):**
   - Persona que solicita la reparación de su dispositivo. No interactúa directamente con la base de datos en P0 (no posee credenciales de acceso web), sino que se comunica mediante el canal mostrador o mensajería con el Operador.
3. **Sistema / Tarea Temporal (Actor Secundario Automatizado):**
   - Componente interno de software encargado de verificar plazos temporales (órdenes en estado `listo` cuya `fecha_listo` supere los 30 días) para disparar alertas de abandono.

---

## 2. Diagrama de Casos de Uso del Núcleo P0

El modelo formal de casos de uso se encuentra implementado en sintaxis PlantUML en [`diagramas/casos_de_uso/casos_de_uso.puml`](diagramas/casos_de_uso/casos_de_uso.puml).

---

## 3. Especificación Formal de Casos de Uso Clave

### CU-01: Recepción de Dispositivo y Apertura de Orden
- **Actor principal:** Operador / Técnico.
- **Precondiciones:** El operador debe haber iniciado sesión en TechFlow.
- **Flujo Principal:**
  1. El operador accede a la vista de nueva orden.
  2. Busca al cliente por nombre o teléfono. Si no existe, ingresa nombre y teléfono para su alta inmediata.
  3. Selecciona el equipo del cliente o da de alta un nuevo dispositivo ingresando tipo (`celular`, `notebook`, `consola`), marca, modelo, y opcionalmente número de serie o IMEI.
  4. Registra obligatoriamente la falla reportada por el cliente y el estado físico visible de ingreso (detallando marcas o roturas previas). Opcionalmente asienta accesorios entregados.
  5. El sistema asigna al operador como técnico responsable (`tecnico_id`), persiste la orden con estado global `recibido`, genera el identificador numérico de orden e inserta el evento en `historial_estados_orden`.
  6. El sistema ofrece el botón *"Copiar Comprobante de Recepción"*.
- **Postcondiciones:** La orden queda creada en estado `recibido` con constancia inmutable en la base de datos.
- **Flujos Alternativos:**
  - *3a. El cliente trae un equipo previamente registrado:* El operador lo selecciona del listado sin duplicar datos técnicos del aparato.

---

### CU-02: Diagnóstico y Creación de Trabajo
- **Actor principal:** Técnico.
- **Precondiciones:** La orden debe estar en estado `recibido` o `en_proceso`.
- **Flujo Principal:**
  1. El técnico inspecciona el dispositivo en banco y determina la causa de la falla.
  2. Accede a la orden y selecciona *"Agregar Trabajo"*.
  3. Ingresa la descripción de la falla/tarea y el detalle del diagnóstico técnico.
  4. El sistema crea el trabajo en estado `diagnosticado`, transiciona la orden global a `en_proceso` (si estaba en `recibido`) y registra la trazabilidad en `historial_estados_trabajo`.
- **Postcondiciones:** El trabajo queda disponible para ser cotizado de forma independiente.
- **Flujos Alternativos:**
  - *2a. Falla nueva detectada en etapa posterior:* El técnico repite el CU-02 para registrar un trabajo adicional sin alterar el avance de los trabajos previos de la misma orden.

---

### CU-03: Emisión de Cotización y Reserva de Repuesto
- **Actor principal:** Técnico.
- **Precondiciones:** El trabajo debe encontrarse en estado `diagnosticado`. No debe existir otra cotización vigente (`pendiente` o `aprobada`) para ese mismo trabajo.
- **Flujo Principal:**
  1. El técnico selecciona el trabajo e inicia una nueva cotización.
  2. Agrega uno o más ítems indicando: tipo (`repuesto`, `mano_obra`, `descripcion`), detalle, cantidad y precio unitario snapshot.
  3. Si el ítem es de tipo `repuesto`:
     - El sistema realiza un bloqueo de fila pesimista (`SELECT ... FOR UPDATE`) sobre la tabla de repuestos.
     - Verifica la disponibilidad neta (`v_repuesto_disponibilidad`). Si hay stock disponible suficiente, crea la reserva en `repuesto_reservas` con estado `reservada`.
  4. El sistema asigna número secuencial a la cotización, fija su estado en `pendiente` y persiste los ítems.
  5. El sistema calcula dinámicamente el importe total mediante la vista `v_cotizacion_totales`.
- **Postcondiciones:** La cotización queda en estado `pendiente`. Los repuestos cotizados quedan reservados, disminuyendo la disponibilidad neta en pañol pero sin alterar `repuestos.stock_total`.
- **Flujos de Excepción:**
  - *3a. Stock insuficiente:* Si el repuesto no cuenta con unidades disponibles en pañol, el sistema avisa al técnico. El técnico puede optar por guardar el trabajo en estado `esperando_repuesto` sin generar la reserva hasta que ingrese mercadería.

---

### CU-04: Registrar Decisión del Cliente (Aprobación / Rechazo)
- **Actor principal:** Operador / Técnico.
- **Precondiciones:** La cotización debe estar en estado `pendiente`.
- **Flujo Principal (Aprobación):**
  1. El operador recibe la conformidad del cliente y selecciona *"Aprobar Cotización"*.
  2. El sistema actualiza la cotización a `aprobada` y transiciona el trabajo a `en_reparacion`.
  3. Registra el cambio en el historial.
- **Flujo Alternativo (Rechazo del Cliente):**
  1. El operador recibe la negativa del cliente y selecciona *"Rechazar Cotización"*.
  2. El sistema exige ingresar obligatoriamente el `motivo_rechazo`.
  3. En la misma transacción:
     - La cotización pasa a estado `rechazada`.
     - Todas las reservas asociadas a los ítems de repuesto pasan de `reservada` a `liberada`, restituyendo de inmediato la disponibilidad del stock.
     - El trabajo técnico pasa al estado `cancelado`.
- **Postcondiciones:** Las cotizaciones aprobadas quedan computables para el saldo de la orden. Las reservas rechazadas quedan libres para otras órdenes.

---

### CU-05: Confirmar Uso Atómico de Repuesto y Terminar Trabajo
- **Actor principal:** Técnico.
- **Precondiciones:** El trabajo debe estar `en_reparacion` y contar con una cotización `aprobada`.
- **Flujo Principal:**
  1. El técnico concluye la intervención física en banco y pulsa *"Confirmar Reparación y Uso de Piezas"*.
  2. El sistema ejecuta una transacción atómica estricta:
     - Actualiza el estado de las reservas de `reservada` a `utilizada`.
     - Decrementa el contador físico `repuestos.stock_total` en la cantidad consumida.
     - Cambia el estado técnico del trabajo a `terminado`.
  3. El sistema evalúa el estado de todos los trabajos de la orden. Si la totalidad de los trabajos ha alcanzado un estado terminal (`terminado`, `irreparable` o `cancelado`), transiciona la orden a `listo` y fija el campo `resultado`:
     - `reparado`: si todos los trabajos culminaron con éxito.
     - `parcial`: si al menos un trabajo fue reparado y otro cancelado/irreparable.
     - `sin_reparacion`: si ningún trabajo culminó en reparación.
- **Postcondiciones:** El inventario físico se actualiza definitivamente y la orden queda en condiciones de ser retirada.

---

### CU-06: Registrar Pago de Orden
- **Actor principal:** Operador / Cajero.
- **Precondiciones:** La orden debe tener al menos una cotización aprobada o encontrarse en proceso.
- **Flujo Principal:**
  1. El cliente entrega dinero en concepto de seña o liquidación total.
  2. El operador accede a la orden y selecciona *"Registrar Pago"*.
  3. Ingresa el monto (restringido a valor $> 0$).
  4. El sistema inserta el registro en la tabla `pagos` vinculando la orden y el usuario receptor.
  5. La vista `v_orden_saldo` actualiza automáticamente el acumulado de pagos, el saldo deudor remanente y el `estado_pago` derivado (`pendiente`, `parcial` o `pagado`).
- **Postcondiciones:** El saldo de la orden disminuye por el monto exacto ingresado.

---

### CU-07: Entrega de Equipo (Validación de Saldo Cero)
- **Actor principal:** Operador.
- **Precondiciones:** La orden debe estar en estado `listo` o `listo_no_retirado`.
- **Flujo Principal:**
  1. El cliente se presenta en mostrador a retirar el equipo.
  2. El operador selecciona *"Entregar Dispositivo"*.
  3. El sistema consulta `v_orden_saldo`:
     - Si `saldo == 0`, autoriza la transición: la orden pasa al estado terminal `entregado`, se registra la fecha y se cierra el ciclo.
     - Si `saldo > 0`, deniega la operación impidiendo el cambio de estado e indica el monto adeudado. El operador debe ejecutar previamente el CU-06 (Registrar Pago) antes de poder concretar la entrega.
- **Postcondiciones:** La orden queda definitivamente cerrada en estado `entregado`.

---

### CU-08: Copiar Mensaje de Estado (WhatsApp Asistido)
- **Actor principal:** Operador / Técnico.
- **Precondiciones:** La orden debe existir en el sistema.
- **Flujo Principal:**
  1. Desde la ficha de la orden, el operador hace clic en *"Copiar Mensaje de Estado"*.
  2. El sistema extrae los datos actuales: nombre del cliente, modelo del equipo, estado global, resumen de trabajos y saldo pendiente.
  3. Ensambla una plantilla clara y profesional de texto plano y la copia automáticamente al portapapeles del dispositivo.
  4. El operador abre su aplicación de mensajería (WhatsApp Web / Desktop), pega el contenido en la conversación del cliente y lo envía.
- **Postcondiciones:** El cliente recibe información precisa sin que el operador deba tipear el mensaje manualmente ni contratar servicios de APIs pagas.
