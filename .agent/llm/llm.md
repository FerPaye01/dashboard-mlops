# Mapa de Navegación del LLM (llm.md)

Archivo índice principal para agentes y LLMs. Contiene la topografía del proyecto,
rutas absolutas del sistema y contexto operativo.

> ⚠️ **Actualización obligatoria**: Este archivo debe actualizarse tras cualquier
> cambio estructural (nuevos módulos, rutas, agentes o configuraciones relevantes).

---

## 📂 Mapa Físico del Proyecto

```text
/data/proyectos/proyecto_de_proyectos/
│
├── .agent/                               # Configuración del agente Antigravity
│   ├── agents/
│   │   ├── .agent.architecture           # Arquitectura, stack y convenciones
│   ├── llm/
│   │   └── llm.md                    # Este archivo — mapa de navegación
│   ├── perfil/                           # Perfil técnico y bitácoras del usuario
│   │   ├── perfil.md                     # Niveles de expertise y calibración
│   │   ├── razonamiento.md               # Bitácora de tareas y decisiones resueltas
│   │   └── estrategias.md                # Explicaciones simplificadas (Feynman)
│   ├── rules/                            # Reglas operativas (always_on)
│   │   ├── RULES.md
│   │   ├── 0-AUDITORIA-OBLIGATORIA.md
│   │   ├── instrucciones-comportamiento.md
│   │   ├── principios-simplicidad.md
│   │   ├── principios-responsive.md
│   │   ├── decisiones-pendientes.md
│   │   ├── deudas-tecnicas.md
│   │   └── detector-tecnologias.md
│   ├── skills/                           # Skills especializados
│   │   ├── creador-skills/
│   │   ├── formulacion-preguntas/
│   │   ├── gestor-rules/
│   │   ├── monitor-skills/
│   │   ├── novice-errors/
│   │   └── pensamiento-critico/
│   └── workflows/                        # Workflows slash-command
│       ├── iniciar-proyecto.md
│       ├── alinear-contexto.md
│       ├── agregar-componente.md
│       ├── crear-skill-conocimiento.md
│       ├── crear-skill-conocimiento-documentado.md
│       ├── actualizar-skill-conocimiento.md
│       └── actualizar-skill-conocimiento-documentado.md
│
├── .analisis/                            # Documentos de análisis y diseño del proyecto
│   ├── ARCHITECTURE_DESIGN.md            # Especificación de arquitectura y diseño
│   ├── PROMPT_ORQUESTADOR_DISENO.md      # System prompt del arquitecto de software
│   ├── REQUIREMENTS_SPEC.md              # Especificación de requerimientos
│   ├── SPRINT_ROADMAP.md                 # Hoja de ruta y plan de sprints
│   └── TEST_ACCEPTANCE.md               # Plan de pruebas de aceptación (UAT)
│
└── README.md                             # Descripción general del proyecto
```

---

## 🗺️ Enlaces Absolutos del Sistema

### Configuración del Agente (.agent/)
- **Arquitectura y Stack**: [.agent.architecture](file:///data/proyectos/proyecto_de_proyectos/.agent/agents/.agent.architecture)
- **Reglas Operativas**: [RULES.md](file:///data/proyectos/proyecto_de_proyectos/.agent/rules/RULES.md)
- **Mapa de Navegación**: [llm.md](file:///data/proyectos/proyecto_de_proyectos/.agent/llm/llm.md)
- **Perfil Técnico**: [perfil.md](file:///data/proyectos/proyecto_de_proyectos/.agent/perfil/perfil.md)
- **Bitácora de Razonamiento**: [razonamiento.md](file:///data/proyectos/proyecto_de_proyectos/.agent/perfil/razonamiento.md)
- **Feynman y Estrategias**: [estrategias.md](file:///data/proyectos/proyecto_de_proyectos/.agent/perfil/estrategias.md)

### Documentos de Análisis (.analisis/)
- [ARCHITECTURE_DESIGN.md](file:///data/proyectos/proyecto_de_proyectos/.analisis/ARCHITECTURE_DESIGN.md) — Arquitectura y diseño del sistema
- [PROMPT_ORQUESTADOR_DISENO.md](file:///data/proyectos/proyecto_de_proyectos/.analisis/PROMPT_ORQUESTADOR_DISENO.md) — System prompt del arquitecto
- [REQUIREMENTS_SPEC.md](file:///data/proyectos/proyecto_de_proyectos/.analisis/REQUIREMENTS_SPEC.md) — Especificación de requerimientos
- [SPRINT_ROADMAP.md](file:///data/proyectos/proyecto_de_proyectos/.analisis/SPRINT_ROADMAP.md) — Hoja de ruta y sprints
- [TEST_ACCEPTANCE.md](file:///data/proyectos/proyecto_de_proyectos/.analisis/TEST_ACCEPTANCE.md) — Plan de pruebas UAT

### Módulos del Proyecto
> Agregar rutas absolutas a medida que se creen módulos del proyecto.

---

## 🧠 Contexto del Proyecto

- **Propósito**: [Qué problema resuelve el proyecto]
- **Stack base**: [Tecnologías principales — ver `.agent.architecture`]
- **Filosofía**: [Principios clave de diseño]
- **Estado actual**: [En definición / En desarrollo / Producción]
- **Objetivos de negocio** : [Còmo entrega valor el proyecto para resolver el problema]
---

## 🤖 Selección de Agente Adecuado

Antes de iniciar cualquier tarea, identificar el agente más adecuado según el dominio técnico.
Si no hay agente específico, el agente principal asume la tarea.

| Dominio técnico | Agente a usar |
|----------------|---------------|
| [Dominio, ej: Frontend] | [Agente, ej: `angular_agent`] |
| [Dominio, ej: Backend Python] | [Agente, ej: `fastapi_agent`] |

> Consultar `.agent/agents/.agent.architecture` para ver el listado completo de agentes del proyecto.
