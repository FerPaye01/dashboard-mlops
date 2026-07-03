---
description: Iniciar un nuevo proyecto — captura contexto, activa el orquestador de diseño y genera la documentación técnica inicial
---

# Flujo: Iniciar Proyecto

## Propósito
Capturar el contexto del proyecto, activar el `PROMPT_ORQUESTADOR_DISENO` como motor de análisis y generar los 4 artefactos técnicos iniciales en `.analisis/` de forma consistente y trazable.

---

## Pasos

### 1. Sesión de Captura de Contexto (OBLIGATORIO)
Ejecutar el skill `formulacion-preguntas` para obtener las 3 entradas que necesita el orquestador:

- **Problema a Resolver**: ¿Qué necesidad de negocio o técnica resuelve exactamente?
- **Stack Tecnológico Inicial**: ¿Qué lenguajes, frameworks y herramientas se proponen?
- **Restricciones de Infraestructura / Negocio**: ¿Hay presupuesto, hardware disponible, plazos o limitaciones?

> No avanzar al siguiente paso hasta tener las 3 respuestas explícitas del usuario.

---

### 2. Activar el Orquestador de Diseño
Leer el archivo [PROMPT_ORQUESTADOR_DISENO.md](file:///data/proyectos/proyecto_de_proyectos/.analisis/PROMPT_ORQUESTADOR_DISENO.md) y usarlo como instrucción maestra.

Completar la sección **"5. Entrada del Usuario"** con lo capturado en el Paso 1:

```
Problema a Resolver: [respuesta del usuario]
Stack Tecnológico Inicial: [respuesta del usuario]
Restricciones de Infraestructura/Negocio: [respuesta del usuario]
```

---

### 3. Generación en Cascada de Artefactos `.analisis/`
Producir los 4 archivos en este orden estricto, respetando la trazabilidad definida en el orquestador:

| Orden | Archivo | Contenido |
|-------|---------|-----------|
| 1° | `REQUIREMENTS_SPEC.md` | RF con verbos imperativos + RNF cuantificables |
| 2° | `ARCHITECTURE_DESIGN.md` | Topología, diagrama Mermaid, ADR, SRP de módulos |
| 3° | `SPRINT_ROADMAP.md` | 4 sprints con entregables tangibles y ruta crítica |
| 4° | `TEST_ACCEPTANCE.md` | Escenarios UAT, mecanismos de defensa (DLQ, Rate Limits) |

> ⚠️ Validar consistencia antes de finalizar: un cambio en `REQUIREMENTS_SPEC` debe reflejarse en `TEST_ACCEPTANCE`.

---

### 4. Actualizar `.agent.architecture`
Con el stack confirmado en el Paso 1, completar las secciones correspondientes en [.agent.architecture](file:///data/proyectos/proyecto_de_proyectos/.agent/agents/.agent.architecture):
- Stack Tecnológico Base
- Flujo de Componentes y Datos
- Agentes Especializados Disponibles (si aplica)
- Principios Arquitectónicos

---

### 5. Actualizar `llm.md`
Actualizar el mapa de navegación en [llm.md](file:///data/proyectos/proyecto_de_proyectos/.agent/agents/llm/llm.md):
- Completar sección **Contexto del Proyecto**
- Agregar rutas absolutas de los módulos reales creados
- Completar tabla de **Selección de Agente Adecuado** si se definieron agentes

---

### 6. Registrar Decisiones Clave
Documentar en [decisiones-pendientes.md](file:///data/proyectos/proyecto_de_proyectos/.agent/rules/decisiones-pendientes.md) cualquier decisión técnica que quedó pendiente o fue tomada durante esta sesión.

---

## Logs
- `LOG_INFO: "iniciar-proyecto: Contexto capturado — problema, stack y restricciones definidos"`
- `LOG_INFO: "iniciar-proyecto: Orquestador activado — generando artefactos en .analisis/"`
- `LOG_INFO: "iniciar-proyecto: [archivo].md generado"`
- `LOG_INFO: "iniciar-proyecto: .agent.architecture y llm.md actualizados"`
- `LOG_WARN: "iniciar-proyecto: Inconsistencia detectada entre artefactos — revisar antes de continuar"`
