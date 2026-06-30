import requests
import json

response = requests.get("https://openrouter.ai/api/v1/models", timeout=12)
if response.status_code == 200:
    data = response.json()
    models = data.get("data", [])
    print(f"Total models: {len(models)}")
    # Find Claude 3.5 Sonnet or GPT-4o
    target_ids = ["anthropic/claude-3.5-sonnet", "openai/gpt-4o", "meta-llama/llama-3-8b-instruct"]
    found = [m for m in models if m["id"] in target_ids]
    if not found:
        # Just grab the first few models
        found = models[:3]
    for m in found:
        print("\n" + "="*40)
        print(f"Model ID: {m['id']}")
        print(f"Keys: {list(m.keys())}")
        # Print pretty JSON of the model metadata
        print(json.dumps(m, indent=2))
else:
    print(f"Error: {response.status_code}")
