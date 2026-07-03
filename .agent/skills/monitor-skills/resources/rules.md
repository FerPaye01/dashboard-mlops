# Rules: monitor-skills

Reglas específicas para el skill de monitoreo de skills.

---

## Responsabilidades

1. **Validar estructura** de cada skill
2. **Actualizar skills** cuando hay mejoras
3. **Gestionar rules** específicas de cada skill
4. **Mantener changelog** actualizado

## Archivos que Gestiona

Por cada skill:
```
skill-name/
├── SKILL.md              # Puede actualizar
└── resources/
    ├── rules.md          # Puede actualizar
    └── changelog.md      # DEBE actualizar
```

## Checklist de Validación

Para cada skill verificar:
- [ ] SKILL.md tiene frontmatter (name, description)
- [ ] examples/ tiene al menos 1 archivo
- [ ] resources/rules.md existe
- [ ] Logs tienen prefijo correcto

## Changelog

Mantener `resources/changelog.md` con formato:
```markdown
## [FECHA]

### Nuevos
- **skill**: descripción

### Actualizados
- **skill**: cambio
```

## Logs del Skill

Prefijo: `monitor-skills:`
```
LOG_INFO: "monitor-skills: [mensaje]"
```

## Coordinación con gestor-rules

- `gestor-rules` → Rules GENERALES del proyecto
- `monitor-skills` → Rules ESPECÍFICAS de cada skill

NO modificar archivos en `.agent/rules/` (responsabilidad de gestor-rules)
