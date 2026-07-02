import httpx
import pandas as pd
import json

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

print("========================================")
print("ANALISIS DE DATOS - REPORTE DE DATASETS")
print("========================================\n")

# --- DATASET 1: STANFORD HELM ---
print("--- 1. STANFORD HELM (v1.0.0 Capabilities) ---")
helm_url = "https://storage.googleapis.com/crfm-helm-public/capabilities/benchmark_output/releases/v1.0.0/groups/core_scenarios.json"
try:
    response = httpx.get(helm_url, timeout=20)
    if response.status_code == 200:
        data = response.json()
        # El primer elemento corresponde al grupo 'Accuracy'
        accuracy_group = data[0]
        columns = [h.get("value") for h in accuracy_group["header"]]
        rows = [[cell.get("value") for cell in row] for row in accuracy_group["rows"]]
        
        df_helm = pd.DataFrame(rows, columns=columns)
        print(f"Numero de registros (filas): {len(df_helm)}")
        print(f"Numero de columnas: {len(df_helm.columns)}")
        print("Columnas:", list(df_helm.columns))
        print("\nPrimeros 5 registros:")
        print(df_helm.head(5).to_string(index=False))
    else:
        print(f"Error descargando HELM: {response.status_code}")
except Exception as e:
    print(f"Error parseando HELM: {e}")

print("\n" + "="*50 + "\n")

# --- DATASET 2: LMSYS CHATBOT ARENA ---
print("--- 2. LMSYS CHATBOT ARENA (HF Parquet) ---")
lmsys_url = "https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset/resolve/main/text/latest-00000-of-00001.parquet"
try:
    df_lmsys = pd.read_parquet(lmsys_url)
    print(f"Numero de registros (filas): {len(df_lmsys)}")
    print(f"Numero de columnas: {len(df_lmsys.columns)}")
    print("Columnas:", list(df_lmsys.columns))
    print("\nPrimeros 5 registros:")
    print(df_lmsys.head(5).to_string(index=False))
except Exception as e:
    print(f"Error descargando/abriendo LMSYS: {e}")
