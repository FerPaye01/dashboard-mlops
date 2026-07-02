import requests
import json

url = "https://huggingface.co/api/datasets/lmarena-ai/leaderboard-dataset"

try:
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        data = response.json()
        siblings = data.get("siblings", [])
        print("Total files:", len(siblings))
        for s in siblings:
            fn = s.get("rfilename")
            if "leaderboard" in fn.lower() or "arena" in fn.lower() or "latest" in fn.lower() or fn.endswith(".parquet"):
                print(" -", fn)
    else:
        print("Error:", response.status_code)
except Exception as e:
    print("Exception:", e)
