---
description: Actualiza un skill existente con nueva documentación proporcionada
---

# Workflow: Actualizar Skill con Conocimiento

Actualiza un skill existente utilizando nueva documentación que el usuario proporciona.

---

## Uso

```
/actualizar-skill-conocimiento [nombre-skill] [fuente]
```

### Ejemplos:
- `/actualizar-skill-conocimiento tailwind ./docs/tailwind-v4-changes.pdf`
- `/actualizar-skill-conocimiento react https://react.dev/blog/new-features`
- `/actualizar-skill-conocimiento vue "Nuevas instrucciones sobre composables..."`

---

## Pasos

### 1. Validar Entrada
- Verificar que el skill EXISTA en `.agent/skills/[nombre-skill]/`
- Verificar que la fuente sea accesible

### 2. Procesar Nueva Fuente
- **Archivo (PDF/TXT/MD):** Leer contenido del archivo
- **URL:** Usar `read_url_content` para obtener el contenido
- **Texto:** Usar el texto directamente

### 3. Actualizar Conocimiento
Agregar nuevo conocimiento a la carpeta resources/:
```
.agent/skills/[nombre-skill]/resources/knowledge-update-[fecha].md
```

Incluir metadatos:
- Fecha de actualización
- Tipo de fuente
- Resumen del nuevo conocimiento

### 4. Consultar Skill `monitor-skills`
Leer `.agent/skills/monitor-skills/SKILL.md` y seguir proceso de actualización:

1. Leer SKILL.md actual
2. Identificar secciones a modificar/agregar
3. Integrar nuevo conocimiento
4. Actualizar fecha de revisión

### 5. Actualizar SKILL.md
Modificar el archivo principal:
- Agregar nuevas instrucciones si aplica
- Actualizar ejemplos si hay cambios
- Agregar nuevas mejores prácticas
- Mantener retrocompatibilidad

### 6. Actualizar Changelog
Agregar entrada en `resources/changelog.md`:
```markdown
## [Fecha]
- Actualizado con nueva fuente: [tipo de fuente]
- Cambios: [resumen de cambios]
```

### 7. Confirmar al Usuario
Mostrar:
- Secciones actualizadas
- Nuevo conocimiento agregado
- Cambios en el SKILL.md

---

## Logs
- LOG_INFO: "actualizar-skill-conocimiento: Procesando nueva fuente..."
- LOG_INFO: "actualizar-skill-conocimiento: Guardando conocimiento actualizado"
- LOG_INFO: "actualizar-skill-conocimiento: Actualizando skill usando monitor-skills"
- LOG_INFO: "actualizar-skill-conocimiento: Skill [nombre] actualizado"
- LOG_WARN: "actualizar-skill-conocimiento: Conflicto detectado con conocimiento existente"
