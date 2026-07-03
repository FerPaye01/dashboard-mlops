# Ejemplo: Revisar un Skill Existente

## Contexto
El usuario quiere verificar que un skill tiene estructura completa y funciona correctamente.

## Entrada del Usuario
```
Revisa el skill creador-skills
```

## Proceso
1. Ubicar carpeta `.agent/skills/creador-skills/`
2. Verificar existencia de SKILL.md
3. Validar frontmatter (name, description)
4. Verificar carpetas: examples/, resources/, scripts/
5. Revisar que haya al menos un ejemplo
6. Reportar estado

## Salida Esperada
```
📊 Revisión de skill: creador-skills

✅ SKILL.md - Presente y válido
✅ examples/ - 1 ejemplo encontrado
✅ resources/ - Presente
✅ scripts/ - Presente

Estado: COMPLETO
Última revisión: 2026-01-29
```

## Log
```
LOG_INFO: monitor-skills: Skill 'creador-skills' validado correctamente
```
