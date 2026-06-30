import os
import sys
# Añadir la carpeta raíz al path para poder importar logic
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from logic import load_dotenv

def test_load_env():
    print("=== Test de Carga de Variables de Entorno ===")
    
    # 1. Cargar el .env
    load_dotenv()
    
    # 2. Verificar tokens
    hf_token = os.environ.get("HF_TOKEN")
    openrouter_key = os.environ.get("OPENROUTER_API_KEY")
    
    print(f"HF_TOKEN cargado: {'Sí (Comienza con ' + hf_token[:6] + '...)' if hf_token else 'No (Vacío)'}")
    print(f"OPENROUTER_API_KEY cargado: {'Sí (Comienza con ' + openrouter_key[:6] + '...)' if openrouter_key else 'No (Vacío)'}")
    
    if not hf_token:
        print("💡 Nota: Puedes añadir tu token en el archivo .env para evitar límites de rate limit en Hugging Face.")
    else:
        print("✅ Configuración de .env cargada correctamente.")

if __name__ == "__main__":
    test_load_env()
