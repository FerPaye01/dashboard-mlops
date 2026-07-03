---
name: Formulación de Preguntas
description: Estándar para la toma de requerimientos, clarificación de dudas y validación de flujos mediante hipótesis estructuradas por dominio de agente y diagramas visuales.
---

# Skill: Formulación de Preguntas (Hipótesis & Clarificación)

## Propósito
Asegurar que ninguna implementación compleja o resolución de problemas comience sin haber validado exhaustivamente los requerimientos, visualizado la arquitectura y planteado hipótesis claras vinculadas a los agentes especializados de la arquitectura.

## Cuándo Usar
- **Inicio de Proyecto (OBLIGATORIO)**: Para capturar los datos que alimentan al orquestador de diseño. Se deben preguntar y documentar bajo estos tres campos exactos:
  1. **Problema a Resolver**: Descripción detallada del problema de negocio/técnico.
  2. **Stack Tecnológico Inicial**: Lenguajes, frameworks y herramientas propuestos.
  3. **Restricciones de Infraestructura/Negocio**: Presupuesto, hardware disponible, plazos o limitantes.
- **Antes de escribir código complejo**: (ej. lógica de negocio core, optimizaciones, integraciones).
- **Resolución de Bugs/Incidencias**: Para diagnosticar problemas planteando hipótesis claras en vez de probar soluciones a ciegas.
- **Cuando el requerimiento sea ambiguo**: (ej. "mejora el rendimiento de la base de datos").

---

## Protocolo de Formulación (Paso a Paso)

### 1. Identificación del Dominio (Agente Especializado)
Antes de proponer nada, identificar qué agentes de la arquitectura ([.agent.architecture](file:///data/proyectos/proyecto_de_proyectos/.agent/agents/.agent.architecture)) son responsables del problema.
*Ejemplo: `fastapi_agent` para lógica de negocio, `vector_db_agent` para búsquedas semánticas, `ui_agent` para presentación.*

### 2. Visualización Obligatoria (Mermaid)
Incluir siempre un diagrama para confirmar el entendimiento mutuo.
- Usar diagramas de flujo (`flowchart TD`) para lógica o procesos.
- Usar diagramas de secuencia (`sequenceDiagram`) para interacciones entre componentes/agentes.

### 3. Calibrar y Plantear Hipótesis (Mínimo 2 opciones)
Antes de escribir las hipótesis, **leer obligatoriamente el archivo personal [perfil.md](file:///data/proyectos/proyecto_de_proyectos/.agent/perfil/perfil.md)** del usuario:
- Identificar el nivel de expertise en la tecnología implicada.
- **Calibrar la Verificación**:
  - Si el nivel es **Principiante / Aprendiendo**, la sección *Verificación* debe explicarse paso a paso con el comando exacto o log a buscar.
  - Si el nivel es **Avanzado / Domina**, la sección *Verificación* puede ser de alta abstracción (ej. "validar mediante test de integración").

Cada hipótesis debe seguir estrictamente este formato:

```markdown
#### Hipótesis [N] — Dominio: [Agente Especializado, ej: fastapi_agent]
- **Creemos que**: [Causa sospechada del problema o justificación del diseño]
- **Si implementamos**: [Mecanismo, intervención o cambio técnico propuesto]
- **Entonces observaremos**: [Resultado esperado, medible o comportamiento final]
- **Verificación**: [Método de prueba adaptado a mi nivel de expertise en perfil.md]
- **Confianza**: Alta / Media / Baja
```

### 4. Preguntas de Contraste / Casos Límite
Formular preguntas específicas sobre escenarios límite (edge cases) o fallos de negocio para validar la robustez de las hipótesis.

---

## Estructura de la Respuesta al Usuario

```markdown
### 1. Agentes Especializados Involucrados
- `[nombre_agente_1]`: [Motivo por el que participa]
- `[nombre_agente_2]`: [Motivo por el que participa]

### 2. Visualización del Flujo Actual vs Propuesto
[Diagrama Mermaid]

### 3. Hipótesis de Abordaje (Opciones)

#### Hipótesis A — Dominio: [Agente]
- **Creemos que**: ...
- **Si implementamos**: ...
- **Entonces observaremos**: ...
- **Verificación**: ...
- **Confianza**: ...

#### Hipótesis B — Dominio: [Agente]
- **Creemos que**: ...
- **Si implementamos**: ...
- **Entonces observaremos**: ...
- **Verificación**: ...
- **Confianza**: ...

### 4. Casos de Riesgo / Preguntas de Contraste
- ¿Qué sucede si el volumen de datos excede [X]?
- ¿Debemos considerar este caso borde en la hipótesis A?
```

## Logs
- `LOG_INFO: "formulacion-preguntas: Identificando dominios de agentes para [tópico]"`
- `LOG_INFO: "formulacion-preguntas: Formulando hipótesis de desarrollo"`
- `LOG_INFO: "formulacion-preguntas: Diagrama visual generado"`
