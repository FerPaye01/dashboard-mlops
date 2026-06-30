import requests
import json

url = "https://datasets-server.huggingface.co/rows?dataset=open-llm-leaderboard/contents&config=default&split=train&offset=0&limit=5"
try:
    print(f"Querying HF datasets-server: {url}")
    response = requests.get(url, timeout=10)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        rows = data.get("rows", [])
        print(f"Fetched {len(rows)} rows.")
        if rows:
            print("\nFirst row sample:")
            print(json.dumps(rows[0], indent=2))
    else:
        print("Response Text:", response.text[:300])
except Exception as e:
    print(f"Error: {e}")
