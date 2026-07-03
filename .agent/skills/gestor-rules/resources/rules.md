# Rules: gestor-rules

Reglas específicas para el skill de gestión de rules.

---

## Archivos que Gestiona

Todos los archivos en `.agent/rules/`:
- RULES.md (índice)
- instrucciones-comportamiento.md
- principios-simplicidad.md
- principios-responsive.md
- decisiones-pendientes.md
- detector-tecnologias.md
- always-ask-rigorously.md

---

## Operaciones por Archivo

| Archivo | Operaciones |
|---------|-------------|
| instrucciones-comportamiento | Agregar convenciones, nomenclatura, logging |
| principios-simplicidad | Agregar principios de código, edge cases |
| principios-responsive | Agregar reglas responsive |
| decisiones-pendientes | Registrar/resolver decisiones |

---

## Nota sobre Stack Tecnológico

El stack tecnológico **no vive en `.agent/rules/`**. Está definido en `.agent/agents/.agent.architecture`. El gestor-rules no lo gestiona.

---

## Checklist de Coherencia

Verificar después de cada cambio:
- [ ] Todos los archivos tienen `trigger: always_on`
- [ ] No hay información duplicada entre archivos
- [ ] RULES.md lista todos los archivos existentes
- [ ] Formato de tablas y listas es consistente

---

## Logs

Prefijo: `gestor-rules:`

---

## NO Gestiona

- Rules de skills → Responsabilidad de `monitor-skills`
- Archivos fuera de `.agent/rules/`
