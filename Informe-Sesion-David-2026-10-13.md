# Informe de Sesión de Trabajo — 13/10/2026

**Autor:** David Gutierrez  
**Proyecto:** TechFlow — Sistema de Gestión para Servicios Técnicos (UTN FRLP)  
**Rama:** `feature/documentacion-devolucion-2-David` (a integrar en `dev`)  
**Instancia:** Documentación y Diseño — 2.ª Entrega

---

## 1. Punto de Partida y Estrategia

Continuando con la línea de trabajo iniciada por Fede el 10/10/2026 (diseño de base de datos relacional y esqueleto en FastAPI), el objetivo de esta jornada fue estructurar la documentación técnica y metodológica exigida por el tutor Oscar Londero en sus dos devoluciones.

Para facilitar la revisión por pares y el Pull Request en GitHub, los cambios se fueron integrando de forma atómica mediante commits temáticos acumulativos.

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
- **Hash:** `716fd91`
- **Archivos:**
  - `docs/entrega-2/04-caso-completo-reparacion.md`
  - `docs/entrega-2/diagramas/secuencia/caso_base_secuencia.puml`
  - `docs/entrega-2/diagramas/secuencia/escenario_sintetico_secuencia.puml`
- **Aporte clave:**
  - Define el caso real sobre el **Perfil A (Técnico Autoempleado)** con María y su iPhone 12.
  - Modela el cierre sin reparación (rechazo total o inviabilidad) y el tratamiento de equipos no retirados a 30 días con constancia de segundo aviso.
  - Establece la matriz de 10 reglas con origen explícito (`[RELEVADA]`, `[DECISIÓN DEL GRUPO]`, `[A CONFIRMAR]`).
  - Documenta el escenario sintético "TecnoRepair" como banco de pruebas para trabajos concurrentes y cotizaciones independientes.

### Commit 3: Requerimientos ISO 29148 y Casos de Uso
- **Hash:** `1ef3520`
- **Archivos:**
  - `docs/entrega-2/05-especificacion-requerimientos.md`
  - `docs/entrega-2/06-casos-de-uso-y-actores.md`
  - `docs/entrega-2/diagramas/casos_de_uso/casos_de_uso.puml`
- **Aporte clave:**
  - Especifica los Requerimientos Funcionales (RF) categorizados por módulo (Clientes, Equipos, Órdenes, Trabajos, Cotizaciones, Stock, Comunicación) con criterios de aceptación en formato Gherkin.
  - Define Requerimientos No Funcionales (RNF) clave: transaccionalidad ACID, seguridad JWT, bloqueo pesimista y usabilidad.
  - Matriz de trazabilidad cruzada (Problema $\rightarrow$ Regla $\rightarrow$ RF $\rightarrow$ Test).
  - Especifica los Casos de Uso del CU-01 al CU-08 con pre/postcondiciones y diagrama formal PlantUML.

### Commit 4: Modelo de Dominio, Máquinas de Estado y Persistencia
- **Hash:** `e4b2b73`
- **Archivos:**
  - `docs/entrega-2/07-modelo-dominio-y-maquinas-estado.md`
  - `docs/entrega-2/11-esquema-base-datos.md`
  - `docs/entrega-2/diagramas/estados/` (`estado_orden.puml`, `estado_trabajo.puml`, `estado_reserva.puml`)
  - `docs/entrega-2/diagramas/dominio/` (`modelo_dominio.puml`, `der_completo.puml`)
- **Aporte clave:**
  - Modelo conceptual de clases en PlantUML que resuelve la relación entre Orden y Trabajos independientes.
  - Máquinas de estados finitos con matrices de transición y condiciones de guarda para Orden y Trabajos.
  - Ciclo de reservas de repuestos (`reservada` $\rightarrow$ `utilizada` / `liberada`) y derivación determinística de saldos vía vistas SQL (`v_orden_saldo`).
  - Documentación del esquema relacional (13 tablas, 4 vistas, índices) y catálogo de las 7 pruebas obligatorias de backend (bloqueo por saldo, monto > 0, concurrencia pesimista con stock = 1).

### Commit 5: Arquitectura N-Capas, Principios UX, Roles y Viabilidad
- **Hash:** `aed7c21`
- **Archivos:**
  - `docs/entrega-2/02-propuesta-valor-y-viabilidad.md`
  - `docs/entrega-2/03-objetivos-alcance-y-modulos.md`
  - `docs/entrega-2/08-diseno-ux-y-flujos-pantalla.md`
  - `docs/entrega-2/09-roles-y-organizacion-equipo.md`
  - `docs/entrega-2/10-arquitectura-tecnica.md`
  - `docs/entrega-2/diagramas/arquitectura/` (`arquitectura_ncapas.puml`, `despliegue.puml`)
- **Aporte clave:**
  - Arquitectura N-Capas de FastAPI desacoplada de la SPA en React 18 + TS, patrones GoF y principios SOLID.
  - Justificación honesta del stack (FastAPI cerrado, sin Spring Boot ni MongoDB), seguridad OAuth2 + JWT y contratos REST.
  - Principios UX para taller, wireframe conceptual y especificación formal de plantillas dinámicas de WhatsApp con copiado en 1 clic.
  - Organización del equipo: definición de roles entre Federico, David y Brian, matriz RACI, metodología GitFlow y plan de trabajo del vertical ejecutable.

### Commit 6: Índices de Navegación, Exclusión de Guías y Cierre
- **Hash:** `ab78423`
- **Archivos:**
  - `.gitignore` (exclusión formal de guías de cátedra de uso local).
  - `README.md` (actualización de enlaces modulares de la 2.ª entrega).
  - `docs/entrega-2/README.md` (índice general de la 2.ª entrega con mapa modular y catálogo de diagramas PlantUML).
- **Aporte clave:** Conecta la totalidad del repositorio haciéndolo 100% navegable desde GitHub sin enlaces rotos, preparando la rama para el Pull Request hacia `dev`.

### Commit 7: Corrección de Origen de Cifras y Puntos a Completar por el Equipo
- **Estado:** en preparación
- **Archivos:** `01-contexto-problematica-y-relevamiento.md`, `04-caso-completo-reparacion.md`, `09-roles-y-organizacion-equipo.md`, `10-arquitectura-tecnica.md`, `entrega-2/README.md`.
- **Qué se corrigió:**
  - Las cifras de "1,5–2 h diarias" y "20–35% de margen" figuraban como hipótesis del equipo; en realidad salieron de una búsqueda con IA (Paso 4 del relevamiento original). Ahora están rotuladas así y se quitó la cifra de RN-09.
  - Los competidores quedan como relevamiento preliminar a verificar.
  - La tabla de competencias queda vacía para que cada uno declare su nivel real.
  - Roles y RACI marcados como propuesta a confirmar entre los tres.
- **Motivo:** la 1.ª devolución pide documentar el origen de las cifras, y no corresponde declarar niveles ajenos.

---

## 3. Estado Final del Repositorio

```text
Rama: feature/documentacion-devolucion-2-David
Commits consolidados:
  [x] Commit 1 (94c46db) - docs: estructura evidencia anonimizada de relevamiento y benchmark de mercado
  [x] Commit 2 (716fd91) - docs: formaliza caso base, variantes y escenario sintetico con diagramas de secuencia
  [x] Commit 3 (1ef3520) - docs: especifica requerimientos funcionales en Gherkin y casos de uso CU-01 a CU-08
  [x] Commit 4 (e4b2b73) - docs: modela maquinas de estado de orden/trabajos, ciclo de reservas y DER completo
  [x] Commit 5 (aed7c21) - docs: define arquitectura N-capas, roles del equipo, principios UX y plantillas de WhatsApp
  [x] Commit 6 (ab78423) - docs: actualiza indices de navegacion, exclusion de guias y referencias de la 2da entrega
  [ ] Commit 7           - docs: corrige origen de cifras y deja competencias y roles para confirmar
```
