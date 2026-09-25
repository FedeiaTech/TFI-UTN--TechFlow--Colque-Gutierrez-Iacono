# Módulos — P0

Alcance acotado según el punto 2 de la devolución del tutor (`Devoluciones/1era devolucion de Tutor 26-08.pdf`): concentrar el proyecto en el circuito cliente → equipo → orden → diagnóstico → presupuesto → aprobación/rechazo → reparación → listo → entrega, sin sumar módulos adicionales hasta validarlo.

## Órdenes de Trabajo

Núcleo del sistema. Alta de orden a partir de un equipo ingresado, registro de diagnóstico, y flujo de estados desde `Recibido` hasta `Entregado`, incluyendo las variantes `Esperando repuesto` y `Listo - No retirado`.

## Clientes

Alta de cliente al ingresar un equipo, ficha con historial de equipos y órdenes asociadas.

## Presupuestos y Cobros

Presupuestos versionados por orden, con ítems que se aprueban o rechazan de forma independiente. Registro de pagos parciales y cálculo de saldo pendiente, sin cuenta corriente.

## Repuestos y Stock

Catálogo de repuestos por categoría, con reserva al presupuestar y descuento de stock recién al confirmarse el uso.

## Fuera de alcance de esta entrega

- **Proveedores y Compras**: gestión de órdenes de compra y reposición de stock desde proveedores.
- **Panel de Métricas + IA**: dashboard analítico y generación de resúmenes vía IA. El propio tutor pidió mantener la IA fuera del núcleo hasta tener datos reales y un sistema funcionando (punto 11 de su devolución).
- **Roles de usuario más allá del mínimo operativo**: diferenciación completa Administrador/Técnico/Recepcionista queda para una instancia posterior.

Estos puntos no se descartan del proyecto: se posponen para no repetir el error que el tutor marcó en el punto 2 de su devolución, donde el alcance volvía a acercarse a un ERP completo en lugar de validar primero el circuito núcleo.
