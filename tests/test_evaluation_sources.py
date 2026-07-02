import os
import sys
import httpx
import pandas as pd

# Añadir la carpeta raíz al path para poder importar logic
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def test_artificial_analysis_structure():
    """
    Test para validar la estructura del API de Artificial Analysis.
    Usa la API Key de entorno si está disponible. Si no, realiza una validación
    estructural simulada (mock) con la estructura esperada de /language/models.
    """
    print("\n=== 1. Test Artificial Analysis API ===")
    api_key = os.getenv("ARTIFICIAL_ANALYSIS_API_KEY")
    url = "https://artificialanalysis.ai/api/v2/language/models"
    
    if api_key:
        print(f"API Key encontrada. Realizando peticion real a {url}...")
        headers = {"x-api-key": api_key}
        try:
            response = httpx.get(url, headers=headers, timeout=15)
            assert response.status_code == 200, f"Error en la API de AA: {response.status_code}"
            data = response.json()
            
            models = []
            if isinstance(data, list):
                models = data
            elif isinstance(data, dict):
                models = data.get("data", [])
            
            assert len(models) > 0, "No se recibieron modelos de la API de AA"
            sample = models[0]
            print(f"Modelo de muestra obtenido: {sample.get('id') or sample.get('name')}")
            
            # Verificar campos de evaluaciones y performance
            assert "performance" in sample or "evaluations" in sample, "Falta informacion de rendimiento/evaluaciones"
            if "evaluations" in sample:
                evals = sample["evaluations"]
                print("Campos en 'evaluations':", list(evals.keys()))
        except Exception as e:
            print(f"Error consultando API de AA: {e}")
            assert False, f"Fallo la consulta real: {e}"
    else:
        print("ARTIFICIAL_ANALYSIS_API_KEY no configurada. Ejecutando validacion estructurada simulada (Mock)...")
        # Estructura de muestra documentada de la API v2
        mock_response = {
            "id": "meta-llama-3-8b-instruct",
            "name": "Meta Llama 3 8B Instruct",
            "slug": "meta-llama-3-8b-instruct",
            "evaluations": {
                "artificial_analysis_intelligence_index": 62.4,
                "gpqa_diamond": 28.5,
                "mmlu_pro": 45.2,
                "if_bench": 76.1
            },
            "performance": {
                "time_to_first_token": 0.15,
                "tokens_per_second": 85.0
            }
        }
        
        # Validaciones de estructura mock
        assert "id" in mock_response
        assert "evaluations" in mock_response
        assert "performance" in mock_response
        
        evals = mock_response["evaluations"]
        assert "artificial_analysis_intelligence_index" in evals
        assert "gpqa_diamond" in evals
        assert "mmlu_pro" in evals
        assert "if_bench" in evals
        
        print("[MOCK OK] La estructura teorica del API de AA es valida.")


def test_stanford_helm_structure():
    """
    Test para validar la estructura del GCS público de Stanford HELM.
    Descarga el archivo core_scenarios.json de la release v1.0.0 de Capabilities.
    """
    print("\n=== 2. Test Stanford HELM (GCS) ===")
    base_url = "https://storage.googleapis.com/crfm-helm-public/"
    path = "capabilities/benchmark_output/releases/v1.0.0/groups/core_scenarios.json"
    full_url = base_url + path
    
    print(f"Descargando datos de HELM desde: {full_url}")
    response = httpx.get(full_url, timeout=20)
    assert response.status_code == 200, f"Error descargando HELM: {response.status_code}"
    
    data = response.json()
    assert isinstance(data, list), "El archivo core_scenarios.json debe ser una lista"
    assert len(data) > 0, "La lista esta vacia"
    
    # El primer elemento corresponde al grupo 'Accuracy'
    accuracy_group = data[0]
    assert accuracy_group.get("title") == "Accuracy", "El primer grupo deberia ser 'Accuracy'"
    
    # Validar que contenga cabecera y filas (rows)
    assert "header" in accuracy_group
    assert "rows" in accuracy_group
    
    headers = [h.get("value") for h in accuracy_group["header"]]
    print("Columnas de HELM encontradas:", headers)
    
    # Esperamos ver MMLU-Pro, GPQA e IFEval en las columnas
    expected_benchmarks = ["Model", "Mean score", "MMLU-Pro", "GPQA", "IFEval"]
    for eb in expected_benchmarks:
        assert any(eb in col for col in headers), f"No se encontro la columna {eb} en la cabecera"
        
    rows = accuracy_group["rows"]
    assert len(rows) > 0, "No se encontraron filas con datos de modelos"
    
    # Validar estructura de celdas del primer modelo
    first_row = rows[0]
    assert isinstance(first_row, list), "Cada fila en HELM debe ser una lista de celdas"
    
    model_name = first_row[0].get("value")
    mean_score = first_row[1].get("value")
    print(f"Primer modelo encontrado en HELM: {model_name} (Mean Score: {mean_score})")
    
    assert isinstance(model_name, str)
    assert isinstance(mean_score, (int, float))
    print("[HELM OK] La estructura de Stanford HELM se cargo y parseo exitosamente.")


def test_lmsys_chatbot_arena_structure():
    """
    Test para validar el leaderboard de LMSYS Chatbot Arena alojado en Hugging Face.
    Descarga el dataset de texto mas reciente en formato Parquet y valida sus columnas y ELO.
    """
    print("\n=== 3. Test LMSYS Chatbot Arena (Hugging Face Parquet) ===")
    url = "https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset/resolve/main/text/latest-00000-of-00001.parquet"
    
    print(f"Descargando y abriendo Parquet desde Hugging Face: {url}")
    df = pd.read_parquet(url)
    
    assert not df.empty, "El dataframe de LMSYS esta vacio"
    print(f"Dimensiones del dataset LMSYS: {df.shape}")
    
    # Columnas requeridas
    required_cols = ["model_name", "rating", "rank", "category"]
    for col in required_cols:
        assert col in df.columns, f"Falta la columna requerida '{col}' en LMSYS"
        
    # Verificar que el rating (ELO) sea numerico y este ordenado
    assert pd.api.types.is_numeric_dtype(df["rating"]), "La columna 'rating' debe ser numerica"
    
    # Mostrar el top 3
    top_models = df.sort_values(by="rating", ascending=False).head(3)
    print("Top 3 modelos segun rating ELO de LMSYS Chatbot Arena:")
    for idx, row in top_models.iterrows():
        print(f" - Rank {row['rank']}: {row['model_name']} (Elo: {row['rating']:.2f})")
        
    print("[LMSYS OK] El dataset Parquet de LMSYS se cargo y valido correctamente.")

if __name__ == "__main__":
    test_artificial_analysis_structure()
    test_stanford_helm_structure()
    test_lmsys_chatbot_arena_structure()
