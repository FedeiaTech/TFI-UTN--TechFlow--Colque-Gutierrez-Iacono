# Módulos — P0

Alcance acotado según el punto 2 de la devolución del tutor (`Devoluciones/1era devolucion de Tutor 26-08.pdf`): concentrar el proyecto en el circuito cliente → equipo → orden → diagnóstico → cotización → aprobación/rechazo → reparación → listo → entrega, sin sumar módulos adicionales hasta validarlo.

## Órdenes de Trabajo

Núcleo del sistema. Alta de orden a partir de un equipo ingresado, con el estado físico y los accesorios de ese ingreso y un **técnico responsable** (usuario del sistema). La orden tiene un estado global simple (`Recibido`, `En proceso`, `Listo`, `Listo - No retirado`, `Entregado`) y un resultado (`Reparado`, `Parcial`, `Sin reparación`) que se fija al quedar lista.

Cada orden agrupa uno o más **trabajos** (por ejemplo, conector de carga, pantalla y altavoz). Cada trabajo tiene su diagnóstico y su estado técnico propio (`Pendiente de diagnóstico`, `Diagnosticado`, `Esperando repuesto`, `En reparación`, `Terminado`, `Irreparable`, `Cancelado`). Una falla nueva durante la reparación se agrega como trabajo nuevo sin frenar los demás.

Cada cambio de estado de la orden o de un trabajo queda en un **historial** con el usuario que lo hizo, la fecha y un motivo opcional.

**Consulta de estado (regla 9):** un botón "copiar mensaje de estado" arma un texto con el estado de la orden y de sus trabajos, para que el técnico lo pegue donde quiera. No se integra la API de WhatsApp.

## Clientes

Alta de cliente al ingresar un equipo, ficha con historial de equipos y órdenes asociadas.

## Usuarios

Identidad mínima para ingresar al sistema (nombre, email, contraseña almacenada como hash, activo). Sirve para asignar el técnico responsable de cada orden y para registrar quién cambió un estado o cobró un pago. La matriz de roles queda fuera del P0.

## Cotizaciones y Cobros

Cada trabajo tiene sus **cotizaciones**: son cotizaciones independientes (no versiones completas de la orden), con ítems de repuesto, mano de obra o descripción, cantidad y precio unitario guardado como snapshot. Cada cotización se aprueba o se rechaza (con motivo) sin afectar las de otros trabajos; las rechazadas o reemplazadas nunca se borran. Solo hay una cotización vigente por trabajo.

El total de la orden es la suma de las cotizaciones aprobadas. Registro de pagos parciales (monto mayor a cero, con el usuario que los registra) y cálculo de saldo y estado de pago (`Pendiente`, `Parcial`, `Pagado`) derivados, sin cuenta corriente. Una orden no pasa a `Entregado` con saldo pendiente.

## Repuestos y Stock

Catálogo de repuestos por categoría, con precio de referencia. El repuesto se reserva al cotizar (una reserva con cantidad), se libera si la cotización se rechaza y se descuenta del stock recién cuando el técnico confirma el uso. La disponibilidad es el stock total menos las reservas activas.

## Fuera de alcance de esta entrega

- **Proveedores y Compras**: gestión de órdenes de compra y reposición de stock desde proveedores.
- **Panel de Métricas + IA**: dashboard analítico y generación de resúmenes vía IA. El propio tutor pidió mantener la IA fuera del núcleo hasta tener datos reales y un sistema funcionando (punto 11 de su devolución).
- **Roles de usuario más allá del mínimo operativo**: la identidad (`usuarios`) sí está en el P0; la diferenciación completa Administrador/Técnico/Recepcionista queda para una instancia posterior.

Estos puntos no se descartan del proyecto: se posponen para no repetir el error que el tutor marcó en el punto 2 de su devolución, donde el alcance volvía a acercarse a un ERP completo en lugar de validar primero el circuito núcleo.
