---
trigger: always_on
---

# 🔧 Directriz: Registro de Deuda Técnica

Este archivo es una **regla estática**. Define el estándar obligatorio sobre cómo el asistente
debe identificar, clasificar y documentar los compromisos de diseño o tareas pendientes.

> ⚠️ **REGLA DE REGISTRO**: Los registros de deuda técnica reales no se guardan en este archivo.
> Deben registrarse exclusivamente en la sección correspondiente de `.agent/perfil/razonamiento.md`.

---

## ⚖️ Cómo Clasificar y Registrar Deuda Técnica

Cuando se implemente una solución rápida que genere deuda, o se identifique una mejora diferida para futuros sprints, el asistente debe documentarla en `razonamiento.md` usando los siguientes bloques estruturados:

### 1. Formato para Deuda Técnica Activa

```markdown
### N. [Título de la Deuda]
- **Prioridad**: 🔴 Alta | 🟡 Media | 🟢 Baja
- **Problema**: [Descripción clara de qué está mal o qué falta optimizar]
- **Solución Propuesta**: [Pasos sugeridos para pagarla]
- **Estado**: ⏳ Pendiente | 🔄 En progreso
- **Razón**: [Por qué decidimos diferir esta tarea o por qué no se resolvió de inmediato]
```

### 2. Formato para Deuda Técnica Solventada (Historial)
Cuando una deuda técnica es pagada (refactorizada), se registra en la tabla del **Historial de Deuda Técnica Resuelta** en `razonamiento.md` con este formato de columnas:

| Fecha | Deuda solventada | Solución implementada | Estado final |
| :--- | :--- | :--- | :--- |
| YYYY-MM-DD | [Título de la Deuda] | [Descripción técnica de la refactorización] | ✅ Resuelto |
