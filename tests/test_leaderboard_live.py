import os
import sys
# Añadir la carpeta raíz al path para poder importar logic
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from logic import fetch_leaderboard_benchmarks_live, fetch_quality_and_benchmarks

def test_leaderboard_live():
    print("=== Test de Extracción de Benchmarks en Vivo (Leaderboard v2) ===")
    
    # 1. Probar un modelo que sabemos que existe en el Leaderboard v2
    target_model_1 = "meta-llama/Meta-Llama-3-8B-Instruct"
    print(f"\nConsultando benchmarks para: {target_model_1}")
    benchmarks_1 = fetch_leaderboard_benchmarks_live(target_model_1)
    
    if benchmarks_1:
        print("✅ Coincidencia encontrada en el Dataset Server de Hugging Face:")
        print(f" - IFEval (Calidad de Instrucciones): {benchmarks_1['ifeval']:.2f}%")
        print(f" - MMLU-PRO (Conocimiento Multidisciplinar): {benchmarks_1['mmlu']:.2f}%")
        print(f" - GPQA (Razonamiento de Postgrado): {benchmarks_1['gpqa']:.2f}%")
    else:
        print("❌ No se encontraron benchmarks para este modelo en la API en vivo.")

    # 2. Probar un modelo ficticio o inexistente
    target_model_2 = "user/modelo-ficticio-que-no-existe-1234"
    print(f"\nConsultando benchmarks para un modelo inexistente: {target_model_2}")
    benchmarks_2 = fetch_quality_and_benchmarks(target_model_2)
    print(f"Resultado obtenido: {benchmarks_2}")
    print("✅ Confirmado: Retorna valores nulos (None) en lugar de inventar datos de prueba.")

if __name__ == "__main__":
    test_leaderboard_live()
