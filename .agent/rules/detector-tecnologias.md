---
trigger: always_on
---

# 🔍 Detector de Tecnologías y Conocimientos

Regla que detecta menciones de tecnologías o fuentes de conocimiento y sugiere workflows apropiados.

---

## Cuándo Activar

Detectar cuando el usuario:
1. Menciona querer aprender una tecnología/framework/herramienta
2. Proporciona documentación (archivo, enlace, texto)
3. Pregunta sobre cómo usar algo que no está en los skills actuales

### Palabras Clave de Activación
- "quiero aprender..."
- "documentación de..."
- "cómo usar [tecnología]"
- "aquí está la guía de..."
- "mira este PDF/enlace/texto sobre..."
- "necesito saber sobre..."

---

## Lógica de Decisión

```
1. ¿El usuario menciona tecnología/herramienta?
   ├── NO → No hacer nada
   └── SÍ → Continuar

2. ¿Existe skill en .agent/skills/ para esa tecnología?
   │
   ├── NO EXISTE → Sugerir workflows de CREACIÓN:
   │   ├── ¿Tiene fuente el usuario (archivo/enlace/texto)?
   │   │   ├── SÍ → Sugerir /crear-skill-conocimiento
   │   │   └── NO → Sugerir /crear-skill-conocimiento-documentado
   │
   └── SÍ EXISTE → Sugerir workflows de ACTUALIZACIÓN:
       ├── ¿Tiene fuente el usuario (archivo/enlace/texto)?
       │   ├── SÍ → Sugerir /actualizar-skill-conocimiento
       │   └── NO → Sugerir /actualizar-skill-conocimiento-documentado
```

---

## Respuesta al Usuario

### Si NO existe el skill:
```
Detecté que mencionas [tecnología]. 
No existe un skill para eso todavía.

¿Tienes documentación (archivo, enlace o texto)?
- SÍ → Usa /crear-skill-conocimiento [nombre] [fuente]
- NO → Usa /crear-skill-conocimiento-documentado [nombre]
```

### Si SÍ existe el skill:
```
Detecté que mencionas [tecnología].
Ya existe el skill `.agent/skills/[nombre-skill]/`

¿Quieres actualizarlo con nueva información?
- SÍ, tengo fuente → Usa /actualizar-skill-conocimiento [nombre] [fuente]
- SÍ, busca online → Usa /actualizar-skill-conocimiento-documentado [nombre]
```

---

## Verificación de Skill Existente

Para verificar si existe un skill:
1. Listar carpetas en `.agent/skills/`
2. Buscar coincidencia con el nombre de la tecnología
3. Si hay coincidencia parcial, preguntar al usuario si es el mismo
