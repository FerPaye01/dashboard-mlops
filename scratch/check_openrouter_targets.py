import requests
import json

response = requests.get("https://openrouter.ai/api/v1/models", timeout=12)
if response.status_code == 200:
    data = response.json()
    models = data.get("data", [])
    target_models = [
        "anthropic/claude-3.5-sonnet",
        "anthropic/claude-3-opus",
        "openai/gpt-4o",
        "deepseek/deepseek-r1"
    ]
    for m in models:
        for target in target_models:
            if target in m["id"].lower():
                print("\n" + "="*40)
                print(f"Model: {m['id']}")
                print("Benchmarks found:")
                print(json.dumps(m.get("benchmarks"), indent=2))
else:
    print(f"Error: {response.status_code}")
