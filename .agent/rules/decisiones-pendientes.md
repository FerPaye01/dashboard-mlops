---
trigger: always_on
---

# 📋 Directriz: Registro de Decisiones Técnicas

Este archivo es una **regla estática**. Define el estándar obligatorio sobre cómo el asistente
debe documentar y estructurar las decisiones de diseño del proyecto. 

> ⚠️ **REGLA DE REGISTRO**: Las decisiones técnicas reales no se guardan en este archivo.
> Deben registrarse exclusivamente en la sección correspondiente de `.agent/perfil/razonamiento.md`.

---

## ⚖️ Cómo Proponer y Registrar una Decisión

Cuando surja un dilema de diseño o arquitectura, el asistente debe documentarlo en `razonamiento.md` usando los siguientes bloques estructurados:

### 1. Formato para Decisiones Pendientes (Dilemas Activos)
Se debe presentar una tabla comparativa con las opciones evaluadas antes de tomar una resolución:

```markdown
### N. [Título de la Decisión / Dilema]
| Opción | Pros | Contras |
| :--- | :--- | :--- |
| Opción A | [Ventajas técnicas] | [Desventajas, costos, deudas] |
| Opción B | [Ventajas técnicas] | [Desventajas, costos, deudas] |

**Estado:** ⏳ Pendiente
**Decisión:** -
```

### 2. Formato para Decisiones Resueltas (Historial)
Una vez que el usuario elige una opción o se llega a un consenso, la decisión se mueve a la tabla del **Historial de Decisiones Resueltas** en `razonamiento.md` bajo este formato de columnas:

| Fecha | Decisión | Solución elegida | Impacto en el sistema |
| :--- | :--- | :--- | :--- |
| YYYY-MM-DD | [Título] | [Opción elegida y breve razón técnica] | [Componentes o reglas modificadas] |
