# Ejemplo: Crear Skill desde URL de Documentación

## Contexto
El usuario proporciona una URL de documentación oficial y quiere un skill que implemente esas instrucciones.

## Entrada del Usuario
```
Crea un skill basado en esta documentación: https://example.com/docs/api-integration
```

## Proceso
1. Leer contenido de la URL
2. Extraer secciones principales
3. Identificar pasos de implementación
4. Crear estructura de carpetas
5. Generar SKILL.md con instrucciones
6. Crear ejemplo básico

## Salida Esperada
```
.agent/skills/api-integration/
├── SKILL.md              # Instrucciones extraídas
├── examples/
│   └── ejemplo_basico.md # Caso de uso
├── resources/
│   └── .gitkeep
└── scripts/
    └── .gitkeep
```

## Log de Confirmación
```
LOG_INFO: creador-skills: Skill 'api-integration' creado exitosamente
```
