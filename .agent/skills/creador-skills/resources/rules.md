# Rules: creador-skills

Reglas específicas para el skill de creación de skills.

---

## Estructura Obligatoria

Todo skill creado DEBE tener:
```
skill-name/
├── SKILL.md          # OBLIGATORIO
├── examples/         # OBLIGATORIO - mínimo 1 ejemplo
├── resources/        # OBLIGATORIO - puede tener .gitkeep
└── scripts/          # OBLIGATORIO - puede tener .gitkeep
```

## Formato SKILL.md

- Frontmatter con `name` y `description`
- Sección "Propósito"
- Sección "Cuándo Activarse"
- Sección "Logs" con formato consistente

## Logs del Skill

Prefijo: `creador-skills:`
```
LOG_INFO: "creador-skills: [mensaje]"
```

## Validación

Antes de marcar skill como creado:
- [ ] SKILL.md tiene frontmatter válido
- [ ] examples/ tiene al menos 1 archivo
- [ ] resources/ existe
- [ ] scripts/ existe
