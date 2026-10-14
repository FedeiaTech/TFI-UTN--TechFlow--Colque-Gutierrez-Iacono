# Índice de Documentación — 2.ª Entrega (Modelo, Arquitectura y Dominio)

Este directorio consolida la documentación formal de ingeniería de software de **TechFlow** para la 2.ª Entrega del Trabajo Final Integrador (UTN FRLP).

La totalidad de los documentos ha sido diseñada respondiendo punto por punto a las observaciones de las **dos devoluciones docentes del tutor Oscar Londero** (26/08 y 05/10), articulando el ciclo completo desde la identificación del problema en el territorio hasta el diseño técnico y el modelo de datos relacional.

---

## 🗺️ Mapa Modular de Documentación

| # | Documento | Eje Temático y Alcance | Devoluciones / Requisitos Atendidos |
|---|---|---|---|
| **01** | [**Contexto, Problemática y Relevamiento**](01-contexto-problematica-y-relevamiento.md) | Caracterización del sector, 4 perfiles empíricos, triangulación de evidencia, separación de datos observados vs. estimaciones del grupo, benchmarking con el mercado (Loop, STApp, SAT). | 1.ª Dev (Puntos 1 y 7); 2.ª Dev (Punto 1 y WhatsApp). |
| **02** | [**Propuesta de Valor, Viabilidad y Criterios**](02-propuesta-valor-y-viabilidad.md) | Canvas de propuesta de valor, viabilidad técnica/operativa/temporal, declaración honesta de autoría y exclusión de IA del núcleo, criterios de éxito del MVP. | 1.ª Dev (Puntos 1, 11); 2.ª Dev (Criterio de avance). |
| **03** | [**Objetivos, Alcance y Módulos**](03-objetivos-alcance-y-modulos.md) | Objetivos generales y específicos, matriz MoSCoW, especificación de los 7 módulos del P0 y delimitación estricta de módulos fuera de alcance (P1/P2). | 1.ª Dev (Puntos 2, 11); 2.ª Dev (Recorte estricto). |
| **04** | [**Caso Completo de Reparación y Reglas**](04-caso-completo-reparacion.md) | Caso real paso a paso (Técnico Autoempleado), variantes de cierre sin reparación y abandono (30 días), matriz de 10 reglas con origen ([RELEVADA], [DECISIÓN], [A CONFIRMAR]), y escenario sintético "TecnoRepair". | 1.ª Dev (Puntos 3, 4, 5, 8); 2.ª Dev (Puntos 1, 2, 3, 5, 6, 8, 13, 14, 15). |
| **05** | [**Especificación de Requerimientos (SRS)**](05-especificacion-requerimientos.md) | Estándar ISO/IEC/IEEE 29148: Requerimientos Funcionales con criterios de aceptación en Gherkin, Requerimientos No Funcionales y matriz de trazabilidad problema $\rightarrow$ regla $\rightarrow$ test. | Estándares de ingeniería de software; trazabilidad completa. |
| **06** | [**Casos de Uso y Actores**](06-casos-de-uso-y-actores.md) | Caracterización de actores, especificación formal de casos de uso (CU-01 a CU-08), pre/postcondiciones y flujos alternativos. | Trazabilidad del flujo de usuario del taller. |
| **07** | [**Modelo de Dominio y Máquinas de Estado**](07-modelo-dominio-y-maquinas-estado.md) | Modelo conceptual de clases, máquinas de estado de Orden y Trabajo, ciclo de vida de reservas (`reservada` $\rightarrow$ `utilizada` / `liberada`), semántica de cotizaciones independientes y vistas SQL reactivas. | 1.ª Dev (Puntos 3, 4, 5); 2.ª Dev (Puntos 2, 3, 4, 9, 10, 14). |
| **08** | [**Diseño UX y Flujos de Pantalla**](08-diseno-ux-y-flujos-pantalla.md) | Principios UX de taller, mapa de pantallas, wireframe conceptual de orden, catálogo de plantillas para WhatsApp (copiado en 1 clic) y recorridos de usuario. | 1.ª Dev (Punto 7); 2.ª Dev (WhatsApp y usabilidad). |
| **09** | [**Organización del Equipo y Roles**](09-roles-y-organizacion-equipo.md) | Asignación de roles entre los 3 integrantes, matriz RACI, metodología Kanban en Trello, flujo de Git (ramas) y plan de acción para el vertical ejecutable. | 1.ª Dev (Punto 10); 2.ª Dev (Metodología incremental). |
| **10** | [**Arquitectura Técnica y Patrones**](10-arquitectura-tecnica.md) | Arquitectura N-Capas, justificación honesta del stack (FastAPI + React + PostgreSQL), patrones GoF y arquitectónicos, principios SOLID, seguridad OAuth2 + JWT y contratos REST. | 1.ª Dev (Puntos 9, 10); 2.ª Dev (Puntos 8, 18). |
| **11** | [**Esquema de Base de Datos y Persistencia**](11-esquema-base-datos.md) | Descripción de las 13 tablas, 4 vistas, índices, restricciones CHECK, trazabilidad al DDL (`schema.sql`) y catálogo de las 7 pruebas obligatorias de backend. | 1.ª Dev (Puntos 4, 5, 8, 9); 2.ª Dev (Puntos 2, 4, 5, 6, 7, 8, 9, 11, 14, 15). |

---

## 🎨 Diagramas PlantUML Disponibles (Directorio `diagramas/`)

Todos los diagramas han sido generados en formato editable `.puml` organizados por tipo:

1. [`diagramas/secuencia/caso_base_secuencia.puml`](diagramas/secuencia/caso_base_secuencia.puml): Secuencia completa del caso base lineal (María y el iPhone 12).
2. [`diagramas/secuencia/escenario_sintetico_secuencia.puml`](diagramas/secuencia/escenario_sintetico_secuencia.puml): Secuencia del escenario multi-trabajo con falla nueva y rechazo parcial.
3. [`diagramas/casos_de_uso/casos_de_uso.puml`](diagramas/casos_de_uso/casos_de_uso.puml): Diagrama de casos de uso del núcleo operativo P0.
4. [`diagramas/dominio/modelo_dominio.puml`](diagramas/dominio/modelo_dominio.puml): Diagrama de clases del modelo conceptual de dominio.
5. [`diagramas/estados/estado_orden.puml`](diagramas/estados/estado_orden.puml): Máquina de estados finitos de la Orden de Trabajo.
6. [`diagramas/estados/estado_trabajo.puml`](diagramas/estados/estado_trabajo.puml): Máquina de estados técnicos del Trabajo.
7. [`diagramas/estados/estado_reserva.puml`](diagramas/estados/estado_reserva.puml): Ciclo de vida de las reservas de pañol.
8. [`diagramas/dominio/der_completo.puml`](diagramas/dominio/der_completo.puml): Diagrama Entidad-Relación (DER) de todas las tablas y claves foráneas.
9. [`diagramas/arquitectura/arquitectura_ncapas.puml`](diagramas/arquitectura/arquitectura_ncapas.puml): Diagrama de componentes y capas lógicas (Frontend, Backend, Persistencia).
10. [`diagramas/arquitectura/despliegue.puml`](diagramas/arquitectura/despliegue.puml): Diagrama de despliegue en la infraestructura cloud (Vercel, Render, Supabase).

---

## 📂 Anexos Metodológicos

- [`anexos/A-respuestas-encuesta.md`](anexos/A-respuestas-encuesta.md): Registro íntegro y anonimizado de las respuestas crudas de los talleres encuestados en campo.
