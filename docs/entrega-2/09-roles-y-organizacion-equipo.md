# 09 — Organización del Equipo, Roles y Plan de Trabajo

## 1. Integrantes del Equipo

- **Colque Gutiérrez, Brian**
- **Gutiérrez, David**
- **Iacono, Federico**

Carrera: Tecnicatura Universitaria en Programación (Virtual) — UTN Facultad Regional La Plata.  
Materia: Trabajo Final Integrador (TFI).

---

## 2. Asignación de Roles y Responsabilidades Técnicas

Para asegurar una ejecución eficiente, evitar cuellos de botella y garantizar que los tres integrantes participen activamente en la construcción y defensa técnica del proyecto, se delimitan las responsabilidades principales:

| Integrante | Rol Principal | Responsabilidades Clave |
|---|---|---|
| **Federico Iacono** | **Líder de Arquitectura Backend y Persistencia** | • Modelado relacional DDL/DML y migraciones en PostgreSQL.<br>• Implementación de Services y Repositories en FastAPI.<br>• Lógica transaccional de reservas y bloqueo pesimista (`FOR UPDATE`).<br>• Configuración de la base de datos en Supabase. |
| **David Gutiérrez** | **Líder de Frontend y Experiencia de Usuario (UI/UX)** | • Desarrollo de la SPA en React 18 + TypeScript con Vite.<br>• Implementación de componentes con Tailwind CSS y Zustand.<br>• Integración con la API REST mediante TanStack Query.<br>• Diseño responsivo y flujo del botón "Copiar Mensaje" (WhatsApp). |
| **Brian Gutiérrez Colque** | **Líder de Integración, Calidad (QA) y Despliegue** | • Diseño y ejecución de la suite de tests en pytest (pruebas obligatorias).<br>• Validación del recorrido vertical ejecutable y endpoints REST.<br>• Configuración de entornos de despliegue en Render y Vercel.<br>• Auditoría de consistencia entre documentación, reglas de negocio y código. |

---

## 3. Matriz de Responsabilidad RACI

```text
R = Responsable de ejecutar la tarea (Responsible)
A = Aprobador final / Responsable de la entrega (Accountable)
C = Consultado para definir criterios (Consulted)
I = Informado sobre avances y cambios (Informed)
```

| Componente / Entregable | Federico | David | Brian |
|---|:---:|:---:|:---:|
| **Diseño y Ajuste de Esquema SQL (`schema.sql`)** | **R / A** | C | C |
| **Endpoints REST y Schemas Pydantic en FastAPI** | **R** | C | **A** |
| **Pruebas Obligatorias de Backend (pytest)** | C | I | **R / A** |
| **Desarrollo de Vistas y Componentes React** | C | **R / A** | C |
| **Consumo de API y Manejo de Estado en Frontend** | C | **R** | **A** |
| **Despliegue Cloud (Render, Vercel, Supabase)** | C | C | **R / A** |
| **Documentación Técnica y Validación con Tutor** | **R** | **R** | **R / A** |

---

## 4. Metodología de Trabajo y Flujo de Git

### 4.1. Marco Ágil (Kanban)
El proyecto se coordina a través de un tablero en **Trello** estructurado en cuatro columnas operativas:
1. `Backlog / P0`: Historias de usuario y tareas técnicas priorizadas para el MVP.
2. `En Proceso (WIP)`: Tareas en desarrollo activo (límite: máximo 1 tarea simultánea por integrante).
3. `En Revisión / Testing`: Funcionalidades con pull request abierto y pruebas locales pasando.
4. `Completado`: Código fusionado en la rama de integración y verificado.

### 4.2. Estrategia de Ramas en Git (GitFlow Simplificado)
Para evitar conflictos y preservar la estabilidad de la rama principal:

```text
main (producción / entregables formales al tutor)
  ▲
  │ (pull request formal al cerrar hito)
dev (rama de integración continua del equipo)
  ▲
  ├── feature/vertical-backend-ordenes
  ├── feature/frontend-tablero-ordenes
  └── test/reserva-concurrente-pytest
```

- **Regla de oro:** Nadie comitea directamente a `main`.
- Toda nueva funcionalidad se desarrolla en una rama `feature/<nombre-descriptivo>` creada a partir de `dev`.
- La fusión hacia `dev` requiere verificación de que la suite de pruebas automatizadas pasa en verde (`pytest`).

---

## 5. Plan de Acción Inmediato: Hacia el Vertical Ejecutable

Atendiendo a la instrucción explícita del tutor en la 2.ª Devolución (*"El próximo avance debería incluir como mínimo un vertical ejecutable: cliente → equipo → orden → diagnóstico → trabajo/presupuesto → aprobación → reserva de repuesto → reparación → listo → pago → entrega"*), el equipo acuerda la siguiente secuencia de trabajo:

```text
Semana 1 (Actual):
  [1] Configuración de .env local con conexión a Supabase por integrante.
  [2] Implementación de Modelos SQLAlchemy, Repositorios y Servicios del núcleo en backend/.
  [3] Ejecución de las 3 pruebas obligatorias de backend:
      - Bloqueo de entrega con saldo pendiente.
      - Monto de pago estrictamente mayor a cero.
      - Reserva concurrente con stock = 1 y SELECT FOR UPDATE.

Semana 2:
  [4] Implementación de Routers REST en FastAPI para el flujo completo.
  [5] Montaje de la estructura base de React + Vite en frontend/.
  [6] Integración del primer recorrido visual en pantalla.

Semana 3:
  [7] Escenario de falla adicional (trabajo nuevo concurrente).
  [8] Componente de copiado de mensaje para WhatsApp.
  [9] Despliegue en Render/Vercel y reporte de conformidad a Oscar por el campus.
```
