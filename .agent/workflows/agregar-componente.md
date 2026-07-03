---
description: Agregar un nuevo componente al proyecto
---

# Flujo: Agregar Componente

## Pasos

1. Definir nombre del componente en español con formato `NombreComponente`

2. Crear archivo en `src/componentes/nombre_componente.js` con:
   - Imports necesarios
   - Logger importado de utilidades
   - Función principal documentada
   - Logs de inicio y fin de renderizado

3. Crear estilos en `src/estilos/componentes/nombre_componente.css` con:
   - Estilos mobile-first (base para 375px)
   - Media query para desktop (min-width: 768px)
   - Media query para desktop grande (min-width: 1200px)

4. Exportar componente desde archivo índice si existe

5. Agregar log en consola describiendo el componente creado
