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
No se pide el PIN. Se abre la orden en `Recibido` y se entrega un comprobante con el número.

**Diagnóstico.** El técnico descarta batería y detecta el conector de carga con un pin doblado.
Diagnóstico: conector de carga a reemplazar. La orden pasa a `Diagnosticado`.

**Presupuesto.** Se genera el presupuesto con repuesto y mano de obra. El repuesto queda
**reservado** (no se descuenta del stock). La orden pasa a `Presupuestado`. Se avisa a María con
un mensaje preparado de estado (sin integración con la API de WhatsApp).

**Aprobación y reparación.** María aprueba. El técnico confirma el uso del repuesto: recién ahí se
descuenta del stock. Se repara y la orden pasa por `En reparación`.

**Listo, cobro y entrega.** La orden pasa a `Listo`. Se avisa a María. Cuando retira, paga el
total (en una o más partes), el saldo pendiente queda en cero y la orden pasa a `Entregado`.

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
| 1 | Un presupuesto rechazado o reemplazado **nunca se borra**: queda en el historial de la orden. | Decisión del grupo |
| 2 | Un repuesto se marca `reservado` al presupuestarlo y **solo se descuenta del stock** cuando el técnico confirma que lo usó. Si se rechaza, vuelve a estar disponible. | Decisión del grupo |
| 3 | Una falla nueva detectada durante la reparación **no bloquea** lo ya aprobado de la misma orden; genera un trabajo o presupuesto adicional independiente. | Decisión del grupo (ejercitada con el escenario sintético) |
| 4 | Estado técnico y estado de pago son **dos campos separados**, nunca un estado combinado. | Decisión del grupo |
| 5 | No se solicita ni se almacena PIN o contraseña del equipo. | Decisión del grupo |
| 6 | Un equipo `Listo` sin retirar pasa a alerta a los 30 días, con segundo aviso documentado, sin disposición automática. | Problema **Relevado**; plazo y aviso, **Decisión del grupo** |
| 7 | No se habla de "rentabilidad neta": se habla de margen por reparación. El cálculo queda pospuesto hasta definir una política de costos (el esquema no guarda costo histórico de repuestos ni costo de mano de obra). | Decisión del grupo |
| 8 | Una orden **no puede pasar a `Entregado` si conserva saldo pendiente**. | Decisión del grupo; **A confirmar** con un negocio real |
| 9 | El cliente puede consultar el estado de su equipo sin escribir al técnico (mensaje preparado y, más adelante, enlace seguro de consulta). | **Relevada** (consultas repetitivas por WhatsApp) |

Consecuencia de la regla 8: cuenta corriente queda fuera del P0 solo porque así lo decidimos. Si
un negocio real indica que entrega equipos con saldo, se reincorpora.

## 5. Escenario sintético de prueba del modelo

> **Este escenario es artificial.** Combina características de los tres perfiles relevados en un
> taller ficticio ("TecnoRepair") y no representa a ningún negocio real. Sirve para someter el
> modelo de datos a una situación exigente, no para validar reglas de negocio.

Se mantiene porque ejercita lo que el caso base no cubre: varios trabajos dentro de una misma
orden, repuesto sin stock y falla nueva durante la reparación. De hecho, ya permitió detectar que
el modelo actual (un único `ordenes.estado`) no representa trabajos en estados distintos dentro
de la misma orden. Ver la devolución del tutor del 05-10.

**Día 1.** María trae un iPhone 12 que no carga; diagnóstico: conector de carga a reemplazar.
Presupuesto con el conector; el repuesto queda reservado.

**Día 2.** María aprueba el conector y pide revisar también un parpadeo de la pantalla. Se genera
una cotización adicional para la pantalla, ligada a la misma orden. El flex necesario no está en
stock: ese trabajo queda `Esperando repuesto` mientras el del conector sigue adelante.

**Día 3.** Llega el flex y se confirma su uso (recién ahí se descuenta del stock). Se reparan
conector y pantalla. En la prueba final aparece una falla nueva: el altavoz suena bajo. Se genera
una tercera cotización. La orden no se retiene: lo aprobado sigue hacia `Listo`. María rechaza el
altavoz por costo (motivo registrado). La orden pasa a `Listo` para los trabajos aprobados, se
cobra el total aprobado y se entrega.

**Pendiente de revisión del modelo:** definir si v1, v2 y v3 son versiones completas o
cotizaciones adicionales independientes, y cómo se calcula el saldo en cada caso.
