import os
import httpx
import asyncio
import sys

# Add root folder to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from logic import load_dotenv

async def probar_api():
    print("=== PROBANDO LA API DE ARTIFICIAL ANALYSIS ===")
    load_dotenv()
    
    api_key = os.getenv("ARTIFICIAL_ANALYSIS_API_KEY")
    if not api_key:
        print("[Error] No se encontro la variable ARTIFICIAL_ANALYSIS_API_KEY en el archivo .env")
        return
        
    print(f"API Key encontrada: {api_key[:6]}...{api_key[-6:] if len(api_key) > 12 else ''}")
    
    url = "https://artificialanalysis.ai/api/v2/language/models"
    headers = {"x-api-key": api_key}
    
    async with httpx.AsyncClient(verify=True) as client:
        try:
            print(f"Enviando solicitud GET a {url}...")
            response = await client.get(url, headers=headers, timeout=15)
            
            print(f"Codigo de respuesta: {response.status_code}")
            if response.status_code != 200:
                print(f"[Error] Error de la API: {response.text[:300]}")
                return
                
            data = response.json()
            print("Conexion exitosa. Datos recibidos.")
            print(f"Tipo de datos de la respuesta: {type(data)}")
            
            # Analyze response structure
            modelos_encontrados = []
            if isinstance(data, list):
                modelos_encontrados = data
            elif isinstance(data, dict):
                print(f"Campos del JSON principal: {list(data.keys())}")
                for k in ["data", "models", "results"]:
                    if k in data and isinstance(data[k], list):
                        modelos_encontrados = data[k]
                        print(f"-> Encontrada lista de modelos en la clave '{k}' con {len(modelos_encontrados)} elementos.")
                        break
            
            if modelos_encontrados:
                print(f"\nTotal de modelos indexados por Artificial Analysis: {len(modelos_encontrados)}")
                print("\nMuestra de los primeros 2 modelos:")
                for i, mod in enumerate(modelos_encontrados[:2]):
                    print(f"\n--- Modelo {i+1} ---")
                    print(f"ID: {mod.get('id') or mod.get('model_id') or mod.get('name')}")
                    print(f"Performance: {mod.get('performance', {})}")
            else:
                print("\nNo se detecto una lista de modelos estructurada. Fragmento del JSON:")
                print(str(data)[:500])
                
        except Exception as e:
            import traceback
            print("[Error] Ocurrio una excepcion durante la conexion:")
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(probar_api())
