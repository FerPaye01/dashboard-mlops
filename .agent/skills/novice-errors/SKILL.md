---
name: Novice Errors & Learning Journal
description: Sistema para organizar y aprender de errores de programación transformándolos en conocimiento estructurado
---

# Skill: Novice Errors & Learning Journal

## Propósito
Transformar errores de programación y "fallos de novato" en oportunidades de aprendizaje mediante un registro estructurado y análisis de causa raíz (post-mortem).

## Cuándo Usar
- Siempre que el usuario solucione un bug o error inesperado.
- Cuando el asistente detecte un patrón recurrente de errores en el código.
- Después de resolver un problema complejo que tomó mucho tiempo.
- Cuando el usuario pida explícitamente "quiero registrar un error" o "aprender de esto".

## Instrucciones

### 1. Capturar el Error
Cuando ocurra un error, documentar:
- **Mensaje Exacto:** Copiar y pegar el error de la terminal o consola.
- **Contexto:** Qué se intentaba hacer y qué archivo/línea se estaba editando.
- **Código Relacionado:** Pequeño snippet del código antes del fix.

### 2. Análisis de Causa Raíz (Post-Mortem)
Realizar las "5 Porqués" para llegar al fondo del asunto:
- ¿Por qué falló? (Síntoma)
- ¿Por qué ocurrió ese síntoma? (Detalle técnico)
- ¿Por qué no se previó? (Falta de conocimiento/herramienta)
- Ad infinitum hasta llegar a una lección aprendida.

### 3. Registro y Clasificación (Routing)
¿Dónde guardar este aprendizaje?

**A. Error Técnico / Configuración Tecnología** (Ej: Linker error, API Misconfiguration)
- documentar en: `.agent/skills/[tecnologia]/SKILL.md` -> Sección **Solución de Problemas**.
- *Objetivo:* Que el próximo dev (o tú) encuentre la solución al usar esa herramienta.

**B. Error de Lógica / Concepto / "Novatada"** (Ej: Olvidar awaits, bucles infinitos)
- Documentar en: `.agent/knowledge/novice-errors.md` (o archivo central).
- *Objetivo:* Aprender patrones de error humanos y mejorar como programador.

### 4. Formato de Registro
Al guardar el error, usar este esquema:
- **Error:** [Descripción breve o mensaje de log]
- **Solución:** [Cómo se arregló]
- **Aprendizaje:** [Concepto técnico descubierto]
- **Acción Preventiva:** [Qué cambiar para que no pase de nuevo]

### 4. Transformar en Flashcards
Opcionalmente (si el proyecto lo permite), sugerir crear flashcards sobre la lección aprendida para reforzar el conocimiento mediante repetición espaciada.

## Ejemplos
Ver carpeta `examples/` para casos de uso reales del proyecto (como el error del disco C o DeckID).

## Resources
Ver carpeta `resources/knowledge-source.md` para la teoría sobre journals de errores y post-mortems.

## Scripts Disponibles
Actualmente manual (documentación en archivos).

## Logs
- LOG_INFO: "novice-errors: Registrando nuevo aprendizaje desde error [descripción]"
- LOG_INFO: "novice-errors: Análisis post-mortem completado para [error]"
- LOG_WARN: "novice-errors: Detectado patrón recurrente de error en [contexto]"
