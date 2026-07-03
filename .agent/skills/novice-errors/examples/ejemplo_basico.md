# Ejemplo: Error de Conteo (DeckID vs Name)

## Contexto
Durante el procesamiento de imágenes, el backend reportaba "0 flashcards generadas" aunque el motor de IA decía haber creado 23.

## Entrada
- **Error:** `[08:46:18] ⚠️ Sección 1: Procesado, pero no se generaron flashcards.`
- **Contexto:** Se usaba el nombre de la sección (`sectionTitle`) para buscar tarjetas en lugar del ID único del mazo (`targetDeckID`).

## Proceso (Post-Mortem)
1. **Identificación:** El log del backend mostraba éxito, pero el frontend recibía 0.
2. **Causa:** Confusión de parámetros en `flashcardService.ListFlashcards`.
3. **5 Porqués:**
    - ¿Por qué el reporte da 0? Porque la consulta falló.
    - ¿Por qué falló la consulta? Porque buscó `deck_id = 'Sección 1'`.
    - ¿Por qué buscó eso? Porque se pasó el nombre del mazo en vez de su ID.
    - ¿Por qué se pasó el nombre? Por una suposición de que los nombres eran únicos e identificadores directos.
    - ¿Por qué se supuso eso? Falta de revisión estricta de la firma de la función en el servicio.

## Salida Esperada (Aprendizaje)
- **Lección:** Siempre usar IDs (UUIDs) para consultas en base de datos, nunca nombres legibles por humanos que pueden duplicarse o ser solo etiquetas.
- **Acción Preventiva:** Verificar la firma de los métodos del servicio antes de llamarlos desde el handler.
