---
description: Crea un skill nuevo buscando documentación online automáticamente
---

# Workflow: Crear Skill desde Documentación Online

Crea un skill nuevo buscando la documentación oficial de la tecnología en internet.

---

## Uso

```
/crear-skill-conocimiento-documentado [nombre-skill]
```

### Ejemplos:
- `/crear-skill-conocimiento-documentado tailwind`
- `/crear-skill-conocimiento-documentado prisma`
- `/crear-skill-conocimiento-documentado zustand`

---

## Pasos

### 1. Validar Entrada
- Verificar que el nombre del skill no exista en `.agent/skills/`

### 2. Buscar Documentación
Usar `search_web` para encontrar documentación oficial:
```
search_web("[nombre-tecnología] official documentation getting started")
```

### 3. Obtener Contenido Base
Usar `read_url_content` para extraer el contenido de la URL encontrada.

### 4. Investigación Profunda (OBLIGATORIO)
- Analizar el contenido base en busca de enlaces hacia conceptos técnicos clave mencionados (ej. APIs, Referencias, Protocolos).
- Iterar leyendo el contenido de al menos 2 a 3 URLs adicionales usando `read_url_content`.
- Extraer ejemplos de código JSON, sintaxis específica de comandos, o descripciones de payloads que demuestren la implementación técnica real.
- **REGLA ESPECIAL DE RESPETO AL CÓDIGO**: Si se encuentra código en blogs, videos, repositorios, chats o cualquier fuente, DEBE COPIARSE EXACTAMENTE TAL CUAL, SIN VARIACIONES, simplificaciones ni adaptaciones.
- **ARMONÍA CON EL STACK**: Validar que la nueva tecnología sea armónica con la arquitectura y stack definidos en `.agent/agents/.agent.architecture`.

### 5. Guardar Conocimiento
Crear archivo con la documentación procesada:
```
.agent/skills/[nombre-skill]/resources/knowledge-source.md
```

Incluir en el archivo:
- URL de origen
- Fecha de captura
- Contenido procesado

### 6. Consultar Skill `creador-skills`
Leer `.agent/skills/creador-skills/SKILL.md` y seguir sus instrucciones para crear la estructura completa:

```
.agent/skills/[nombre-skill]/
├── SKILL.md              # Instrucciones principales
├── examples/             # Al menos un ejemplo
│   └── ejemplo_basico.md
├── resources/            # Fuente de conocimiento
│   ├── knowledge-source.md  # Documentación capturada
│   └── rules.md             # Reglas específicas
└── scripts/
    └── .gitkeep
```

### 7. Generar SKILL.md
Crear el archivo principal con:
- Frontmatter (name, description)
- Propósito extraído de la documentación
- Instrucciones de uso
- Ejemplos de código si aplica
- Mejores prácticas detectadas
- Referencia a la fuente original

### 8. Validación con el Usuario (Opción C)
Usar el skill `formulacion-preguntas` para validar con el usuario:
- Presentar la estructura generada.
- Validar si el propósito y las instrucciones cubren lo esperado.
- Consultar casos de uso extremos o limitaciones detectadas.

### 9. Confirmar al Usuario
Mostrar:
- Ruta del skill creado
- URL de la documentación usada
- Resumen del contenido
- Cómo usar el nuevo skill

---

## Logs
- LOG_INFO: "crear-skill-conocimiento-documentado: Buscando documentación de [nombre]..."
- LOG_INFO: "crear-skill-conocimiento-documentado: Documentación encontrada en [URL]"
- LOG_INFO: "crear-skill-conocimiento-documentado: Guardando conocimiento en resources/"
- LOG_INFO: "crear-skill-conocimiento-documentado: Creando estructura usando creador-skills"
- LOG_INFO: "crear-skill-conocimiento-documentado: Skill [nombre] creado"
- LOG_WARN: "crear-skill-conocimiento-documentado: No se encontró documentación oficial, usando fuentes alternativas"
