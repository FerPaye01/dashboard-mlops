---
trigger: always_on
---

# 🛡️ Regla 0: Auditoría Contextual Obligatoria (0-AUDITORIA-OBLIGATORIA.md)

**Propósito**: Esta es la regla primordial (Regla Cero). Obliga al asistente a auditar contextualmente sus propuestas frente al resto de directrices del proyecto y el perfil del usuario antes de dar respuestas, proponer planes o escribir código.

---

## 📋 1. Checklist de Auditoría Interna (Ejecución Obligatoria)
Antes de responder, el asistente debe validar su propia propuesta contra este checklist:

- **Simplicidad (➔ [principios-simplicidad.md](file:///data/proyectos/proyecto_de_proyectos/.agent/rules/principios-simplicidad.md))**:
  - ¿La solución es directa y sin abstracciones complejas?
  - ¿Está 100% libre de `# TODO` o placeholders (cero ambigüedad)?
- **Comportamiento (➔ [instrucciones-comportamiento.md](file:///data/proyectos/proyecto_de_proyectos/.agent/rules/instrucciones-comportamiento.md))**:
  - ¿Todas las variables y funciones propuestas usan `snake_Mayus` en español?
  - Si es Python, ¿se exige activar el entorno virtual (`venv`)?
  - ¿Los logs propuestos son autocontenidos y siguen las convenciones de JS/Python?
- **Auditoría de Pensamiento Crítico (➔ [pensamiento-critico](file:///data/proyectos/proyecto_de_proyectos/.agent/skills/pensamiento-critico/SKILL.md))**:
  - Si propongo un plan o cambio de diseño, ¿he listado y desafiado al menos 3 premisas obvias mediante pensamiento lateral?
- **Detector de Tecnologías (➔ [detector-tecnologias.md](file:///data/proyectos/proyecto_de_proyectos/.agent/rules/detector-tecnologias.md))**:
  - Si el usuario menciona querer aprender algo, proporciona documentación o pregunta sobre una nueva herramienta, ¿he sugerido activar los workflows de creación/actualización de skills?
- **Registro de Estado (➔ [decisiones-pendientes.md](file:///data/proyectos/proyecto_de_proyectos/.agent/rules/decisiones-pendientes.md) / [deudas-tecnicas.md](file:///data/proyectos/proyecto_de_proyectos/.agent/rules/deudas-tecnicas.md))**:
  - Si propongo una solución rápida o hay deudas/decisiones, ¿se indica registrarlo en [razonamiento.md](file:///data/proyectos/proyecto_de_proyectos/.agent/perfil/razonamiento.md) con el formato correspondiente?

---

## 🛑 2. Frenos de Seguridad e Intervención (Detenerse y Esperar)
El asistente **DEBE detenerse a esperar la aprobación explícita** del usuario antes de:
1. Modificar múltiples archivos a la vez o proponer cambios de arquitectura lógica.
2. Ejecutar comandos de terminal que escriban, alteren o eliminen archivos en el sistema (excluyendo lecturas).
3. **Freno Total**: NUNCA intentar configurar credenciales de Git (`git config`), claves privadas, ni ejecutar comandos de subida remota (`git push`) sin autorización explícita del usuario.

---

## ❓ 3. Protocolo de Preguntas e Hipótesis
Cuando sea necesario consultar al usuario:
- Invocar el skill `formulacion-preguntas` para plantear hipótesis de desarrollo (mínimo 2) en vez de opciones de solución cerradas.
- Consultar el archivo [perfil.md](file:///data/proyectos/proyecto_de_proyectos/.agent/perfil/perfil.md) para calibrar la jerga técnica y la complejidad de los pasos de verificación de la hipótesis.
- **Visualización**: Los diagramas Mermaid son opcionales. Solo generarlos si el flujo lógico/arquitectónico es verdaderamente complejo o si el usuario lo solicita.

---

## 🚫 Excepciones de Parada
No requiere pausar la ejecución en tareas triviales (ej. corrección de typos menores, cambio de textos estáticos, o cuando el usuario pida de forma explícita "un cambio directo sin preguntas").
