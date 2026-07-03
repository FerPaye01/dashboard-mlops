---
description: Alinear el contexto del proyecto y limpiar residuos de plantillas
---

# Flujo: Alineamiento de Contexto y Limpieza

Este flujo se utiliza para purgar información inconsistente de las reglas del proyecto (como restos de plantillas previas) y asegurar que Antigravity tenga una visión clara del objetivo actual.

## Pasos

### 1. Definición de Identidad
Antes de cualquier cambio, se debe realizar una entrevista rápida para capturar:
- **Nombre del Proyecto**: (ej. TheLook Churn)
- **Problema Central**: (ej. Predicción de abandono de clientes)
- **Stack Tecnológico**: (ej. Python, Streamlit, XGBoost)
- **Formato de Datos**: (ej. CSV local)

### 2. Escaneo de Inconsistencias
Antigravity debe ejecutar una búsqueda de términos sospechosos en `.agent/rules/`:
- Palabras clave de plantillas conocidas (ej. "Flashcards").
- Placeholders no resueltos (ej. "[Nombre del Problema]").
- Desajustes técnicos (ej. Referencia a React en un proyecto de Python).

### 3. Propuesta de Purga (OBLIGATORIO)
Antigravity presentará una lista de los cambios propuestos en una tabla:

| Archivo | Contenido a Eliminar/Cambiar | Nuevo Contenido Propuesto |
| :--- | :--- | :--- |
| `instrucciones-comportamiento.md` | ... | ... |
| `decisiones-pendientes.md` | ... | ... |

### 4. Confirmación Paso a Paso
**REGLA ESTRICTA**: No se puede sobrescribir ningún archivo de reglas sin un "Sí" explícito del usuario para **cada archivo** o para el bloque completo.

### 5. Ejecución y Registro
- Usar las herramientas de edición de archivos para actualizar las reglas.
- Documentar la sincronización en el historial de `RULES.md`.

### 6. Verificación de Realidad (Física)
**REGLA DE INTEGRIDAD**: Al actualizar hitos o el estado del proyecto, Antigravity DEBE ejecutar comandos `ls` o `grep` para verificar que los archivos mencionados como "Completados" existen físicamente en la ruta especificada. Si no existen, el hito no puede marcarse como ✅.

---

// turbo
#### Comando de Activación Sugerido:
"Antigravity, ejecuta el workflow /alinear-contexto para limpiar los residuos de la plantilla anterior."
