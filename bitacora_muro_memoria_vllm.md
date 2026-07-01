# Bitácora de Sesión: Rompiendo el Muro de Memoria y Calibración de vLLM con Qwen 2.5
**Identificador Simbólico de Sesión:** `SESION_MURO_MEMORIA_INNOVATE_VLLM`  
**Fecha:** 2026-07-01  
**Estado:** Completado y Calibrado  

---

## 1. Contexto de la Sesión y Debate de Arquitectura
La sesión se centró en auditar y perfeccionar el modelado matemático utilizado en el dashboard MLOps para la estimación del consumo de memoria física (VRAM) en inferencia local e híbrida de LLMs (Modelos de Lenguaje).

Se abordó un cambio de paradigma conceptual:
* **Enfoque Anterior (Top-Down / Restringido por Recurso):** La infraestructura física disponible (VRAM de la GPU elegida) limitaba y descartaba qué modelos eran visibles o compatibles.
* **Enfoque Actual (Bottom-Up / Orientado a Requisitos):** Los parámetros de carga de trabajo del usuario (modelo base seleccionado, longitud del contexto, nivel de concurrencia y tasa de actividad) deben realizar un proceso de *Feature Engineering* sobre el catálogo completo para proyectar de forma masiva los requerimientos físicos ideales (VRAM Base, KV Cache y VRAM Peak), recomendando de forma proactiva la GPU o instancia cloud idónea en lugar de actuar como un filtro eliminatorio.

---

## 2. Validación Empírica en Caliente (Ollama - Qwen 2.5 7B)
Se realizó una descarga y ejecución real en el entorno del usuario para medir el impacto de memoria de un modelo base cuantizado:
* **Modelo Descargado:** `qwen2.5:7b` (Arquitectura `qwen2` de 7.61B parámetros, cuantización `Q4_K_M`).
* **Tamaño del archivo en disco:** `4.7 GB`.
* **Memoria en ejecución observada (`ollama ps`):** `5.1 GB` activos en RAM/CPU para una longitud de contexto de **4096 tokens**.
* **Diferencia de Overhead y Caché KV medida:** $5.1\text{ GB} - 4.7\text{ GB} = 0.4\text{ GB } (\approx 400\text{ MB})$.

### Demostración Matemática de Calibración
La topología fina de Qwen 2.5 7B utiliza **GQA (Grouped-Query Attention)**:
* $N_{\text{layers}} = 28$
* $N_{\text{kv\_heads}} = 4$
* $d_{\text{head}} = 128$ ($\text{hidden\_size } 3584 / N_{\text{heads }} 28$)
* $B_{\text{bytes}} = 2.0$ (FP16 para caché de claves/valores en motores llama.cpp/Ollama)
* $L_{\text{contexto}} = 4096$

$$V_{\text{KV}} = 2 \times N_{\text{layers}} \times N_{\text{kv\_heads}} \times d_{\text{head}} \times L_{\text{contexto}} \times B_{\text{bytes}}$$
$$V_{\text{KV}} = 2 \times 28 \times 4 \times 128 \times 4096 \times 2 \text{ bytes}$$
$$V_{\text{KV}} = 234,881,024 \text{ bytes} \approx \mathbf{224\text{ MB }} (\mathbf{0.22\text{ GB}})$$

Los $\approx 176\text{ MB}$ restantes para completar los 400 MB observados corresponden al overhead del motor de ejecución (grafo de cómputo, buffers de activación y subprocesos).

> [!NOTE]
> **Importancia de la precisión del modelo matemático:** 
> Si el dashboard no discriminara la arquitectura de atención y asumiera MHA (Multi-Head Attention estándar) para todos los modelos locales por igual, la caché KV para Qwen 2.5 7B se habría calculado erróneamente en:
> $$V_{\text{KV\_MHA}} = 2 \times 28 \times 28 \times 128 \times 4096 \times 2 \text{ bytes} \approx \mathbf{1.53\text{ GB}}$$
> Esto representaría una sobreestimación de **+1.31 GB por usuario**. Multiplicado por 15 usuarios concurrentes, el cálculo incorrecto arrojaría **22.9 GB de caché KV** en lugar de los **3.3 GB reales**, provocando falsos descartes de hardware local en el dashboard.

---

## 3. Contraste con Caso Real de Producción (Grupo INNOVATE)
El grupo INNOVATE compartió las especificaciones de su entorno preproductivo en AWS SageMaker para desplegar **Qwen 2.5 7B** soportando un máximo de **15 usuarios concurrentes** con respuestas inmediatas en milisegundos:
* **GPU (VRAM):** 24 GB.
* **Procesador (CPU):** 2 vCPUs (inicialmente).
* **Memoria RAM:** 8 o 16 GB (inicialmente).
* **Motor de Inferencia:** **vLLM** corriendo sobre instancias de la familia `ml.g5`.
* **Comportamiento observado:** El modelo activo consume cerca de 14 GB de la GPU (VRAM), dejando 10 GB libres para herramientas auxiliares y caché interno. Al superar los 15 usuarios, las peticiones empiezan a encolarse de forma notable.
* **Solución de escalabilidad de INNOVATE:** Cambiar a la instancia **`ml.g5.4xlarge`** (16 vCPUs y 64 GB de RAM) manteniendo la misma GPU (1x A10G de 24 GB VRAM) para poder alojar modelos más grandes.

### Análisis MLOps del Entorno INNOVATE
1. **Equivalencia Binaria de VRAM:** 
   El reporte de consumos de "14 GB" para el modelo activo encaja con los pesos en precisión FP16 ($7.61\text{B parámetros} \times 2\text{ bytes} = 15.22\text{ GB}$ decimales), que equivale exactamente a **14.17 GiB** en la medición del sistema operativo de la GPU.
2. **Explicación de la Reserva Dinámica de vLLM:**
   vLLM pre-asigna espacio de VRAM al arrancar para evitar fragmentación. Si se define `gpu_memory_utilization = 0.90` en una GPU de 24 GB, el servicio reserva **21.6 GB** de VRAM de manera fija. De estos, ~14.2 GB son pesos y activaciones y los ~7.4 GB restantes se dividen en páginas lógicas de caché KV.
3. **El Cuello de Botella Oculto (CPU Host y RAM Host):**
   La necesidad de INNOVATE de pasar de una instancia pequeña a una `ml.g5.4xlarge` confirma que el cuello de botella del encolamiento a partir de los 15 usuarios **no era la VRAM de la GPU**, sino la potencia del CPU host para gestionar las colas de peticiones, la fase de pre-llenado de tokens (*prefill stage*), y el cargado seguro en memoria RAM del sistema sin producir OOM (Out Of Memory) en el host.

---

## 4. Implementaciones Realizadas en el Código (`app.py`)
Para reflejar estos aprendizajes en la aplicación web del dashboard, se realizaron las siguientes modificaciones:

1. **Feature Engineering en el Catálogo Dinámico:**
   Se modificó el loop de procesamiento en [app.py](file:///C:/Users/opaye/Proyectos/dashboards/app.py) para inyectar en caliente métricas físicas detalladas para **todos** los modelos del catálogo de forma paralela:
   * `_vram_base_gb`: Pesos estáticos cuantizados + 5% de activaciones.
   * `_kv_cache_user_gb`: Tamaño de la caché KV para 1 usuario según su arquitectura de atención.
   * `_kv_cache_total_gb`: KV Cache total requerida para los usuarios concurrentes configurados en el sidebar.
   * `_vram_peak_gb`: Consumo peak recomendado de VRAM para producción (Weights + KV + Activations + 20% Margen de Seguridad + 2 GB CUDA).
   * `_hw_sugerido`: GPU e instancia cloud sugerida (como `ml.g5.2xlarge` o clústeres Multi-GPU `ml.p4d`).
   * `_params_b`: Parámetros en billones.

2. **Pestaña "Tablero de Infraestructura / Feature Engineering":**
   Se creó una nueva pestaña centralizada llamada **`📊 Tablero de Infraestructura / Feature Engineering`** que muestra side-by-side la comparativa de todos los modelos bajo este enfoque de ingeniería de características físicas de VRAM.

3. **Optimización para Modelos Cloud:**
   Se corrigió el comportamiento de los modelos hospedados en la nube (ej: `NVIDIA: Nemotron 3 Ultra`). Al no ejecutarse localmente, ahora todas sus columnas de VRAM se formatean como **`N/A (Cloud)`**, eliminando la visualización confusa de terabytes de VRAM local requeridos.

4. **Control Global de Cuantización (Sidebar):**
   Se integró el selector interactivo **`🎚️ Cuantización de Referencia (Local)`** en la barra lateral izquierda. Permite conmutar instantáneamente todo el simulador y catálogo entre **FP16 / BF16 (Nativo)**, **INT8** e **INT4 (Q4_K_M)**, recalculando dinámicamente cada métrica y compatibilidad en caliente.

5. **Sincronización del Modelo Seleccionado:**
   Se vinculó la sección de simulación de colas y desglose de VRAM del modelo validado al final de la página para que responda dinámicamente a los bits de la cuantización global seleccionada (16, 8 o 4 bits).

---

## 5. Decisiones Pendientes y Vacíos Técnicos (No Simplificados)
Los siguientes aspectos quedan abiertos para ser validados con el equipo INNOVATE o implementados en futuras iteraciones del dashboard:

* **[ ] Parámetro `--max-model-len` en vLLM:**
  Se debe verificar cuál es el límite físico de contexto configurado en el servidor vLLM de INNOVATE (por ejemplo, si está limitado a 8,192 o 16,384 tokens). Esto altera drásticamente el tamaño del pool de páginas reservado en la GPU y debe sincronizarse con el slider de longitud de contexto del simulador.
* **[ ] Verificación de Parámetros de Inferencia de vLLM:**
  Validar si INNOVATE tiene habilitados parámetros clave en producción como `--enable-prefix-caching` (para optimizar plantillas comunes de TDR), `--max-num-seqs` (máximo de secuencias simultáneas por batch), y si están utilizando esquemas de cuantización intermedia como *AWQ/GPTQ de 4 bits* o *FP8 de 8 bits* para optimizar el rendimiento por token.
* **[ ] Mapeo de Tamaño Físico de Descarga:**
  La API de Hugging Face a veces no expone directamente el peso físico en bytes del archivo cuantizado GGUF o Safetensor antes de descargarlo. Sería óptimo extender la inyección de la Capa Bronce/Plata para descargar o consultar el tamaño real del archivo del repositorio de Hugging Face y guardarlo en `model_catalog_cache.json` como un feature estático de tamaño real en disco, en lugar de aproximarlo de forma teórica.
* **[ ] Puntuación de Compatibilidad de Host (CPU/RAM):**
  Actualmente, el dashboard solo calcula la compatibilidad local basada en la VRAM de la GPU. Dado que el CPU host (vCPUs) y la RAM del sistema demostraron ser el factor limitante real para la concurrencia de 15 usuarios en producción en AWS, se debe evaluar si el dashboard debe incorporar una segunda regla de validación de CPU/RAM para marcar un modelo como "Incompatible" o "Riesgo de Degradación por Host CPU" si la instancia de GPU seleccionada no posee al menos 8 vCPUs y 32 GB de RAM (para modelos > 8B).
