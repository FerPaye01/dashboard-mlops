---
name: Gestor de Rules del Proyecto
description: Actualiza y mantiene los archivos en .agent/rules/ incluyendo principios, comportamiento y decisiones
---

# Skill: Gestor de Rules del Proyecto

## Propósito
Mantener TODOS los archivos de reglas en `.agent/rules/` actualizados, coherentes y sincronizados.

## Archivos que Gestiona

```
.agent/rules/
├── RULES.md                        # Índice
├── instrucciones-comportamiento.md # Nomenclatura, logging, consentimiento
├── principios-simplicidad.md       # Cero ambigüedad, análisis de producto
├── principios-responsive.md        # Diseño responsive
├── decisiones-pendientes.md        # Por decidir
├── detector-tecnologias.md         # Detecta tecnologías y sugiere workflows
└── always-ask-rigorously.md        # Preguntar antes de actuar
```

---

## Triggers de Activación

### Comportamiento (instrucciones-comportamiento.md)
| Frase | Acción |
|-------|--------|
| "Nueva convención: X" | Agregar patrón |
| "Cambiar nomenclatura a X" | Actualizar sección |

### Principios (principios-simplicidad.md, principios-responsive.md)
| Frase | Acción |
|-------|--------|
| "Nuevo principio: X" | Agregar principio |
| "Regla de responsive: X" | Agregar a responsive |

### Decisiones (decisiones-pendientes.md)
| Frase | Acción |
|-------|--------|
| "Decidimos usar X" | Marcar decisión como tomada |
| "Pendiente: X" | Agregar nueva decisión |

---

## Proceso de Actualización

1. Detectar trigger en mensaje del usuario
2. Identificar archivo a modificar
3. Proponer cambio al usuario
4. Aplicar si aprueba
5. Verificar coherencia con otros archivos
6. Confirmar con log

---

## Verificación de Coherencia

Después de cada cambio verificar:
- [ ] No hay duplicación entre archivos
- [ ] Todos los archivos tienen `trigger: always_on`
- [ ] RULES.md refleja todos los archivos existentes
- [ ] Formato consistente (tablas, listas)

---

## Logs

Prefijo: `gestor-rules:`
```
LOG_INFO: "gestor-rules: Actualizando [archivo]"
LOG_INFO: "gestor-rules: Tecnología [X] registrada en stack"
LOG_INFO: "gestor-rules: Coherencia verificada"
LOG_WARN: "gestor-rules: Posible duplicación detectada"
```

---

## NO Gestiona

- Rules de skills individuales → Responsabilidad de `monitor-skills`
- Archivos fuera de `.agent/rules/`
