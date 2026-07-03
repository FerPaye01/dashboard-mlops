# Bitácora de Razonamiento (razonamiento.md)

Este archivo sirve como panel de control y bitácora de razonamiento para la planificación,
desglose de tareas y seguimiento de decisiones y deudas técnicas del proyecto.

---

## 🎯 Objetivo de la Sesión Actual
- Implementar y validar la fusión de frameworks en la rama `exp1`.
- Configurar y calibrar el sistema de perfiles y auditoría técnica.

---

## 📋 Desglose de Tareas Activas
- [x] **Configurar la rama exp1**: Crear la rama limpia de trabajo.
- [x] **Fusión de reglas**: Integrar las reglas operativas en `.agent/rules/`.
- [x] **Limpieza del workspace**: Dejar listos los templates de `.agent.architecture` y `llm.md`.
- [x] **Rediseñar Habilidades**:
  - [x] `formulacion-preguntas` (hipótesis por agentes).
  - [x] `pensamiento-critico` (auditor técnico de premisas).
- [x] **Configurar Carpeta Perfil**:
  - [x] Crear `perfil.md`, `razonamiento.md` y `estrategias.md`.
  - [x] Adaptar los skills de preguntas y crítica para que consuman `perfil.md`.
- [ ] **Ajuste de Bitácora**:
  - [x] Centralizar bitácora de decisiones y deudas aquí.
  - [ ] Convertir `decisiones-pendientes.md` y `deudas-tecnicas.md` en reglas estáticas de formato.

---

## ⏳ Decisiones Técnicas Pendientes
*Registradas según el formato de instrucciones de decisiones-pendientes.md*

*(No hay decisiones pendientes en esta sesión)*

---

## ✅ Historial de Decisiones Resueltas
*Registro de decisiones ya tomadas e implementadas:*

| Fecha | Decisión | Solución elegida | Impacto en el sistema |
| :--- | :--- | :--- | :--- |
| 2026-06-28 | Estructura de Rules | Múltiples archivos en `.agent/rules/` | Centraliza directrices operativas en archivos temáticos. |
| 2026-06-28 | Nomenclatura | Español y `snake_Mayus` | Define estilo de código unificado para el proyecto. |
| 2026-06-28 | Stack vs Rules | Stack en `.agent.architecture` | Limpia rules de variables de infraestructura. venv va a comportamiento. |
| 2026-06-28 | Formato de Preguntas | Hipótesis contrastadas por dominio | Cambia opciones de solución por hipótesis evaluables de manera científica. |
| 2026-06-28 | Formato de Crítica | Auditor de premisas obvias | Inyecta pensamiento lateral para cuestionar asunciones implícitas. |
| 2026-07-03 | Simplificación de Rendimiento Local | Remover la caché KV del cálculo de velocidad y quitar topes artificiales de tokens/s. | Modifica `logic.py` y `app.py` para usar un modelo Roofline puro de pesos. |
| 2026-07-03 | Eliminación de Cuantización | Retirar el selector de cuantización y fijar los cálculos locales en precisión FP16 (2.0 bytes/peso). | Simplifica la UI del sidebar y la lógica de VRAM en `app.py` fijando a 16 bits. |
| 2026-07-03 | Eliminación del Tablero de Infraestructura | Borrar la pestaña "Tablero de Infraestructura / Feature Engineering" para simplificar la UI. | Remueve el bloque tab_infraestructura y su visualización de df_infra en `app.py`. |

---

## 🔧 Deuda Técnica Activa
*Registradas según el formato de instrucciones de deudas-tecnicas.md*

*(No hay deudas técnicas activas registradas en esta sesión)*

---

## 📜 Historial de Deuda Técnica Resuelta
*Registro de deudas técnicas solventadas:*

*(No hay deudas técnicas resueltas todavía)*
