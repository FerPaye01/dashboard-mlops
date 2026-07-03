---
description: Actualiza un skill existente buscando documentación online
---

# Workflow: Actualizar Skill desde Documentación Online

Actualiza un skill existente buscando nueva documentación oficial de la tecnología.

---

## Uso

```
/actualizar-skill-conocimiento-documentado [nombre-skill]
```
### Ejemplos:
- `/actualizar-skill-conocimiento-documentado tailwind`
- `/actualizar-skill-conocimiento-documentado prisma`
- `/actualizar-skill-conocimiento-documentado zustand`

---

## Pasos

### 1. Validar Entrada
- Verificar que el skill EXISTA en `.agent/skills/[nombre-skill]/`
- Leer knowledge-source.md existente para saber fuente original

### 2. Buscar Documentación Actualizada
Usar `search_web` para encontrar actualizaciones:
```
search_web("[nombre-tecnología] documentation changelog updates latest")
```

### 3. Obtener Contenido Nuevo e Investigación Profunda
- Usar `read_url_content` para extraer el contenido de las URLs encontradas.
- Obligatoriamente navegar por los enlaces técnicos relacionados dentro del contenido base buscando nuevos endpoints, esquemas JSON, variables de entorno o configuraciones avanzadas.
- **REGLA ESPECIAL DE RESPETO AL CÓDIGO**: Si se encuentra código en las páginas, blogs, videos, repositorios, chats o cualquier fuente, DEBE COPIARSE EXACTAMENTE TAL CUAL, SIN VARIACIONES, simplificaciones ni adaptaciones.
- **ARMONÍA CON EL STACK**: Validar que la tecnología o los códigos encontrados estén en ARMONÍA con la arquitectura y stack definidos en `.agent/agents/.agent.architecture`.

### 4. Comparar con Conocimiento Existente
- Leer `resources/knowledge-source.md` actual
- Identificar diferencias y nuevo contenido
- Determinar qué es información nueva
- Confirmar si la actualización mantiene la coherencia con el proyecto global.

### 5. Guardar Actualización
Crear archivo con la documentación nueva:
```
.agent/skills/[nombre-skill]/resources/knowledge-update-[fecha].md
```

Incluir:
- URL de origen
- Fecha de captura
- Diferencias con versión anterior
- Contenido nuevo

### 6. Consultar Skill `monitor-skills`
Leer `.agent/skills/monitor-skills/SKILL.md` y seguir proceso de actualización:

1. Leer SKILL.md actual
2. Integrar nuevo conocimiento
3. Actualizar instrucciones si aplica
4. Agregar nuevos ejemplos si hay features nuevas

### 7. Actualizar SKILL.md
Modificar el archivo principal con:
- Nuevas instrucciones
- Ejemplos actualizados
- Mejores prácticas nuevas
- Referencia a fuente actualizada

### 8. Actualizar Changelog
Agregar entrada en `resources/changelog.md`:
```markdown
## [Fecha]
- Actualizado desde: [URL]
- Cambios detectados: [resumen]
```

### 9. Validación con el Usuario (Opción C)
Usar el skill `formulacion-preguntas` para validar con el usuario:
- Mostrar el resumen de los cambios.
- Validar si la nueva actualización cubre lo esperado.
- Consultar posibles escenarios de uso o falencias que la actualización pueda presentar.

### 10. Confirmar al Usuario
Mostrar:
- URL de documentación usada
- Cambios detectados
- Secciones actualizadas
- Nuevo conocimiento agregado

---

## Logs
- LOG_INFO: "actualizar-skill-conocimiento-documentado: Buscando actualizaciones..."
- LOG_INFO: "actualizar-skill-conocimiento-documentado: Documentación encontrada en [URL]"
- LOG_INFO: "actualizar-skill-conocimiento-documentado: Comparando con conocimiento existente"
- LOG_INFO: "actualizar-skill-conocimiento-documentado: Actualizando skill usando monitor-skills"
- LOG_INFO: "actualizar-skill-conocimiento-documentado: Skill [nombre] actualizado"
- LOG_WARN: "actualizar-skill-conocimiento-documentado: No se encontraron cambios significativos"