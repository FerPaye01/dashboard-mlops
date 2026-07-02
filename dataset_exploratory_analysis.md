# Reporte de Análisis Exploratorio de Datos

Este reporte presenta el perfil de los datasets de **Stanford HELM** y **LMSYS Chatbot Arena**, exponiendo la cantidad de registros, el esquema completo de columnas y una muestra representativa de los primeros 5 registros.

---

## 1. Stanford HELM (Capabilities Release v1.0.0)

Este dataset contiene las métricas de precisión de los principales modelos evaluados bajo la metodología HELM de la Universidad de Stanford.

### Resumen Dimensional
*   **Cantidad de Registros (Filas):** 22 modelos evaluados.
*   **Cantidad de Columnas:** 7 variables de análisis.

### Esquema de Columnas (todas las columnas)
1.  **`Model`** (`string`): Nombre del modelo evaluado.
2.  **`Mean score`** (`float`): Puntuación de precisión promedio agregada de todas las pruebas.
3.  **`MMLU-Pro - COT correct`** (`float`): Precisión bajo Chain-of-Thought (COT) en MMLU-Pro.
4.  **`GPQA - COT correct`** (`float`): Precisión bajo COT en el benchmark GPQA.
5.  **`IFEval - IFEval Strict Acc`** (`float`): Precisión estricta en el benchmark de seguimiento de instrucciones IFEval.
6.  **`WildBench - WB Score`** (`float`): Puntuación obtenida en WildBench.
7.  **`Omni-MATH - Acc`** (`float`): Precisión en problemas matemáticos de nivel olimpíada Omni-MATH.

### Primeros 5 Registros (Muestra)

| Model | Mean score | MMLU-Pro - COT | GPQA - COT | IFEval Strict | WildBench | Omni-MATH |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **DeepSeek v3** | 0.6653 | 0.7230 | 0.5381 | 0.8324 | 0.8305 | 0.4027 |
| **Llama 3.1 Instruct Turbo (405B)** | 0.6177 | 0.7230 | 0.5224 | 0.8112 | 0.7826 | 0.2493 |
| **Llama 3.1 Instruct Turbo (70B)** | 0.5737 | 0.6530 | 0.4260 | 0.8210 | 0.7583 | 0.2100 |
| **Llama 3.1 Instruct Turbo (8B)** | 0.4437 | 0.4060 | 0.2466 | 0.7428 | 0.6865 | 0.1367 |
| **Mistral Instruct v0.3 (7B)** | 0.3759 | 0.2770 | 0.3027 | 0.5675 | 0.6602 | 0.0720 |

---

## 2. LMSYS Chatbot Arena Leaderboard Dataset

Este dataset representa las evaluaciones de preferencia humana recopiladas en vivo mediante duelos a ciegas (A/B testing) en la plataforma Chatbot Arena de LMSYS.

### Resumen Dimensional
*   **Cantidad de Registros (Filas):** 9,124 filas (historial y cortes por categorías).
*   **Cantidad de Columnas:** 11 variables.

### Esquema de Columnas (todas las columnas)
1.  **`model_name`** (`string`): Nombre/identificador técnico del modelo.
2.  **`organization`** (`string`): Organización o empresa creadora del modelo (ej: `anthropic`, `openai`, `deepseek`).
3.  **`license`** (`string`): Tipo de licencia (ej: `Proprietary`, `Apache-2.0`, `Llama-3.1`).
4.  **`rating`** (`float`): Puntuación Elo promedio (métrica principal de inteligencia conversacional).
5.  **`rating_lower`** (`float`): Límite inferior del intervalo de confianza para la puntuación Elo.
6.  **`rating_upper`** (`float`): Límite superior del intervalo de confianza para la puntuación Elo.
7.  **`variance`** (`float`): Varianza de la estimación Elo del modelo.
8.  **`vote_count`** (`float`): Número total de votos (combates) en los que participó el modelo.
9.  **`rank`** (`float`): Rango jerárquico dentro de la categoría actual.
10. **`category`** (`string`): Categoría de corte de la evaluación (ej: `overall`, `coding`, `long_user_query`).
11. **`leaderboard_publish_date`** (`string`): Fecha de publicación del dataset/corte.

### Primeros 5 Registros (Muestra)

| model_name | organization | license | rating | rating_lower | rating_upper | variance | vote_count | rank | category | publish_date |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :---: |
| **claude-opus-4-6-thinking** | anthropic | Proprietary | 1500.25 | 1496.38 | 1504.12 | 3.90 | 51,769 | 1.0 | overall | 2026-06-25 |
| **claude-opus-4-6** | anthropic | Proprietary | 1498.23 | 1494.45 | 1502.01 | 3.72 | 55,027 | 2.0 | overall | 2026-06-25 |
| **claude-fable-5** | anthropic | Proprietary | 1494.45 | 1485.17 | 1503.74 | 22.46 | 4,366 | 3.0 | overall | 2026-06-25 |
| **claude-opus-4-7-thinking** | anthropic | Proprietary | 1489.39 | 1484.92 | 1493.87 | 5.22 | 38,326 | 4.0 | overall | 2026-06-25 |
| **claude-opus-4-7** | anthropic | Proprietary | 1481.65 | 1477.18 | 1486.12 | 5.21 | 39,550 | 5.0 | overall | 2026-06-25 |
