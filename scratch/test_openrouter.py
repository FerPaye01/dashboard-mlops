import requests
import json

try:
    response = requests.get("https://openrouter.ai/api/v1/models", timeout=12)
    if response.status_code == 200:
        data = response.json()
        models = data.get("data", [])
        print(f"Total models fetched: {len(models)}")
        claude_models = [m for m in models if "claude" in m["id"].lower() or "opus" in m["id"].lower()]
        for m in claude_models:
            print(f"ID: {m['id']} | Name: {m.get('name')} | Pricing: {m.get('pricing')}")
    else:
        print(f"Failed to fetch: {response.status_code}")
except Exception as e:
    print(f"Error: {e}")
