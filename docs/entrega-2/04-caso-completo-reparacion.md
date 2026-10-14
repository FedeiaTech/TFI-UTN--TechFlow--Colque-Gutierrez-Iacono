# Caso completo de reparación

## 1. Fuente del caso y criterio de origen

**Perfil base: técnico autoempleado** (trabaja solo, sin venta de accesorios). Es uno de los tres
perfiles identificados en el relevamiento de campo (encuesta y entrevistas), descrito en
[`docs/entrega-1`](../entrega-1/TRABAJO-FINAL-INTEGRADOR-unificado.md). Los negocios relevados
se mantienen anonimizados.

Lo que el relevamiento respalda de este perfil es acotado:

- Pierde tiempo respondiendo consultas de estado por WhatsApp ("¿ya está?", "¿cuánto falta?").
- Tiene problemas con el manejo de equipos abandonados.

Todo lo demás de este documento (secuencia de pasos, plazos, políticas de cobro y de stock) es
una **reconstrucción del grupo** sobre ese perfil, no un dato observado. Para no confundir ambas
cosas, cada regla de la sección 4 indica su origen con esta leyenda:

| Origen | Significado |
|---|---|
| **Relevada** | Surge de lo que dijeron los negocios relevados. |
| **Decisión del grupo** | La adoptamos para el MVP; no fue validada por un taller real. |
| **A confirmar** | Hay que consultarla con un negocio real antes de darla por válida. |

## 2. Caso base — técnico autoempleado

Caso lineal: una sola persona atiende mostrador, diagnostica y repara.

**Ingreso.** Un cliente, María, trae un iPhone 12 que no carga. Se registra el cliente, el equipo
(modelo, IMEI), el estado físico visible (dos rayones en pantalla), los accesorios que deja (solo
el equipo, sin cargador) y la falla reportada: "no carga, a veces prende si lo muevo el cable".
No se pide el PIN. Se abre la orden en `Recibido`, a cargo de un técnico responsable, y se entrega un comprobante con
el número. El estado físico y los accesorios quedan en la orden (cambian en cada ingreso); el
equipo guarda solo sus datos estables.

**Diagnóstico.** El técnico descarta batería y detecta el conector de carga con un pin doblado.
Diagnóstico: conector de carga a reemplazar. Se registra como un trabajo de la orden, que pasa a
`En proceso`; el trabajo queda `Diagnosticado`.

**Cotización.** Se genera la cotización del trabajo con repuesto y mano de obra (con el precio
aplicado en cada ítem). El repuesto queda **reservado** (no se descuenta del stock) y la cotización
queda pendiente de respuesta. Se avisa a María con un mensaje preparado de estado, que el técnico
copia con un botón (sin integración con la API de WhatsApp).

**Aprobación y reparación.** María aprueba la cotización. El técnico confirma el uso del repuesto:
recién ahí se descuenta del stock. El trabajo pasa por `En reparación` y luego `Terminado`.

**Listo, cobro y entrega.** Con todos los trabajos terminados, la orden pasa a `Listo` con resultado
`Reparado`. Se avisa a María. Cuando retira, paga el total aprobado (en una o más partes), el saldo
pendiente queda en cero y la orden pasa a `Entregado`.

**Variante sin reparación.** Si el cliente rechaza todas las cotizaciones o el equipo resulta
irreparable, la orden pasa a `Listo` con resultado `Sin reparación` y luego a `Entregado`, sin pasar
por estados de reparación.

## 3. Variante — equipo no retirado

Una notebook queda `Listo`, se avisa al cliente y no vuelve a buscarla.

- A los 30 días sin retiro tras el aviso, la orden pasa a `Listo - No retirado` con alerta visible.
- Se vuelve a notificar por escrito (mismo mensaje preparado) y se deja constancia de la fecha del
  segundo aviso.
- No se define ninguna disposición automática del equipo (decisión legal y comercial fuera del P0).

El problema de fondo (equipos abandonados) es **Relevado**; el plazo de 30 días y el segundo aviso
son **Decisión del grupo** (ver sección 4).

## 4. Reglas de negocio que salen del caso

| # | Regla | Origen |
|---|---|---|
| 1 | Una cotización rechazada o reemplazada **nunca se borra**: queda en el historial del trabajo. | Decisión del grupo |
| 2 | Un repuesto se marca `reservado` al cotizarlo y **solo se descuenta del stock** cuando el técnico confirma que lo usó. Si se rechaza la cotización, la reserva se libera y vuelve a estar disponible. | Decisión del grupo |
| 3 | Una falla nueva detectada durante la reparación **no bloquea** lo ya aprobado de la misma orden; genera un trabajo adicional con su propia cotización independiente. | Decisión del grupo (ejercitada con el escenario sintético) |
| 4 | Estado técnico y estado de pago son **dos campos separados**, nunca un estado combinado. | Decisión del grupo |
| 5 | No se solicita ni se almacena PIN o contraseña del equipo. | Decisión del grupo |
| 6 | Un equipo `Listo` sin retirar pasa a alerta a los 30 días, con segundo aviso documentado, sin disposición automática. | Problema **Relevado**; plazo y aviso, **Decisión del grupo** |
| 7 | No se habla de "rentabilidad neta": se habla de margen por reparación. El cálculo queda pospuesto hasta definir una política de costos (el esquema no guarda costo histórico de repuestos ni costo de mano de obra). | Decisión del grupo |
| 8 | Una orden **no puede pasar a `Entregado` si conserva saldo pendiente**. | Decisión del grupo; **A confirmar** con un negocio real |
| 9 | El cliente puede consultar el estado de su equipo sin escribir al técnico (mensaje preparado y, más adelante, enlace seguro de consulta). | **Relevada** (consultas repetitivas por WhatsApp) |

Cotización sin respuesta: queda pendiente y su reserva se libera por decisión manual del técnico;
no hay vencimiento automático en el P0.

Consecuencia de la regla 8: cuenta corriente queda fuera del P0 solo porque así lo decidimos. Si
un negocio real indica que entrega equipos con saldo, se reincorpora.

## 5. Escenario sintético de prueba del modelo

> **Este escenario es artificial.** Combina características de los tres perfiles relevados en un
> taller ficticio ("TecnoRepair") y no representa a ningún negocio real. Sirve para someter el
> modelo de datos a una situación exigente, no para validar reglas de negocio.

Se mantiene porque ejercita lo que el caso base no cubre: varios trabajos dentro de una misma
orden, repuesto sin stock y falla nueva durante la reparación. De hecho, ya permitió detectar que
el modelo anterior (un único `ordenes.estado`) no representaba trabajos en estados distintos dentro
de la misma orden. Ver la devolución del tutor del 05-10. El modelo actual resuelve eso con trabajos
y cotizaciones independientes.

**Día 1.** María trae un iPhone 12 que no carga; diagnóstico: conector de carga a reemplazar.
Se crea el **trabajo 1** (conector de carga) con su cotización 1; el repuesto queda reservado.

**Día 2.** María aprueba la cotización del conector (trabajo 1 sigue adelante) y pide revisar también
un parpadeo de la pantalla. Se crea el **trabajo 2** (pantalla) con su propia cotización, ligada a la
misma orden, y María la aprueba. El flex necesario no está en stock: el trabajo 2 queda
`Esperando repuesto` mientras el trabajo 1 está `En reparación`. La orden está `En proceso`.

**Día 3.** Llega el flex y se confirma su uso (recién ahí se descuenta del stock). Se terminan los
trabajos 1 y 2. En la prueba final aparece una falla nueva: el altavoz suena bajo. Se crea el
**trabajo 3** con su cotización. La orden no se retiene: lo aprobado sigue hacia `Listo`. María
rechaza la cotización del altavoz por costo (motivo registrado, reserva liberada) y el trabajo 3 queda
`Cancelado`. La orden pasa a `Listo` con resultado `Parcial`. El total de la orden es la suma de las
cotizaciones aprobadas (trabajos 1 y 2); María paga ese total y se entrega.

En un mismo momento de este escenario, los tres trabajos están en estados técnicos distintos
(por ejemplo, terminado, esperando repuesto y diagnosticado con cotización pendiente), algo que el
modelo representa sin un estado único de la orden.

**Semántica elegida:** las cotizaciones son **cotizaciones adicionales independientes**, una o más
por trabajo, y no versiones completas de la orden. El total de la orden es la suma de las
cotizaciones aprobadas; el saldo es ese total menos los pagos, y el estado de pago (`Pendiente`,
`Parcial`, `Pagado`) se deriva de ambos, sin campo editable.
