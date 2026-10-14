# 02 — Propuesta de Valor, Viabilidad y Criterios de Éxito

## 1. Declaración de la Propuesta de Valor

**TechFlow** es una plataforma web concebida para profesionalizar y dotar de trazabilidad integral al ciclo operativo de talleres y servicios técnicos de reparación electrónica.

A diferencia de soluciones administrativas genéricas o sistemas de retail adaptados a la fuerza, TechFlow centra su propuesta en la **verdad operativa del taller**:
- Cada reparación puede componerse de múltiples fallas o intervenciones técnicas con dinámicas independientes.
- El presupuesto debe ser transparente y respaldado por una reserva real de repuestos sin comprometer el pañol.
- La información de estado debe estar disponible de forma instantánea para reducir a cero los tiempos muertos en comunicaciones redundantes.

### 1.1. Lienzo de Propuesta de Valor (Value Proposition Canvas)

| Elemento | Realidad del Taller / Dolores del Cliente | Solución TechFlow |
|---|---|---|
| **Dolores (Pains)** | • Interrupciones constantes por "¿ya está mi equipo?".<br>• Confusión sobre el estado real de un trabajo con fallas múltiples.<br>• Repuestos que faltan a la hora de reparar porque se asignaron a otro equipo.<br>• Equipos terminados que pasan meses abandonados sin constancia de aviso.<br>• Clientes que cuestionan el importe final por falta de desglose inicial. | • **Botón de mensaje preparado de estado** listo para enviar en 1 segundo.<br>• **Sub-entidad Trabajo con estado técnico independiente** dentro de la Orden.<br>• **Sistema de reservas con bloqueo concurrente** y descuento atómico al uso.<br>• **Flujo para equipos no retirados a 30 días** con registro de avisos fehacientes.<br>• **Cotizaciones versionadas con snapshot de precio y cantidad** calculadas en vista. |
| **Alegrías (Gains)** | • Saber con certeza qué técnico intervino y qué se le hizo al equipo.<br>• Control claro del saldo pendiente antes de entregar.<br>• Certeza de repuestos disponibles en el banco de trabajo.<br>• Registro histórico de ingresos anteriores del mismo equipo. | • **Historial inmutable de estados** con responsable asociado.<br>• **Regla de backend:** bloqueo de entrega si existe saldo mayor a cero.<br>• **Vista de disponibilidad real** de pañol (`stock_total - reservas_activas`).<br>• **Entidad Equipo disociada de Orden:** preserva historial ante reingresos. |

---

## 2. Evaluación de Viabilidad Multidimensional

Siguiendo las pautas metodológicas de la cátedra para la formulación del Trabajo Final Integrador, se analiza la factibilidad del proyecto en sus tres dimensiones esenciales:

### 2.1. Viabilidad Técnica
- **Alineación con el perfil formativo:** El stack elegido (FastAPI en backend con arquitectura N-capas, PostgreSQL con integridad relacional ACID, y React con TypeScript en frontend) capitaliza los conocimientos adquiridos a lo largo de la tecnicatura en programación web, bases de datos relacionales y diseño de sistemas.
- **Riesgo de sobreingeniería mitigado:** Se descartaron arquitecturas de microservicios, bases de datos duales (MongoDB + PostgreSQL) y dependencias de mensajería asíncrona externa (Kafka/RabbitMQ). Se opera con un monolito modular con separación física Frontend/Backend conectado por API REST estándar.
- **Validación temprana con tests automatizados:** La integridad del negocio (concurrencia en pañol, estados terminales y validación de saldos) se confía al motor relacional de PostgreSQL complementado con pruebas de integración en pytest sobre transacciones aisladas.

### 2.2. Viabilidad Operativa
- **Baja fricción de adopción:** La interfaz está orientada a operadores de taller y recepcionistas, priorizando pantallas limpias, carga rápida en dispositivos de escritorio/móviles y atajos directos (como la copia de mensajes preformateados).
- **Independencia de APIs pagas:** No se ata el sistema a la API oficial de WhatsApp Cloud (que exige cuentas de empresa Meta verificadas, tarjetas de crédito y costos por conversación), garantizando que cualquier microtaller pueda utilizar TechFlow sin costo operativo adicional.
- **Seguridad y responsabilidad civil:** La decisión deliberada de **no almacenar credenciales de desbloqueo (PIN/patrón)** exime al taller y al sistema de responsabilidades legales frente a eventuales filtraciones de datos personales de los clientes.

### 2.3. Viabilidad Temporal y Alcance Académico
- **Alineación con el calendario lectivo:** El cronograma de la asignatura fija la entrega de la solución terminada para noviembre de 2026. Al circunscribir el alcance de la etapa P0 estrictamente al flujo núcleo (`Cliente → Equipo → Orden → Diagnóstico → Cotización → Aprobación → Reparación → Listo → Pago → Entrega`), se garantiza la finalización, testeo y despliegue dentro de los plazos estipulados.
- **Estrategia iterativa de desarrollo:**
  $$\text{Modelar} \longrightarrow \text{Implementar vertical ejecutable} \longrightarrow \text{Comprobar con tests} \longrightarrow \text{Corregir y avanzar}$$
  Se descarta la postergación de la codificación a la espera de "especificaciones cerradas al 100%".

---

## 3. Rol de la Inteligencia Artificial y Declaración de Autoría

En estricta concordancia con la Observación 1 de la 1.ª Devolución del tutor Oscar Londero:

> *"Eliminaría conclusiones del tipo 'veredicto según IA': la IA puede ayudarnos a analizar, pero las conclusiones profesionales tienen que ser asumidas y justificadas por ustedes. Mantengan IA fuera del núcleo."*

El equipo establece formalmente los límites del uso de herramientas de IA generativa en el proyecto:

1. **Uso como herramienta exploratoria de asistencia:** La IA fue empleada como apoyo de redacción preliminar, generación de ideas de contraste y síntesis de fuentes abiertas en la etapa de formulación inicial.
2. **Autoría y validación humana:** Todas las conclusiones de diseño, decisiones arquitectónicas, reglas de negocio y restricciones del modelo de datos son **responsabilidad y decisión exclusiva del equipo de desarrollo**. No se presentan "veredictos automáticos" ni conclusiones delegadas en modelos de lenguaje.
3. **Exclusión de la IA del Alcance Núcleo (P0):** En esta etapa del sistema, **no existe ningún componente de IA, modelo LLM ni arquitectura RAG en el flujo operativo**. Las métricas de estado y los cálculos financieros se resuelven de forma puramente determinística mediante consultas SQL estructuradas y lógica de backend. La eventual incorporación de asistentes de lenguaje para resúmenes de órdenes queda relegada a etapas futuras (P2) cuando el sistema cuente con datos operativos reales acumulados.

---

## 4. Criterios de Éxito del MVP (P0)

El éxito de la implementación de la primera fase se medirá a través del cumplimiento de los siguientes indicadores objetivos y verificables mediante software:

1. **Trazabilidad Completa del Circuito:** Ejecución sin errores del recorrido vertical de punta a punta: desde el alta del cliente hasta la entrega física del equipo con saldo cero.
2. **Soporte de Trabajos Concurrentes:** Capacidad demostrada del sistema para gestionar una orden que contenga trabajos en estados disímiles (p. ej., uno terminado y otro en espera de repuesto) sin inconsistencias de estado global.
3. **Consistencia Transaccional de Stock:** Comprobación mediante prueba automatizada de que ante dos intentos concurrentes de reservar la última unidad disponible de un repuesto (`stock = 1`), exactamente una transacción prevalece y la otra es rechazada ordenadamente.
4. **Protección de Saldo Pendiente:** Garantía inquebrantable mediante regla de negocio y test unitario de que ninguna orden con saldo deudor pueda transicionar al estado `Entregado`.
5. **Reducción del Tiempo de Redacción de Avisos:** Generación instantánea en interfaz del mensaje de estado formateado con los datos de la orden para su transmisión directa al cliente.
