# 08 — Diseño UX, Arquitectura de Información y Flujos de Pantalla

## 1. Filosofía de Diseño UX para Taller Electrónico

El diseño de la experiencia de usuario (UX) en TechFlow está concebido específicamente para el entorno físico de un servicio técnico, caracterizado por:
1. **Ritmo acelerado en mostrador:** El cliente espera de pie mientras entrega o retira su equipo; la carga de datos no debe demorar más de 60–90 segundos.
2. **Entorno de laboratorio técnico:** El técnico suele trabajar con manos ocupadas, herramientas de banco y monitores compartidos; la información sobre diagnóstico y repuestos debe ser legible a un golpe de vista sin navegación en cascada innecesaria.
3. **Comunicación asíncrona sin fricción:** Minimizar el tiempo de mecanografía en WhatsApp mediante botones de copiado instantáneo de textos contextualizados.

### Principios Rectores:
- **Cero ventanas modales anidadas:** Las acciones críticas se resuelven en la misma página o en modales simples de un único paso.
- **Jerarquía visual inequívoca:** Los estados técnicos (`En reparación`, `Esperando repuesto`) y los estados financieros (`Saldo: $X`, `Pagado`) están separados físicamente en la pantalla con codificación de color consistente (badges).
- **Prevención proactiva de errores:** Deshabilitación de botones de entrega si el saldo es mayor a cero, con tooltip explicativo del motivo del bloqueo.

---

## 2. Mapa de Navegación y Pantallas del MVP (P0)

```text
[ Login / Auth ]
       │
       ▼
[ Dashboard / Tablero de Órdenes ] ◄────────────────────────┐
       │                                                    │
       ├──► [ Formulario de Recepción / Nueva Orden ] ──────┤
       │                                                    │
       ├──► [ Ficha de Detalle de Orden ] ──────────────────┤
       │         ├──► Modal de Agregar Trabajo              │
       │         ├──► Modal de Emitir Cotización            │
       │         ├──► Modal de Registrar Pago               │
       │         └──► Botón: Copiar Mensaje WhatsApp        │
       │                                                    │
       └──► [ Catálogo de Pañol y Disponibilidad ] ─────────┘
```

---

## 3. Wireframes Conceptuales de Pantallas Clave

### 3.1. Pantalla 1: Ficha de Detalle de Orden de Trabajo (`/ordenes/{id}`)

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│  TechFlow | Taller Central             [Usuario: David (Técnico)]  [Cerrar Sesión]     │
├────────────────────────────────────────────────────────────────────────────────────────┤
│  ◄ Volver a Órdenes                                                                    │
│                                                                                        │
│  ORDEN #101                                                   ESTADO GLOBAL: [ LISTO ] │
│  Fecha Ingreso: 12/10/2026 10:15 hs                           RESULTADO:     [ REPARADO ]
│  Técnico Responsable: David Gutiérrez                         ESTADO PAGO:   [ PARCIAL ]
├────────────────────────────────────────────────────────────────────────────────────────┤
│  ACCIONES RÁPIDAS:                                                                     │
│  [ 📋 Copiar Mensaje: Equipo Listo ]    [ ➕ Agregar Trabajo ]    [ 🚪 Entregar Equipo ] │
├──────────────────────────────────────────────────────┬─────────────────────────────────┤
│  DATOS DEL CLIENTE Y EQUIPO                          │  RESUMEN FINANCIERO             │
│  Cliente: María López                                │  Total Aprobado:   $ 8.000,00   │
│  Teléfono: 11-2345-6789                              │  Total Pagado:     $ 3.000,00   │
│  Dispositivo: Celular — Apple iPhone 12              │  ────────────────────────────── │
│  IMEI / Serie: 356987412589632                       │  SALDO A COBRAR:   $ 5.000,00   │
│  Falla Reportada: "No carga la batería"              │  (Bloquea entrega física)       │
│  Estado Físico Ingreso: "2 rayones en pantalla"      │  [ 💵 Registrar Pago ]           │
│  Accesorios Dejados: "Solo equipo, sin cargador"     │                                 │
├──────────────────────────────────────────────────────┴─────────────────────────────────┤
│  TRABAJOS TÉCNICOS ASOCIADOS A ESTA ORDEN                                              │
│                                                                                        │
│  ┌─ TRABAJO #1: Reemplazo de pin de carga ───────────── ESTADO: [ TERMINADO ] ──────┐  │
│  │  Diagnóstico: Pin 4 doblado en conector Lightning.                                │  │
│  │                                                                                    │  │
│  │  COTIZACIÓN VIGENTE (Cotización #1 - Aprobada el 12/10 11:30 hs):                  │  │
│  │  • [Repuesto] Conector Carga iPhone 12  (x1)  $ 5.000,00  → Estado: [ UTILIZADA ]  │  │
│  │  • [Mano de Obra] Desarme y soldadura   (x1)  $ 3.000,00                          │  │
│  │  Subtotal Cotización: $ 8.000,00                                                   │  │
│  └────────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                        │
│  ┌─ HISTORIAL DE AUDITORÍA Y TRAZABILIDAD (Log inmutable) ──────────────────────────┐  │
│  │  • 12/10 16:30 | David | Orden pasó a LISTO (Resultado: Reparado).                 │  │
│  │  • 12/10 16:28 | David | Trabajo #1 pasó a TERMINADO. Repuesto conector utilizado. │  │
│  │  • 12/10 11:35 | David | Registró pago seña de $3.000,00.                          │  │
│  │  • 12/10 11:30 | David | Cotización #1 APROBADA por el cliente.                    │  │
│  │  • 12/10 10:45 | David | Emitió Cotización #1 ($8.000). Repuesto conector reservado│  │
│  │  • 12/10 10:15 | David | Orden creada en RECIBIDO. Falla: "No carga".              │  │
│  └────────────────────────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Especificación del Módulo de "Mensaje Preparado" para WhatsApp

Para resolver el problema empírico de las **consultas repetitivas por WhatsApp** sin incurrir en los costos y complejidades de la API oficial de Meta, TechFlow implementa plantillas dinámicas que se copian al portapapeles mediante la API nativa `navigator.clipboard.writeText()` del navegador.

### 4.1. Catálogo de Plantillas Dinámicas

#### Plantilla 1: Comprobante de Recepción (Al crear la orden)
- **Disparador:** Botón *"Copiar Mensaje: Ingreso"* en pantalla de recepción.
- **Formato del texto generado:**
  ```text
  Hola *{nombre_cliente}*, recibimos tu *{tipo_equipo} {modelo}* en el taller.
  📄 *Orden de Trabajo:* #{orden_id}
  🔧 *Falla reportada:* {falla_reportada}
  Te estaremos avisando por este medio una vez realizado el diagnóstico técnico. ¡Muchas gracias!
  _TechFlow — Servicio Técnico_
  ```

#### Plantilla 2: Envío de Presupuesto / Cotización (Al cotizar trabajos)
- **Disparador:** Botón *"Copiar Mensaje: Cotización"* en el bloque del trabajo.
- **Formato del texto generado:**
  ```text
  Hola *{nombre_cliente}*, tenemos el diagnóstico de tu *{modelo}* (Orden #{orden_id}):
  🔎 *Diagnóstico:* {diagnostico}
  💰 *Presupuesto:*
  {detalle_items}
  💵 *TOTAL:* ${total_cotizacion}
  
  Por favor, confirmanos si aceptás la cotización para reservar los repuestos y comenzar la reparación. ¡Saludos!
  ```

#### Plantilla 3: Aviso de Equipo Listo para Retirar
- **Disparador:** Botón *"Copiar Mensaje: Equipo Listo"* (disponible cuando la orden pasa a `listo`).
- **Formato del texto generado:**
  ```text
  ¡Buenas noticias *{nombre_cliente}*! 🎉
  Tu *{modelo}* (Orden #{orden_id}) ya está listo para retirar en nuestro local.
  📊 *Resultado:* {resultado}
  💵 *Saldo pendiente a abonar:* ${saldo_pendiente}
  
  Podés pasar de lunes a viernes de 09:00 a 19:00 hs. ¡Te esperamos!
  _TechFlow — Servicio Técnico_
  ```

#### Plantilla 4: Segundo Aviso por Equipo Abandonado (Aviso de 30 días)
- **Disparador:** Botón *"Copiar Mensaje: 2.º Aviso de Retiro"* (habilitado en estado `listo_no_retirado`).
- **Formato del texto generado:**
  ```text
  Estimado/a *{nombre_cliente}*, nos comunicamos desde TechFlow en relación a su equipo *{modelo}* (Orden #{orden_id}), finalizado el día {fecha_listo}.
  Le recordamos que han transcurrido más de 30 días desde la notificación inicial sin que se haya registrado el retiro del mismo.
  Solicitamos coordinar el retiro a la brevedad para evitar cargos de guarda y custodia.
  Saldo pendiente: ${saldo_pendiente}. Quedamos a su disposición.
  ```

---

## 5. Recorridos de Usuario (User Journeys)

### 5.1. Recorrido A: Recepción y Creación Rápida de Orden (Duración objetivo: < 60 seg)
1. **Acceso:** El operador presiona el atajo `[+ Nueva Orden]` en la barra superior.
2. **Identificación:** Escribe el teléfono del cliente; si existe, sus datos se autocompletan en 200 ms; si no, escribe nombre y teléfono.
3. **Equipo:** Selecciona modelo o ingresa marca/modelo en campos sugeridos.
4. **Constatación:** Dicta o tipea falla y estado visible; el sistema enfoca automáticamente el campo siguiente con `Tab`.
5. **Finalización:** Presiona `[Guardar Orden y Copiar Aviso]`. El sistema emite la orden y carga el texto de WhatsApp en el portapapeles en un único evento.

### 5.2. Recorrido B: Retiro en Mostrador y Control de Saldo (Duración objetivo: < 30 seg)
1. **Búsqueda:** El operador digita el número de orden (`101`) o el apellido en el buscador universal.
2. **Visualización:** La pantalla resalta en color naranja el badge `Saldo: $5.000` y muestra el botón `[Entregar]` bloqueado.
3. **Cobro:** Clic en `[Registrar Pago]`, ingresa `5000` y presiona `Enter`.
4. **Validación:** El badge cambia a verde `Pagado / Saldo: $0.00` y el botón `[Entregar]` se activa inmediatamente en color azul.
5. **Cierre:** Clic en `[Entregar]`. El equipo queda registrado como entregado y sale de la lista de activos.
