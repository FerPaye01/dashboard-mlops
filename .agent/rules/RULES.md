---
trigger: always_on
---

# 📚 Índice de Reglas del Proyecto

Este archivo sirve como índice. Las reglas principales están en `.agent/rules/`.

---

## Archivos de Rules

| Archivo | Trigger | Descripción |
|---------|---------|-------------|
| [0-AUDITORIA-OBLIGATORIA.md](0-AUDITORIA-OBLIGATORIA.md) | `always_on` | 🛡️ Regla primordial de auditoría contextual y seguridad |
| [instrucciones-comportamiento.md](instrucciones-comportamiento.md) | `always_on` | 📜 Nomenclatura snake_Mayus/español, logging por capa, consentimiento de archivos |
| [principios-simplicidad.md](principios-simplicidad.md) | `always_on` | 🔧 Reglas de código + cero ambigüedad + análisis de producto |
| [principios-responsive.md](principios-responsive.md) | `always_on` | 📱 Diseño responsive |
| [decisiones-pendientes.md](decisiones-pendientes.md) | `always_on` | 📋 Directriz de formato para el registro de decisiones técnicas |
| [deudas-tecnicas.md](deudas-tecnicas.md) | `always_on` | 🔧 Directriz de formato para el registro de deuda técnica |
| [detector-tecnologias.md](detector-tecnologias.md) | `always_on` | 🔍 Detecta tecnologías y sugiere workflows |

---

## Rules por Skill

Cada skill tiene sus reglas específicas:

| Skill | Rules |
|-------|-------|
| creador-skills | `resources/rules.md` |
| gestor-rules | `resources/rules.md` |
| monitor-skills | `resources/rules.md` |

---

## Cómo Funcionan los Triggers

- `trigger: always_on` → Se aplica siempre en cada interacción
- Sin trigger → Se aplica cuando es relevante al contexto
