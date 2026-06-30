import os
import sys
# Añadir la carpeta raíz al path para poder importar logic
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from logic import (
    fetch_huggingface_model_metadata,
    fetch_physical_performance_metrics,
    cargar_catalogo_modelos
)

def test_model_metadata():
    print("=== Test de Extracción de Metadatos de Interés ===")
    
    # 1. Probar extracción de metadatos de un modelo local de Hugging Face
    local_model_id = "Qwen/Qwen2.5-7B-Instruct"
    print(f"\n[LOCAL] Extrayendo metadatos técnicos de Hugging Face para: {local_model_id}")
    local_meta = fetch_huggingface_model_metadata(local_model_id)
    print("Resultados:")
    print(f" - ID de Modelo: {local_meta.get('model_id')}")
    print(f" - Parámetros (B): {local_meta.get('parameters_b')}")
    print(f" - Capas (layers): {local_meta.get('layers')}")
    print(f" - Hidden Size (Tamaño oculto): {local_meta.get('hidden_size')}")
    print(f" - Cabezales de Atención (num_heads): {local_meta.get('num_heads')}")
    print(f" - Cabezales KV (num_kv_heads): {local_meta.get('num_kv_heads')}")
    print(f" - Tipo de Atención: {local_meta.get('attention_type')}")
    print(f" - Fuente de Datos: {local_meta.get('source')}")
    
    # 2. Probar extracción de métricas de rendimiento físico (TTFT, velocidad, costo de APIs)
    print(f"\n[PERFORMANCE] Extrayendo métricas de latencia y costo para: {local_model_id}")
    perf = fetch_physical_performance_metrics(local_model_id)
    print("Resultados:")
    print(f" - TTFT estimado (ms): {perf.get('ttft_ms')}")
    print(f" - Velocidad estimada (Tokens/s): {perf.get('tokens_per_sec')}")
    print(f" - Costo Input (por Millón): ${perf.get('cost_input_per_m')}")
    print(f" - Costo Output (por Millón): ${perf.get('cost_output_per_m')}")

    # 3. Probar ingesta parcial del catálogo completo (Local y Cloud)
    print(f"\n[CATALOG] Probando ingesta dinámica de catálogo con un límite bajo...")
    df_cat = cargar_catalogo_modelos(
        tipo_despliegue="Ambos (Híbrido)",
        server_vram=80.0,
        context_length=8000,
        concurrent_users=5,
        limite_modelos=15
    )
    if not df_cat.empty:
        print(f"✅ Ingesta completada con éxito. Se recuperaron {len(df_cat)} modelos en el catálogo.")
        print("\nMuestreo de modelos recuperados:")
        print(df_cat[["model_id", "hosting", "attention_type", "format"]].head(5))
    else:
        print("❌ No se pudieron recuperar modelos para el catálogo.")

if __name__ == "__main__":
    test_model_metadata()
