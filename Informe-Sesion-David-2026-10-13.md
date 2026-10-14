# Informe de Sesión de Trabajo — 13/10/2026

**Autor:** David Gutierrez  
**Proyecto:** TechFlow — Sistema de Gestión para Servicios Técnicos (UTN FRLP)  
**Rama:** `feature/documentacion-devolucion-2-David` (a integrar en `dev`)  
**Instancia:** Documentación y Diseño — 2.ª Entrega

---

## 1. Punto de Partida y Estrategia

Continuando con la línea de trabajo iniciada por Fede el 10/10/2026 (diseño de base de datos relacional y esqueleto en FastAPI), el objetivo de esta jornada fue estructurar la documentación técnica y metodológica exigida por el tutor Oscar Londero en sus dos devoluciones.

Para facilitar la revisión por pares y el Pull Request en GitHub, los cambios se van integrando de forma atómica mediante commits temáticos acumulativos.

---

## 2. Registro Acumulativo de Avances por Commit

### Commit 1: Evidencia del Relevamiento y Problemática
- **Hash:** `94c46db`
- **Archivos:**
  - `docs/entrega-1/relevamiento-de-campo-original.md` (reubicado para preservar trazabilidad).
  - `docs/entrega-2/anexos/A-respuestas-encuesta.md` (transcripción textual de las 4 respuestas de la encuesta, anonimizadas).
  - `docs/entrega-2/01-contexto-problematica-y-relevamiento.md` (distinción formal entre datos observados, hipótesis del grupo y benchmarking de mercado: Loop, STApp, SAT Network).
- **Aporte clave:** Resuelve la observación 1 de la 1.ª devolución, blanqueando el origen de las estimaciones y aislando la evidencia empírica.

### Commit 2: Caso de Referencia, Reglas de Negocio y Diagramas de Secuencia
- **Estado:** En proceso / staging
- **Archivos:**
  - `docs/entrega-2/04-caso-completo-reparacion.md`
  - `docs/entrega-2/diagramas/secuencia/caso_base_secuencia.puml`
  - `docs/entrega-2/diagramas/secuencia/escenario_sintetico_secuencia.puml`
- **Aporte clave:**
  - Define el caso real sobre el **Perfil A (Técnico Autoempleado)** con María y su iPhone 12.
  - Modela el cierre sin reparación (rechazo total o inviabilidad) y el tratamiento de equipos no retirados a 30 días con constancia de segundo aviso.
  - Establece la matriz de 10 reglas con origen explícito (`[RELEVADA]`, `[DECISIÓN DEL GRUPO]`, `[A CONFIRMAR]`).
  - Documenta el escenario sintético "TecnoRepair" como banco de pruebas para trabajos concurrentes y cotizaciones independientes.

---

## 3. Estado del Repositorio

```text
Rama: feature/documentacion-devolucion-2-David
Commits completados:
  [x] Commit 1 (94c46db) - docs: estructura evidencia anonimizada de relevamiento y benchmark de mercado
  [ ] Commit 2           - docs: formaliza caso base, variantes y escenario sintetico con diagramas de secuencia
  [ ] Commit 3           - docs: especifica requerimientos funcionales en Gherkin y casos de uso CU-01 a CU-08
  [ ] Commit 4           - docs: modela maquinas de estado de orden/trabajos, ciclo de reservas y DER completo
  [ ] Commit 5           - docs: define arquitectura N-capas, roles del equipo, principios UX y plantillas de WhatsApp
  [ ] Commit 6           - docs: actualiza indices de navegacion y referencias de la 2da entrega
```
