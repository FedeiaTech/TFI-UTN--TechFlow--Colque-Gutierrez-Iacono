# Caso completo de reparación

## 1. El taller (compuesto a partir de los 3 perfiles relevados)

**"TecnoRepair"** — taller de 2 personas (un técnico + una persona en mostrador que también
hace diagnóstico básico), reparación de celulares y notebooks, ubicado en un local a la
calle. Perfil intermedio entre el "comercio unipersonal con venta" y el "taller de 3-5
personas" ya relevados.

## 2. Caso end-to-end

**Día 1 — Ingreso.**
Un cliente, María, trae un iPhone 12 que no carga. En mostrador se registra:

- Datos del cliente (nombre, teléfono, si es primera vez o recurrente).
- Datos del equipo: modelo, IMEI, estado físico visible (foto del cliente saca dos rayones
  en la pantalla, se deja constancia), accesorios que deja (solo el equipo, sin cargador).
- Problema reportado por el cliente: "no carga, a veces prende si lo muevo el cable".
- **No se le pide el PIN** en este paso — el mostrador le explica que solo hará falta si el
  diagnóstico requiere probar software, y en ese caso se lo van a pedir puntualmente y no
  van a guardarlo.
- Se abre la orden en estado `Recibido`, se entrega un comprobante con número de orden.

**Día 1 (más tarde) — Diagnóstico.**
El técnico revisa el equipo: prueba con otro cable/cargador, descarta que sea la batería,
detecta que el conector de carga tiene un pin doblado/suciedad. Diagnóstico: **conector de
carga a reemplazar**. La orden pasa a `Diagnosticado`. Se registra el diagnóstico en la
orden (texto libre + repuesto sugerido).

**Día 1 — Presupuesto.**
Se genera el presupuesto v1: repuesto (conector de carga) + mano de obra, total $X. Se marca
el repuesto como **reservado** (no descontado de stock todavía, para no perderlo si el
presupuesto no se aprueba). La orden pasa a `Presupuestado`. Se contacta a María (llamado o
mensaje preparado con el estado, no WhatsApp API) para que apruebe.

**Día 2 — Aprobación con cambio.**
María aprueba el cambio de conector, pero al leer el presupuesto pregunta si también pueden
revisar por qué la pantalla "parpadea a veces" — algo que no había mencionado al ingresar.
Esto genera un **presupuesto adicional (v2)** ligado a la misma orden, no una orden nueva.
La orden queda en `Esperando aprobación adicional` para la parte nueva mientras el trabajo
aprobado (conector) puede seguir. El presupuesto v1 no se borra ni se sobreescribe: queda en
el historial de la orden.

**Día 2 — Repuesto sin stock.**
El conector de carga está en stock, pero el repuesto necesario para el diagnóstico de
pantalla (un flex) no está. La orden pasa a `Esperando repuesto` para esa parte. Se pide al
proveedor (esto queda fuera del P0 como proceso de compra formal, pero el estado sí importa
para que el cliente sepa por qué se demora).

**Día 3 — En reparación.**
Llega el flex. El técnico confirma que va a usarlo: **recién en este momento se descuenta
del stock** (no cuando se cotizó). Se repara el conector de carga y se reemplaza el flex de
pantalla. Orden en estado `En reparación`.

**Día 3 — Falla nueva no relacionada.**
Al hacer la prueba final, aparece un problema distinto: el altavoz suena bajo. No estaba en
el diagnóstico original ni en el pedido de María. Se genera un tercer presupuesto (v3), se
notifica a María, y **la orden no se retiene por esto**: el trabajo ya aprobado (conector +
pantalla) sigue su curso hacia `Listo`, y el altavoz queda como un ítem pendiente aparte
dentro de la misma orden, a la espera de que María decida.

**Día 3 — Listo, decisión del cliente sobre el altavoz.**
María dice que por ahora no quiere arreglar el altavoz. Ese ítem se marca `Rechazado` dentro
de la orden (con motivo: "cliente no autoriza por costo"), sin afectar el resto. La orden
pasa a `Listo` para los ítems aprobados.

**Estado financiero (independiente del estado técnico).**
La orden llegó a `Listo` con estado de pago `Pendiente`. María paga el total en el momento
del retiro: estado de pago pasa a `Pagado`. **Regla del taller:** TecnoRepair **no entrega
equipos con saldo pendiente** — paga todo o no se lleva el equipo. Por eso el P0 no necesita
cuenta corriente: alcanza con `total`, `pagos registrados` (por si paga en dos partes el
mismo día) y `saldo pendiente` calculado.

**Día 3 — Entrega.**
Orden pasa a `Entregado`. Fin del ciclo para este caso.

## 3. Caso alternativo — equipo no retirado (para la regla del punto 3)

Variante corta, mismo taller: un cliente deja una notebook, se repara, queda `Listo`, se lo
notifica, y **no vuelve a buscarla**. Regla adoptada:

- A los 30 días sin retiro tras la notificación, la orden pasa a `Listo - No retirado` con
  alerta visible para el mostrador.
- El taller vuelve a notificar por escrito (mensaje preparado, mismo mecanismo que para
  presupuestos) dejando constancia de la fecha del segundo aviso.
- No se define en el P0 ninguna acción automática de disposición/venta del equipo — eso es
  una decisión legal/comercial que excede el alcance técnico de esta entrega.

## 4. Reglas de negocio que salen de este caso (nunca deberían violarse)

1. Un presupuesto rechazado o reemplazado **nunca se borra**: queda en el historial de la
   orden, versionado (v1, v2…).
2. Un repuesto se marca `reservado` al presupuestarlo y **solo se descuenta del stock**
   cuando el técnico confirma que lo usó. Si el ítem se rechaza, el repuesto vuelve a estar
   disponible.
3. Una falla nueva detectada durante la reparación **no bloquea** los ítems ya aprobados de
   la misma orden; genera un ítem/presupuesto adicional independiente dentro de la misma
   orden.
4. Estado técnico (`Recibido → … → Entregado`) y estado de pago (`Pendiente / Parcial /
   Pagado`) son **dos campos separados**, nunca un solo estado combinado.
5. No se solicita ni se almacena PIN/contraseña del equipo salvo que el diagnóstico lo
   requiera puntualmente, y en ese caso no queda persistido en la base.
6. Un equipo `Listo` sin retirar pasa a un estado de alerta a los 30 días, con un segundo
   aviso documentado — sin acción automática de disposición en el P0.
7. Ningún cálculo de este flujo se llama "rentabilidad neta": lo que se calcula es margen
   por reparación (cobrado − repuestos − mano de obra).
