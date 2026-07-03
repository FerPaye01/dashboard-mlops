---
name: Monitor de Skills
description: Monitorea, actualiza y mejora los skills existentes del proyecto
---

# Skill: Monitor de Skills

## Propósito
Mantener los skills del proyecto actualizados, detectar bugs o mejoras necesarias, y evolucionar los skills conforme el proyecto crece. Este skill actúa como "meta-skill" que supervisa a los demás.

## Cuándo Activarse

### Triggers Automáticos
1. Usuario reporta un problema con un skill
2. Se detecta un patrón repetido no cubierto por skills existentes
3. Usuario pide revisar o mejorar un skill
4. Actualización de documentación fuente de un skill

### Triggers Manuales
- "Revisa el skill [nombre]"
- "Actualiza los skills"
- "¿Qué skills tenemos?"
- "El skill [nombre] no funciona bien"

## Funciones Principales

### 1. Inventario de Skills
Listar todos los skills disponibles con su estado:

```markdown
| Skill | Estado | Última Revisión |
|-------|--------|-----------------|
| creador-skills | ✅ Activo | 2026-01-29 |
| gestor-rules | ✅ Activo | 2026-01-29 |
| monitor-stack | ✅ Activo | 2026-01-29 |
| monitor-skills | ✅ Activo | 2026-01-29 |
```

### 2. Validación de Estructura
Verificar que cada skill tenga estructura completa:

```
[skill]/
├── SKILL.md          ✅ Obligatorio
├── examples/         ✅ Obligatorio (al menos 1 ejemplo)
├── resources/        ⚪ Opcional
└── scripts/          ⚪ Opcional
```

### 3. Detección de Mejoras
Identificar oportunidades de mejora:
- Skills con instrucciones incompletas
- Ejemplos faltantes o desactualizados
- Scripts que podrían automatizar tareas repetitivas
- Patrones que podrían convertirse en nuevos skills

### 4. Actualización de Skills
Proceso para actualizar un skill existente:

1. Leer SKILL.md actual
2. Identificar sección a modificar
3. Proponer cambio al usuario
4. Aplicar cambio si el usuario aprueba
5. Actualizar fecha de revisión
6. Verificar que sigue funcionando

## Checklist de Revisión

Para cada skill verificar:

- [ ] SKILL.md tiene frontmatter válido (name, description)
- [ ] Propósito está claramente definido
- [ ] Triggers de activación están documentados
- [ ] Instrucciones son ejecutables paso a paso
- [ ] Existe evidencia de **profundidad técnica** (código, JSON, endpoints) y no solo teoría de alto nivel.
- [ ] Hay al menos un ejemplo técnico y detallado en examples/
- [ ] Existe sección "Solución de Problemas" (opcional pero recomendada)
- [ ] Logs están definidos con formato consistente

## Comandos del Usuario

| Comando | Acción |
|---------|--------|
| "Lista los skills" | Mostrar inventario |
| "Revisa skill [nombre]" | Validar estructura y contenido |
| "Mejora skill [nombre]" | Proponer mejoras |
| "El skill [nombre] falla" | Diagnosticar y corregir |
| "Actualiza todos los skills" | Revisión completa |

## Registro de Cambios

Mantener un log en `resources/changelog.md`:

```markdown
# Changelog de Skills

## 2026-01-29
- Creado skill monitor-skills
- Actualizado creador-skills con estructura completa

## [Fecha]
- [Cambio realizado]
```

## Logs
- LOG_INFO: "monitor-skills: Revisando skill [nombre]..."
- LOG_INFO: "monitor-skills: Skill [nombre] validado correctamente"
- LOG_WARN: "monitor-skills: Skill [nombre] tiene estructura incompleta"
- LOG_ERROR: "monitor-skills: Skill [nombre] tiene errores críticos"

## Portabilidad (GitHub Template)

Este skill y los demás pueden usarse como template para nuevos proyectos:

1. Clonar repositorio
2. Eliminar código específico del proyecto
3. Mantener carpeta `.agent/` intacta
4. Los skills estarán listos para usar

### Archivos Portables
```
.agent/
├── rules/           # Adaptar al nuevo proyecto
├── workflows/       # Reutilizables
└── skills/          # 100% reutilizables
    ├── creador-skills/
    ├── gestor-rules/
    ├── monitor-skills/
    └── monitor-stack/
```
