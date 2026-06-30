import requests
import json

url = "https://datasets-server.huggingface.co/search"
# Query for a known model: meta-llama/Meta-Llama-3-8B-Instruct
params = {
    "dataset": "open-llm-leaderboard/contents",
    "config": "default",
    "split": "train",
    "query": "Meta-Llama-3-8B-Instruct",
    "offset": 0,
    "length": 5
}
try:
    print(f"Searching for model in leaderboard dataset...")
    response = requests.get(url, params=params, timeout=10)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        rows = data.get("rows", [])
        print(f"Found {len(rows)} matching rows.")
        for row in rows:
            model_info = row.get("row", {})
            print(f"\nModel ID found: {model_info.get('fullname') or model_info.get('eval_name')}")
            print(f"IFEval: {model_info.get('IFEval')}")
            print(f"GPQA: {model_info.get('GPQA')}")
            print(f"MMLU-PRO: {model_info.get('MMLU-PRO')}")
            print(f"Average: {model_info.get('Average ⬆️')}")
    else:
        print("Response Text:", response.text[:300])
except Exception as e:
    print(f"Error: {e}")
