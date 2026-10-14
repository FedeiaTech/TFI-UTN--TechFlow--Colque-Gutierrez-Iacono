# 04 — Caso Completo de Reparación y Reglas de Negocio

## 1. Fuente del Caso y Criterio Metodológico de Origen

En cumplimiento estricto de las observaciones metodológicas formuladas por el tutor Oscar Londero en su 2.ª Devolución:
- Se toma como **caso de referencia un taller real específico**, correspondiente al **Perfil A (Técnico Autoempleado)** relevado en la investigación de campo ([Anexo A](anexos/A-respuestas-encuesta.md)), anonimizado para preservar la confidencialidad comercial.
- Se diferencia categóricamente el origen de cada regla para no atribuir a la observación empírica decisiones adoptadas internamente por el grupo para el diseño del software.

```text
┌───────────────────────────────┬────────────────────────────────────────────────────────────┐
│ ORIGEN                        │ SIGNIFICADO                                                │
├───────────────────────────────┼────────────────────────────────────────────────────────────┤
│ [RELEVADA]                    │ Surge directamente de lo manifestado por el negocio real.  │
│ [DECISIÓN DEL GRUPO]          │ Decisión adoptada para el MVP; no validada empíricamente.  │
│ [A CONFIRMAR]                 │ Hipótesis pendiente de validación formal en campo.         │
└───────────────────────────────┴────────────────────────────────────────────────────────────┘
```

---

## 2. Caso Base: Técnico Autoempleado (Flujo Lineal)

El caso representa la dinámica habitual de un microtaller donde una única persona gestiona la atención al público, el diagnóstico técnico, la elaboración de cotizaciones y la ejecución de la reparación.

### 2.1. Secuencia Operativa Paso a Paso

1. **Ingreso y Recepción:**
   - La clienta (María) se presenta en el local con un teléfono celular iPhone 12 que no enciende con normalidad y manifiesta: *"No carga, a veces prende si muevo el cable"*.
   - El operador abre el sistema y registra a la clienta (nombre y teléfono) y los datos estables del equipo (tipo: celular, marca: Apple, modelo: iPhone 12, número de serie / IMEI).
   - El sistema solicita obligatoriamente el **estado físico visible en ese ingreso** (*"Pantalla con dos micro-rayones en zona superior, tapa trasera sin daños"*) y los **accesorios entregados** (*"Solo equipo, sin cable ni cargador"*).
   - **Privacidad:** No se solicita ni se almacena PIN ni patrón de desbloqueo `[DECISIÓN DEL GRUPO]`.
   - Se crea la **Orden de Trabajo #101** con estado global `recibido`, asignando al usuario autenticado como `tecnico_id` responsable. El sistema emite el número de orden y genera un texto preformateado que el técnico copia con un botón para enviar por chat.

2. **Diagnóstico Técnico y Creación de Trabajo:**
   - El técnico traslada el equipo al banco de trabajo. Conecta amperímetro USB, realiza mediciones de consumo, descarta batería agotada y visualiza con microscopio un pin quebrado en el puerto Lightning.
   - En el sistema, la orden pasa al estado global `en_proceso` y se registra el **Trabajo #1**:
     - *Descripción:* "Reemplazo de módulo de conector de carga (pin USB)".
     - *Diagnóstico:* "Pin interno número 4 quebrado. Requiere cambio de flex de carga".
     - *Estado técnico del trabajo:* `diagnosticado`.

3. **Cotización y Reserva de Repuesto:**
   - Para el Trabajo #1 se emite la **Cotización #1**:
     - Ítem 1 (Repuesto): Conector Lightning iPhone 12 — Cantidad: 1 — Precio Unitario Snapshot: $5.000.
     - Ítem 2 (Mano de obra): Desarme, micro-soldadura y armado — Cantidad: 1 — Precio Unitario: $3.000.
   - Total de la cotización: $8.000 (calculado automáticamente por la vista `v_cotizacion_totales`).
   - **Gestión de Pañol:** En el momento de guardar la cotización con estado `pendiente`, el sistema crea una entrada en `repuesto_reservas` con estado `reservada`. El repuesto **no se descuenta del stock total todavía**, pero queda bloqueado para que ninguna otra orden pueda tomarlo `[DECISIÓN DEL GRUPO]`.
   - El técnico pulsa el botón *"Copiar Mensaje de Estado"*, obteniendo en el portapapeles:
     > *"Hola María, revisamos tu iPhone 12 (Orden #101). Diagnóstico: pin de carga dañado. Presupuesto: $8.000 ($5.000 repuesto + $3.000 mano de obra). ¿Confirmás la reparación? TechFlow Taller."*
   - Pega el texto en su aplicación de mensajería y lo despacha.

4. **Aprobación y Ejecución de la Reparación:**
   - María responde afirmativamente.
   - El técnico marca en el sistema la Cotización #1 como `aprobada`. El Trabajo #1 cambia su estado técnico a `en_reparacion`.
   - El técnico toma la pieza del pañol y realiza la intervención física.
   - Concluida la tarea, en una **única transacción atómica de base de datos** `[DECISIÓN DEL GRUPO]`:
     1. La reserva pasa de `reservada` a `utilizada`.
     2. El campo `stock_total` del repuesto se decrementa en 1 unidad.
     3. El Trabajo #1 pasa al estado técnico `terminado`.

5. **Transición a Listo para Retirar:**
   - Al estar todos los trabajos de la orden en estado terminal (`terminado`), el sistema transiciona automáticamente la Orden #101 a:
     - `estado`: `listo`
     - `resultado`: `reparado`
     - `fecha_listo`: timestamp actual.
   - El técnico pulsa *"Copiar Mensaje: Equipo Listo"* y notifica a María que su equipo está probado y listo para entrega.

6. **Cobro y Entrega Física:**
   - María acude al taller a retirar el celular.
   - El técnico abre la orden e intenta marcarla directamente como `entregado`.
   - **Regla inquebrantable:** El backend consulta `v_orden_saldo`, constata que el total aprobado es $8.000, los pagos registrados son $0 y el saldo deudor es $8.000 ($> 0$), **rechazando la transición y arrojando error** `[DECISIÓN DEL GRUPO - A CONFIRMAR]`.
   - El técnico registra un pago por $8.000 en efectivo (indicando el usuario receptor). La vista recalcula automáticamente `saldo = $0` y `estado_pago = 'pagado'`.
   - El sistema habilita la transición: la Orden #101 pasa a `entregado`. Se registra la salida en el historial y concluye el ciclo.

### 2.2. Diagrama de Secuencia del Caso Base
El diagrama formal en sintaxis PlantUML se encuentra versionado en [`diagramas/secuencia/caso_base_secuencia.puml`](diagramas/secuencia/caso_base_secuencia.puml).

---

## 3. Variantes Operativas del Caso Real

### 3.1. Variante A: Cierre sin Reparación (Rechazo de Presupuesto o Equipo Irreparable)
Resuelve la inquietud formulada en la 2.ª Devolución docente: *¿Cómo cierra la orden si no hay trabajo técnico?*

- **Escenario 1 (Rechazo del Cliente):** El cliente considera que el presupuesto es elevado y decide no reparar.
  1. El técnico registra la Cotización #1 como `rechazada`, asentando obligatoriamente el motivo (*"Presupuesto elevado"*).
  2. En esa misma operación, el sistema pasa la reserva del repuesto a `liberada`, devolviendo inmediatamente la unidad a la disponibilidad neta del pañol.
  3. El Trabajo #1 pasa al estado técnico `cancelado`.
  4. Como no existen otros trabajos pendientes, la Orden pasa a estado global `listo` con resultado `sin_reparacion`.
  5. Dado que el total de cotizaciones aprobadas es $0, el saldo deudor es $0.
  6. Cuando el cliente acude a retirar su dispositivo sin reparar, el sistema permite transicionar directamente a `entregado` sin exigir cobro.
- **Escenario 2 (Falla Irreparable):** Durante el examen se constata fisura en placa base no subsanable.
  1. El Trabajo pasa a `irreparable`.
  2. La Orden pasa a `listo` con resultado `sin_reparacion` y se entrega al cliente bajo el mismo procedimiento.

### 3.2. Variante B: Tratamiento de Equipos Abandonados (Plazo de 30 Días)
Atiende el dolor relevado en campo respecto de aparatos que quedan inmovilizados en estanterías por meses:

1. **Disparador:** La orden se encuentra en estado `listo` y han transcurrido 30 días corridos desde `fecha_listo` sin que el cliente haya retirado el equipo.
2. **Cambio de Estado:** La orden transiciona a `listo_no_retirado` y genera una alerta visual prominente en la interfaz del sistema.
3. **Segundo Aviso Documentado:** El operador emite un segundo mensaje formal de intimación y pulsa el botón para asentar `fecha_segundo_aviso_no_retirado` en el registro de la orden.
4. **Límite Legal:** El sistema no ejecuta disposición automática ni enajenación del bien, dejando constancia documental fehaciente para resguardo del taller.

---

## 4. Matriz de Reglas de Negocio Derivadas del Caso

| # | Regla de Negocio | Origen Metodológico | Justificación y Mecanismo de Control |
|---|---|---|---|
| **RN-01** | **Preservación Inmutable de Cotizaciones:** Una cotización rechazada o reemplazada nunca se elimina físicamente de la base de datos; permanece en el historial del trabajo con su motivo y fechas. | [DECISIÓN DEL GRUPO] | Garantiza auditoría y trazabilidad histórica frente a reclamos posteriores del cliente. |
| **RN-02** | **Ciclo de Reservas en Dos Fases:** Un repuesto se marca `reservada` al cotizar y únicamente se descuenta de `stock_total` cuando el técnico confirma su uso efectivo. Al rechazar o cancelar, pasa a `liberada`. | [DECISIÓN DEL GRUPO] | Evita el "stock fantasma" y quiebres de inventario durante el lapso de espera de respuesta del cliente. |
| **RN-03** | **Independencia de Trabajos en Falla Adicional:** Un nuevo hallazgo detectado durante la reparación no frena ni altera los trabajos ya aprobados; origina un trabajo independiente con cotización propia. | [DECISIÓN DEL GRUPO] (Validada con Escenario Sintético) | Resuelve la limitación de modelos monolíticos: permite que tareas sencillas avancen sin quedar bloqueadas por repuestos demorados. |
| **RN-04** | **Disociación Técnica vs. Financiera:** El estado técnico de la orden/trabajos y el estado de cobro son campos separados. `estado_pago` nunca es editable a mano: se deriva de los saldos. | [DECISIÓN DEL GRUPO] | Impide inconsistencias contables donde un operador marca una orden como "pagada" sin respaldo de registros en la tabla de pagos. |
| **RN-05** | **Política de Cero Persistencia de Credenciales:** El sistema no cuenta con campos para almacenar PIN, clave alfanumérica ni patrón gráfico de desbloqueo de los dispositivos. | [DECISIÓN DEL GRUPO] | Protección de datos sensibles del cliente y mitigación de responsabilidad penal/civil del taller ante filtraciones. |
| **RN-06** | **Gestión de Abandono con Doble Constancia:** Todo equipo en `listo` sin retirar transiciona a alerta a los 30 días, exigiendo el registro formal de un segundo aviso con fecha. | Problema [RELEVADA]; plazo y flujo [DECISIÓN DEL GRUPO] | Brinda respaldo administrativo ante litigios por custodia prolongada de bienes ajenos. |
| **RN-07** | **Terminología Económica Rigurosa:** El sistema prohíbe el término "rentabilidad neta", empleando exclusivamente "margen directo por reparación" (ingresos menos repuestos aplicados). | [DECISIÓN DEL GRUPO] | Precisión técnica solicitada por la cátedra: no se contemplan costos indirectos fijos en el MVP. |
| **RN-08** | **Bloqueo de Entrega con Saldo Deudor:** Una orden de trabajo no puede cambiar a estado `entregado` si `v_orden_saldo.saldo > 0`. | [DECISIÓN DEL GRUPO] - [A CONFIRMAR en taller] | Garantiza la política comercial estándar de cobrar antes de liberar la custodia del dispositivo. |
| **RN-09** | **Comunicación Asistida Asíncrona:** El sistema provee botones contextuales que generan plantillas de texto formateadas listas para copiar y pegar en canales externos de chat. | [RELEVADA] (Dolor por WhatsApp manual) | Reduce drásticamente las 1.5–2 horas diarias que los técnicos dedican a redactar mensajes repetitivos. |
| **RN-10** | **Identidad y Trazabilidad Obligatoria:** Cada orden tiene asignado un técnico responsable (`tecnico_id`) y cada cambio de estado queda registrado en un historial con el usuario autor. | [DECISIÓN DEL GRUPO] | Responde al señalamiento docente de saber siempre quién atiende y quién autoriza cada etapa. |

---

## 5. Escenario Sintético para Pruebas de Estrés ("TecnoRepair")

> [!WARNING]
> **Naturaleza del escenario:** Este escenario es una construcción artificial creada por el equipo para someter el modelo relacional y la API a condiciones de máxima exigencia (múltiples trabajos simultáneos, esperas asíncronas de repuestos y rechazos parciales). **No representa a un taller real**, sino que oficia de banco de pruebas de software.

### 5.1. Narrativa del Escenario
- **Día 1:** María ingresa un iPhone 12 que no carga. Se abre la Orden #201 en estado global `recibido`. El técnico diagnostica falla en pin de carga y crea el **Trabajo 1** (Conector) con la **Cotización 1** por $8.000. El repuesto conector queda en estado `reservada`. María aprueba la cotización: el Trabajo 1 pasa a `en_reparacion`.
- **Día 2:** Mientras el conector está siendo reparado, María contacta al taller solicitando que revisen la pantalla porque presenta un parpadeo intermitente.
  - El técnico agrega a la misma orden el **Trabajo 2** (Pantalla).
  - Emite la **Cotización 2** por $35.000 (requiere flex de pantalla). María aprueba la cotización.
  - Al revisar pañol, no hay flex en existencia: el Trabajo 2 transiciona al estado técnico `esperando_repuesto`.
  - **Estado del sistema en este instante:**
    - Orden #201: estado global `en_proceso`.
    - Trabajo 1: estado técnico `en_reparacion`.
    - Trabajo 2: estado técnico `esperando_repuesto`.
    *(Demostración de que la estructura soporta estados concurrentes disímiles dentro de la misma orden sin forzar estados globales ambiguos).*
- **Día 3:** Llega el flex a taller. El técnico confirma el uso del repuesto (descuento atómico) y concluye tanto el Trabajo 1 como el Trabajo 2 (ambos pasan a `terminado`).
  - Durante las pruebas funcionales finales antes del cierre, el técnico advierte que el altavoz suena con distorsión grave.
  - Crea el **Trabajo 3** (Altavoz) con la **Cotización 3** por $12.000 (el repuesto altavoz queda `reservada`).
  - Se notifica a María. La clienta responde que no dispone de presupuesto adicional y prefiere no reparar el altavoz.
  - El técnico asienta el **Rechazo de la Cotización 3** por "Costo elevado".
  - **Consecuencias automáticas:**
    - La reserva del repuesto altavoz pasa a `liberada` (vuelve a stock disponible).
    - El Trabajo 3 pasa a estado técnico `cancelado`.
- **Cierre y Liquidación:**
  - Trabajos: Trabajo 1 (`terminado`), Trabajo 2 (`terminado`), Trabajo 3 (`cancelado`).
  - Dado que todos los trabajos están en estado terminal, la Orden #201 pasa a:
    - `estado`: `listo`
    - `resultado`: `parcial` (se repararon conector y pantalla, no altavoz).
  - Cálculo de saldos en `v_orden_saldo`:
    - Total aprobado: $8.000 + $35.000 = $43.000 (la cotización rechazada de $12.000 no se computa).
    - Pagos registrados: $0.
    - Saldo a cobrar: $43.000.
  - María abona los $43.000 en el local. Se registra el pago, el saldo queda en $0 y la orden se entrega con éxito.

El diagrama formal de secuencia de este escenario sintético se encuentra en [`diagramas/secuencia/escenario_sintetico_secuencia.puml`](diagramas/secuencia/escenario_sintetico_secuencia.puml).
