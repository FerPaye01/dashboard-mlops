---
name: Creador de Skills desde Documentación
description: Genera nuevos skills de Antigravity con estructura completa a partir de documentación proporcionada
---

# Skill: Creador de Skills desde Documentación

## Propósito
Crear nuevos skills de Antigravity con estructura profesional completa, analizando documentación externa (URLs, texto, PDFs) para extraer instrucciones y mejores prácticas.

## Estructura Obligatoria de un Skill

Cada skill DEBE tener la siguiente estructura:

```
.agent/skills/[nombre-skill]/
├── SKILL.md              # Archivo principal (OBLIGATORIO)
├── examples/             # Ejemplos de uso
│   └── ejemplo_basico.md
├── resources/            # Recursos adicionales (templates, configs)
│   └── .gitkeep
└── scripts/              # Scripts helper (si aplica)
    └── .gitkeep
```

## Proceso de Creación

### 1. Análisis de Documentación Expansivo
- Leer y comprender el contenido proporcionado.
- Si el contenido tiene enlaces a documentación técnica de bajo nivel (APIs, configuración JSON, etc.), navegarlos primero (Investigación exhaustiva).
- Identificar propósito principal.
- Extraer pasos, instrucciones clave, endpoints y esquemas.
- Detectar ejemplos de código, prestando extrema atención a payloads o JSONs de configuración (no solo código de alto nivel).
- Identificar mejores prácticas y limitantes.
- Identificar logs y mensajes de error comunes.
- Extraer comandos del usuario.
- Extraer ejemplos de uso rápido
- Extraer ejemplos de uso detallados
- Extraer ejemplos de uso avanzados 
- Extraer ejemplos de uso con scripts
- Extraer ejemplos de uso con workflows
- Extraer ejemplos de uso con pipelines
- Extraer ejemplos de uso con pipelines

### 2. Generar Estructura Completa
Crear todos los archivos y carpetas:

```bash
# Estructura a crear
skill-name/
├── SKILL.md
├── examples/ejemplo_basico.md
├── resources/.gitkeep
└── scripts/.gitkeep
```

### 3. Formato del SKILL.md

```markdown
---
name: [Nombre descriptivo]
description: [Descripción de una línea]
---

# [Título del Skill]

## Propósito
[Para qué sirve este skill]

## Cuándo Usar
[Triggers y condiciones de activación]

## Instrucciones
[Pasos detallados]

## Ejemplos
Ver carpeta `examples/` para casos de uso.

## Resources
Ver carpeta `resources/` para templates y configs.

## Scripts Disponibles
Ver carpeta `scripts/` para automatizaciones.

## Solución de Problemas
[Errores comunes y cómo solucionarlos]

## Logs
- LOG_INFO: "[nombre-skill]: Mensaje"
```

### 4. Archivo examples/ejemplo_basico.md

```markdown
# Ejemplo: [Caso de Uso Básico]

## Contexto
[Cuándo usar este ejemplo]

## Entrada
[Qué proporciona el usuario]

## Proceso
[Pasos que ejecuta el skill]

## Salida Esperada
[Resultado esperado]
```

### 5. Validación Final
- [ ] SKILL.md tiene frontmatter válido (name, description)
- [ ] Carpeta examples/ existe con al menos un ejemplo
- [ ] Carpeta resources/ existe
- [ ] Carpeta scripts/ existe
- [ ] Instrucciones son claras y ejecutables

## Comandos del Usuario

| Comando | Acción |
|---------|--------|
| "Crea skill desde [URL]" | Analiza URL y crea skill |
| "Nuevo skill para [propósito]" | Crea skill desde descripción |
| "Skill basado en [texto]" | Crea skill desde texto pegado |

## Logs
- LOG_INFO: "creador-skills: Analizando documentación..."
- LOG_INFO: "creador-skills: Creando estructura en .agent/skills/[nombre]/"
- LOG_INFO: "creador-skills: Skill '[nombre]' creado exitosamente"
- LOG_WARN: "creador-skills: Documentación incompleta, skill creado con datos parciales"
