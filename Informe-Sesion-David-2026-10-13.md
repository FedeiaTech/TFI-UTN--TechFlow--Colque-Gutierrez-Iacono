# Informe de Sesión de Trabajo — 13/10/2026

**Autor:** David Gutierrez 
**Proyecto:** TechFlow — Sistema de Gestión para Servicios Técnicos (UTN FRLP)  
**Rama:** `feature/documentacion-devolucion-2-David` (a integrar en `dev`)  
**Instancia:** Avance modular — **Commit 1 / 6**

---

## 1. Punto de Partida

Continuando con el informe de sesión de Fede del 10/10/2026 (donde se rediseñó el esquema relacional en PostgreSQL y se montó el esqueleto inicial de FastAPI con endpoints `/health`), el objetivo de esta jornada fue estructurar y cerrar la documentación formal de la 2.ª Entrega requerida por el tutor Oscar Londero y la cátedra de la UTN.

Para que el avance sea claro y fácil de revisar en el Pull Request, acordamos no subir un commit gigante con todo mezclado, sino dividir la entrega en **pequeños commits atómicos por tema**. Este informe refleja el estado correspondiente al **primer commit**.

---

## 2. Alcance de este Avance (Commit 1)

### 2.1. Objetivos del Commit 1
- Responder a la crítica metodológica de Oscar sobre la evidencia del relevamiento (Puntos 1 y 7 de la 1.ª Devolución).
- Blanquear el origen de las cifras y datos citados en la propuesta original.
- Organizar la evidencia primaria de campo en un anexo formal anonimizado.
- Redactar el documento formal de contexto, problemática y benchmarking del sector.

### 2.2. Tareas Realizadas y Archivos Incluidos

| Archivo / Componente | Acción | Justificación / Contenido |
|---|---|---|
| `docs/entrega-1/relevamiento-de-campo-original.md` | Reubicado y preservado | Se preserva el informe original de relevamiento de la 1.ª entrega en su carpeta histórica para mantener la trazabilidad. |
| `docs/entrega-2/anexos/A-respuestas-encuesta.md` | Creado | **Evidencia primaria pura:** Se transcribieron las 4 respuestas completas y textuales del formulario Google (A, B, C y D), debidamente anonimizadas. Se aclara que la 1.ª entrega solo había analizado 3 de las 4 respuestas. |
| `docs/entrega-2/01-contexto-problematica-y-relevamiento.md` | Creado | • Distinción explícita de datos con leyendas: `[DATO RELEVADO]`, `[HIPÓTESIS EQUIPO]` y `[REFERENCIA SECTOR]`.<br>• Se aclara que números como *"1.5 a 2 hs de WhatsApp"* o *"20% a 35% de merma"* fueron estimaciones de impacto del grupo y no mediciones estadísticas de los talleres.<br>• Cuadro de los 4 perfiles reales y sus dolores textuales.<br>• Benchmarking comparativo frente a soluciones del mercado local (Sistema Loop, STApp, SAT Network). |

---

## 3. Estado del Repositorio tras el Commit 1

```text
Rama actual: feature/documentacion-entrega-2-David (partida desde dev)
Commit 1: docs: estructura evidencia anonimizada de relevamiento y benchmark de mercado
Estado: En staging / commiteado el bloque de evidencia y problemática.
```

---

## 4. Plan de Próximos Commits (Trabajo ya preparado en local)

Los siguientes documentos y diagramas ya están redactados y organizados en el espacio de trabajo local, y se irán comiteando progresivamente actualizando este informe en cada paso:

- [ ] **Commit 2:** Reglas de negocio y caso completo (`04-caso-completo-reparacion.md`, diagramas de secuencia del caso base y escenario sintético).
- [ ] **Commit 3:** Especificación formal de requerimientos ISO 29148 y Casos de Uso (`05-...`, `06-...`, diagrama PlantUML de casos de uso).
- [ ] **Commit 4:** Modelo conceptual de dominio, máquinas de estado y DER completo (`07-...`, `11-...`, diagramas de estados y DER).
- [ ] **Commit 5:** Arquitectura N-Capas, Principios UX / plantillas WhatsApp y Roles del equipo (`02-...`, `03-...`, `08-...`, `09-...`, `10-...`, diagramas de arquitectura).
- [ ] **Commit 6:** Actualización de READMEs generales, índices de navegación y cierre del Pull Request hacia `dev`.
