import requests
import json

base_url = "https://storage.googleapis.com/crfm-helm-public/"
path_core = "capabilities/benchmark_output/releases/v1.0.0/groups/core_scenarios.json"
response = requests.get(base_url + path_core)

if response.status_code == 200:
    data = response.json()
    print("Type of data:", type(data))
    if isinstance(data, list) and len(data) > 0:
        first_item = data[0]
        print("Keys in the first item of list:", list(first_item.keys()))
        print("Title of first item:", first_item.get("title"))
        
        # Let's inspect rows
        rows = first_item.get("rows", [])
        print("Number of rows:", len(rows))
        if rows:
            print("First row structure:")
            print(json.dumps(rows[0], indent=2))
            
            # Print a few model names and their scores
            print("\nSample models and scores:")
            for row in rows[:5]:
                print(f"Model: {row.get('cells', [{}])[0].get('value')} | Mean Score: {row.get('cells', [{}])[1].get('value')}")
