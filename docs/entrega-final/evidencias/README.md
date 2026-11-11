# Evidencias de funcionamiento

Ejecuciones reales del 11/11/2026 sobre la API desplegada (https://techflow-api.onrender.com) y la base de datos en Supabase. Los datos de cada recorrido son de demostración.

| Archivo | Qué muestra |
| --- | --- |
| `01-swagger-docs.png` | Endpoints expuestos por la API desplegada |
| `02-health.png`, `03-health-db.png` | Disponibilidad de la API y de la conexión a la base |
| `04-saldo-orden-entregada.png` | Saldo de una orden entregada, derivado de cotizaciones aprobadas y pagos |
| `05-pytest-local.txt` | Suite de pruebas contra la base real (5 pruebas) |
| `06-recorrido-deploy.txt` | Recorrido completo con pagos parciales: la entrega con saldo responde 400 y el pago de monto 0 responde 422 |
| `07-escenario-falla-nueva-deploy.txt` | Falla nueva durante la reparación: el trabajo adicional no altera lo aprobado y la orden cierra como `parcial` |
| `08-rechazo-libera-reserva-deploy.txt` | Con stock 1, una segunda reserva responde 400; rechazar la cotización libera el repuesto |
| `09-irreparable-libera-deploy.txt` | Un trabajo declarado irreparable libera su reserva y deja de sumar al saldo |
