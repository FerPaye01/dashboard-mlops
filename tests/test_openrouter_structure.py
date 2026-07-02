import os
import sys
import asyncio
import httpx

# Añadir la carpeta raíz al path para poder importar logic
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from logic import LLMDataIngester

async def run_openrouter_test():
    print("=== Test de Estructura de Datos de OpenRouter ===")
    
    # 1. Test de la API directa de OpenRouter
    url = "https://openrouter.ai/api/v1/models"
    print(f"\n[API] Consultando directamente {url}...")
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=15)
        
        assert response.status_code == 200, f"Error en la petición: {response.status_code}"
        data = response.json()
        assert "data" in data, "La respuesta no contiene la clave 'data'"
        
        models = data["data"]
        print(f"Total de modelos encontrados: {len(models)}")
        assert len(models) > 0, "La API retornó una lista de modelos vacía"
        
        # Buscar un modelo conocido o usar el primero de la lista para la validación
        sample = None
        for m in models:
            if "claude" in m.get("id", "").lower() or "llama" in m.get("id", "").lower():
                sample = m
                break
        if not sample:
            sample = models[0]
            
        print(f"\n[ESTRUCTURA CRUDA] Validando campos en el modelo de muestra ({sample.get('id')}):")
        
        # Validar la presencia de campos clave
        required_keys = ["id", "name", "context_length", "pricing"]
        for key in required_keys:
            assert key in sample, f"Falta la clave requerida '{key}' en el modelo"
            print(f" - {key}: {sample[key]}")
            
        # Validar estructura del objeto de precios
        pricing = sample["pricing"]
        pricing_keys = ["prompt", "completion"]
        for pk in pricing_keys:
            assert pk in pricing, f"Falta la clave de pricing '{pk}'"
            # Verificar que sea convertible a float
            try:
                val = float(pricing[pk])
                print(f"   * pricing.{pk}: {val} (casteable a float)")
            except (ValueError, TypeError):
                assert False, f"El campo pricing.{pk} ({pricing[pk]}) no se puede convertir a float"
        
        # Mostrar campos opcionales del caché si están presentes en la respuesta de este modelo
        cache_fields = ["input_cache_read", "input_cache_write", "input_cache_write_1h"]
        for cf in cache_fields:
            if cf in pricing:
                print(f"   * pricing.{cf}: {pricing[cf]}")
                
        # 2. Test del integrador LLMDataIngester.fetch_openrouter
        print("\n[INGESTER] Probando normalización con LLMDataIngester...")
        ingester = LLMDataIngester()
        normalized_models = await ingester.fetch_openrouter(client)
        
        assert len(normalized_models) > 0, "No se pudieron normalizar los modelos de OpenRouter"
        print(f"Modelos normalizados con éxito: {len(normalized_models)}")
        
        # Buscar el modelo correspondiente en los normalizados
        sample_norm = None
        for nm in normalized_models:
            if nm.get("model_id") == sample.get("id"):
                sample_norm = nm
                break
        if not sample_norm:
            sample_norm = normalized_models[0]
            
        print(f"\n[NORMALIZACIÓN] Modelo normalizado correspondiente ({sample_norm.get('model_id')}):")
        
        norm_keys = [
            "model_id", "name", "context_length", 
            "cost_input_per_m", "cost_output_per_m", 
            "cost_cache_read_per_m", "cost_cache_write_per_m", 
            "hosting"
        ]
        for nk in norm_keys:
            assert nk in sample_norm, f"Falta la clave normalizada '{nk}'"
            print(f" - {nk}: {sample_norm[nk]}")
            
    print("\n[SUCCESS] Todos los tests de estructura y normalizacion de OpenRouter pasaron exitosamente!")

def test_openrouter_structure():
    asyncio.run(run_openrouter_test())

if __name__ == "__main__":
    test_openrouter_structure()
