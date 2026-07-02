import requests
import json

try:
    response = requests.get("https://openrouter.ai/api/v1/models", timeout=12)
    if response.status_code == 200:
        data = response.json()
        models = data.get("data", [])
        if models:
            # Let's find a model with a comprehensive set of fields
            # e.g., one that has pricing, architecture details, etc.
            example_model = None
            for m in models:
                if "claude-3-haiku" in m["id"]:
                    example_model = m
                    break
            if not example_model:
                example_model = models[0]
            
            print("Keys in a model object:")
            print(list(example_model.keys()))
            print("\nFull structure of the example model:")
            print(json.dumps(example_model, indent=2))
        else:
            print("No models found in response data.")
    else:
        print(f"Failed to fetch: {response.status_code}")
except Exception as e:
    print(f"Error: {e}")
