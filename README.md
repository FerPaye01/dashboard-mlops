# Selector de Modelos de IA Generativa - MLOps Dashboard (Fase 1)

Este proyecto es la **Fase 1 (Barra Lateral de Infraestructura Física)** de un Dashboard dinámico para la selección de Modelos de Inteligencia Artificial Generativa. Este sistema está orientado a un asistente RAG (Generación Aumentada por Recuperación) que redacta Términos de Referencia (TDR) legales, donde el contexto y la precisión son críticos.

## 🏛️ Estándar de Arquitectura

El código sigue el patrón **Vista - Lógica - Estado**:

1.  **Estado (`st.session_state`):** Todas las variables ingresadas en esta fase (`server_vram`, `context_length`, `concurrent_users`, `selected_model`, `user_activity_rate`) se persisten en el estado de Streamlit y se actualizan de forma inmediata mediante eventos reactivos `on_change`.
2.  **Vista (`app.py`):** Los componentes de entrada y el visualizador KPI / Semáforo de saturación se renderizan exclusivamente en la barra lateral izquierda (`st.sidebar`). El panel central muestra explicaciones visuales, desglose de memoria e integración de APIs.
3.  **Lógica (`logic.py`):** Contiene funciones puras independientes para la estimación del consumo de VRAM y el cálculo del factor de saturación por Erlang-C.

---

## 🔧 Configuración del Entorno Virtual (Garantía Cero Huella)

Para asegurar que al borrar el entorno virtual no quede ningún rastro en tu sistema, se ha diseñado la siguiente estructura. El caché de Hugging Face se redirige de forma local:

1.  **Creación del entorno virtual:**
    ```bash
    python -m venv venv
    ```

2.  **Configuración de `HF_HOME`:**
    Al activar el entorno virtual, puedes redirigir el caché de Hugging Face de forma temporal para que se almacene dentro de la carpeta del entorno.
    *   **En PowerShell (Windows):**
        Edita el archivo `venv\Scripts\Activate.ps1` y añade al final:
        ```powershell
        $env:HF_HOME = "$PSScriptRoot\..\.hf_cache"
        ```
    *   **En Command Prompt (cmd Windows):**
        Edita el archivo `venv\Scripts\activate.bat` y añade al final:
        ```cmd
        set "HF_HOME=%~dp0..\.hf_cache"
        ```

3.  **Instalación de Dependencias:**
    Instala streamlit y huggingface_hub directamente dentro del entorno virtual:
    ```bash
    .\venv\Scripts\pip install streamlit huggingface_hub pandas numpy
    ```

4.  **Ejecución de la Aplicación:**
    ```bash
    .\venv\Scripts\streamlit run app.py
    ```

---

## 🧮 Modelado Matemático de Infraestructura

### 1. Dimensionamiento de VRAM KV Cache
El tamaño de la caché KV por usuario se calcula en base a la topología del modelo:
*   **Atención MHA / GQA:**
    $$V_{\text{KV}} = 2 \times N_{\text{layers}} \times N_{\text{kv\_heads}} \times d_{\text{head}} \times L_{\text{context}} \times B_{\text{bytes}}$$
*   **Atención MLA (DeepSeek):**
    $$V_{\text{KV}} = (d_{\text{latent}} + d_{\text{decoupled}}) \times N_{\text{layers}} \times L_{\text{context}} \times B_{\text{bytes}}$$

### 2. Teoría de Colas Erlang-C
Calcula la probabilidad de que una petición entrante de redacción de TDR quede bloqueada o en cola por falta de slots activos de inferencia (cuando la VRAM está saturada):
$$P_C(m, A) = \frac{\frac{A^m}{m!} \frac{m}{m - A}}{\sum_{k=0}^{m-1} \frac{A^k}{k!} + \frac{A^m}{m!} \frac{m}{m - A}}$$
Donde:
*   $m$ = Número de slots concurrentes tolerados por la VRAM disponible.
*   $A = B_c \times \rho_{\text{user}}$ = Intensidad del tráfico en Erlangs.

---

## 🔌 Fuentes de Datos Integradas
Las funciones de ingesta de datos en `logic.py` están preparadas con el decorador `@st.cache_data(ttl=86400)` para limitar la consulta de APIs a **1 vez al día**, protegiendo los límites de uso de los proveedores externos:
*   **Hugging Face Hub (`huggingface_hub.HfApi`):** Metadatos de tensores, capas y tipo de atención.
*   **Artificial Analysis / OpenRouter:** Latencia (TTFT), velocidad (Tokens/s) y costo.
*   **Open LLM Leaderboard (EleutherAI):** Benchmarks de calidad de razonamiento legal (MMLU, IFEval, GPQA).

---

## ⚙️ Fase 2: Preferencias de Negocio y Despliegue

En esta fase, la aplicación incorpora las prioridades estratégicas del negocio para balancear la selección final del modelo:

1.  **Entorno de Despliegue (Filtro Dinámico):**
    *   **Solo Local (Privado / GGUF):** Filtra y mantiene solo modelos con soporte de descarga física (.safetensors o GGUF) indexados en Hugging Face, considerando los límites físicos de VRAM del nodo local (Fase 1).
    *   **Solo Cloud (APIs / OpenRouter):** Omite la limitación física de la VRAM local (Fase 1) y evalúa el hosting en la nube mediante costes por millón de tokens.
    *   **Ambos (Híbrido):** Realiza una comparación integral balanceando las dos estrategias.
2.  **Sliders Reactivos Normalizados (Matemática de Ponderación):**
    Los pesos asignados a **Calidad Técnica** ($W_{\text{calidad}}$), **Velocidad** ($W_{\text{velocidad}}$) y **Eficiencia** ($W_{\text{eficiencia}}$) se normalizan de forma interactiva e instantánea usando la función `normalize_weights` para asegurar que:
    $$W_{\text{calidad}} + W_{\text{velocidad}} + W_{\text{eficiencia}} = 100\%$$
3.  **Etiqueta Dinámica de Eficiencia:**
    La etiqueta del tercer slider se adapta contextualmente según la opción de despliegue seleccionada:
    *   Local $\rightarrow$ **Eficiencia de VRAM**.
    *   Cloud $\rightarrow$ **Menor Coste por Token**.
    *   Híbrido $\rightarrow$ **Eficiencia de VRAM / Coste**.

