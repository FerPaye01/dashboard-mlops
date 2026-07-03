---
description: Crea un skill nuevo a partir de documentación proporcionada por el usuario
---

# Workflow: Crear Skill desde Conocimiento

Crea un skill nuevo utilizando documentación que el usuario proporciona directamente.

---

## Uso

```
/crear-skill-conocimiento [nombre-skill] [fuente]
```

### Ejemplos:
- `/crear-skill-conocimiento tailwind ./docs/tailwind-guide.pdf`
- `/crear-skill-conocimiento react https://react.dev/learn`
- `/crear-skill-conocimiento vue "Texto pegado con la documentación..."`

---

## Pasos

### 1. Validar Entrada
- Verificar que el nombre del skill no exista en `.agent/skills/`
- Verificar que la fuente sea accesible (archivo existe, URL responde, texto no vacío)

### 2. Procesar Fuente
- **Archivo (PDF/TXT/MD):** Leer contenido del archivo
- **URL:** Usar `read_url_content` para obtener el contenido
- **Texto:** Usar el texto directamente

### 3. Guardar Conocimiento
Crear archivo de conocimiento en la estructura del skill:
```
.agent/skills/[nombre-skill]/resources/knowledge-source.md
```

### 4. Consultar Skill `creador-skills`
Leer el archivo `.agent/skills/creador-skills/SKILL.md` y seguir sus instrucciones para crear la estructura completa:

```
.agent/skills/[nombre-skill]/
├── SKILL.md              # Instrucciones principales
├── examples/             # Al menos un ejemplo
│   └── ejemplo_basico.md
├── resources/            # Fuente de conocimiento
│   ├── knowledge-source.md
│   └── rules.md          # Reglas específicas del skill
└── scripts/
    └── .gitkeep
```

### 5. Generar SKILL.md
Crear el archivo principal con:
- Frontmatter (name, description)
- Propósito extraído de la documentación
- Instrucciones de uso
- Ejemplos de código si aplica
- Mejores prácticas detectadas

### 6. Confirmar al Usuario
Mostrar:
- Ruta del skill creado
- Resumen del contenido
- Cómo usar el nuevo skill

---

## Logs
- LOG_INFO: "crear-skill-conocimiento: Procesando fuente..."
- LOG_INFO: "crear-skill-conocimiento: Guardando conocimiento en resources/"
- LOG_INFO: "crear-skill-conocimiento: Creando estructura usando creador-skills"
- LOG_INFO: "crear-skill-conocimiento: Skill [nombre] creado en .agent/skills/[nombre]/"
